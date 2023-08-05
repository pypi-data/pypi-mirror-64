#==============================================================================
#
#  $Id$
#
"""
   My first cut at writing a Proactor framework.

   The Proactor pattern is a concept introduced to me by Alex Libman (author
   of the ACE Proactor, and the single best communication framework programmer
   that I have ever had the pleasure of working with).  Proactor is almost an
   extension of the standard Reactor pattern - both make callbacks to
   handler classes in response to low-level communications events.  The
   difference between the two is that while the Reactor notifies the handler
   when the communication channel is /ready/ for a read or write, the Proactor
   actually /performs/ the IO, notifying the handler only to put received data
   to it and get received data from it.

   This approach is superior because it completely hides the
   details of the underlying communication channel from the data handler,
   allowing the implementation details to be custom-tailored to whatever
   mechanisms are available on the operating system.

   TODO: provide the proactor and the connection object to the handlers
   through the callback methods.
"""
#
#  Copyright (C) 2006 Michael A. Muller
#
#  Permission is granted to use, modify and redistribute this code,
#  providing that the following conditions are met:
#
#  1) This copyright/licensing notice must remain intact.
#  2) If the code is modified and redistributed, the modifications must
#  include documentation indicating that the code has been modified.
#  3) The author(s) of this code must be indemnified and held harmless
#  against any damage resulting from the use of this code.
#
#  This code comes with ABSOLUTELY NO WARRANTEE, not even the implied
#  warrantee of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#==============================================================================

import six
import socket, select, fcntl, os, errno, weakref
from threading import RLock
from spug.util.process import ChildProcess
from .reactor import *

class DataHandler:
   """
      Abstract interface for classes that server and retrieve data.
   """

   READ = 1
   WRITE = 2

   def onPollFrame(self):
      """
         Called at the beginning of every poll that will involve the data
         handler, before any of the other methods.
      """
      pass

   def readyToGet(self):
      """
         Returns true if the handler is ready to provide data to its
         connection via @get().
      """
      raise NotImplementedError()

   def readyToPut(self):
      """
         Returns true if the handler is ready to consume data from its
         connection via @put()
      """
      raise NotImplementedError()

   def readyToClose(self):
      """
         Returns true if the handler is ready to close.  The Proactor will
         respond to this by shutting down the connection and discarding the
         handler.

         May be implemented by derived classes, base class implementation
         always returns False.
      """
      return False

   def handleConnect(self):
      """
         Called by Proactor when the connection is fully initialized.

         May be overriden, base class version does nothing.

         TODO: call this!!
      """
      pass

   def peek(self, size):
      """
         Called by Proactor when the connection is ready to write data and the
         handler is ready to read.  Should return a string buffer no bigger
         than /size/.  Note that the data buffer should not be considered to
         have been consumed by the underlying communicaton channel until
         @get() has been called - multiple calls to peek() without
         a call to @get() should return the same data block.

         parms:
            size::
               [int] maximum size of buffer to return
      """
      raise NotImplementedError()

   def get(self, size):
      """
         Called by Proactor when the block of data returned by the last
         @peek() has successfully been written to the communication
         channel.

         parms:
            size::
               [int] maximum size of buffer to return.  This will always be
               less than or equal to the size of the data a returned from the
               last peek().
      """
      raise NotImplementedError()

   def put(self, data):
      """
         Called by Proactor when data has been read from the connection.

         parms:
            data::
               [string] the data that has been read.
      """
      raise NotImplementedError()

   def handleError(self):
      """
         Called by Proactor when an error occurs on the stream.

         May be implemented by derived classes, base class implementation
         deregisters.
      """
      pass

   def handleDisconnect(self, mode):
      """
         Called by Proactor when the connection disconnects.

         This will be called twice - with mode = READ when the read (put())
         side of the connection disconnects, with mode WRITE when the write
         (get()) side disconnects.

         The handler should not attempt to deregister the object from the
         proactor - this will be done automatically by the proactor.

         May be implemented by derived classes, base class implementation does
         nothing.
      """
      pass

class ConnectHandler:
   """
      Abstract interface for classes that provide a connect callback and
      create @DataHandler's.
   """

   def handleConnect(self, connection):
      """
         Called by the @Proactor when a new connection has been received.  The
         handler should use this opportunity to provide the connection with a
         @DataHandler.
      """
      raise NotImplementedError()

   def readyToClose(self):
      """
         When this method returns true, it signals the proactor to remove the
         ConnectHandler and its associated listener from the list of monitored
         objects and shut down the listener.

         May be overriden by derived classes.  Base class implementation
         always returns False.
      """
      return False

class Connection(ConnectionSocket):
   """
      Provids the glue between reactor's ConnectionSocket and the Proactor's
      DataHandler.
   """

   def __init__(self, proactor, sock = None, addr = None, dataHandler = None):
      if sock:
         ConnectionSocket.__init__(self, sock = sock)
      else:
         ConnectionSocket.__init__(self, addr = addr)
      self.dataHandler = dataHandler
      self.__proactor = weakref.ref(proactor)
      self.__closed = False

   def onPollFrame(self):
      if self.dataHandler:
         self.dataHandler.onPollFrame()

   def wantsToRead(self):

      # check to see if the data handler wants to shutdown.  If it does,
      # remove it from the proactor and close the connection.  We could just
      # as easily do this from wantsToWrite().
      if self.dataHandler and self.dataHandler.readyToClose():
         # we can get away with a None argument here because it isn't used by
         # the disconnect handler
         self.handleDisconnect(None)
         return False

      elif self.connected and self.dataHandler:
         return self.dataHandler.readyToPut()

      else:
         return False

   def wantsToWrite(self):

      # if we're not connected yet, we always want to be checked for ready to
      # write because that tells us when we are connected.
      if not self.connected:
         return True

      elif self.dataHandler:
         return self.dataHandler.readyToGet()

      else:
         return False

   def handleRead(self, dispatcher):

      # catch error 104 (connection reset by peer) - seems to happen sometimes
      try:
         data = os.read(self._sock.fileno(), MTU)
      except OSError as ex:
         if ex.errno == errno.ECONNRESET:
            data = b''
         else:
            raise

      if not data:
         # treat this as a disconnect (XXX can we still be writable after read
         # comes back empty?)
         debug('read channel closed!')
         self.handleDisconnect(dispatcher)
      else:
         self.dataHandler.put(data)

   def handleWrite(self, dispatcher):
      if not self.connected:
         ConnectionSocket.handleWrite(self, dispatcher)
         self.dataHandler.handleConnect()
         return
      data = six.ensure_binary(self.dataHandler.peek(MTU))
      try:
         written = os.write(self._sock.fileno(), data)
      except OSError as ex:
         # treat broken pipe errors as disconnects, re-raise everything else.
         if ex.errno == errno.EPIPE:
            self.handleDisconnect(dispatcher)
            return
         else:
            raise
      self.dataHandler.get(written)

   def handleError(self, dispatcher):
      if self.dataHandler:
         self.dataHandler.handleError()

   def handleDisconnect(self, dispatcher):
      if not self.__closed:
         if self.dataHandler:
            self.dataHandler.handleDisconnect(DataHandler.READ | DataHandler.WRITE)
            self.dataHandler = None

         self.__proactor().remove(self)
         self._sock.close()
         self.__closed = True
      else:
         print('connection %s is already closed' % self)

   def setDataHandler(self, handler):
      """
         Sets the data handler for the connection.
      """
      self.dataHandler = handler

class Listener(ListenerSocket):
   """
      Provides the glue between ConnectionSocket and ConnectHandler.
   """

   def __init__(self, proactor, sock = None, inetAddress = None,
                connectHandler = None
                ):
      ListenerSocket.__init__(self, sock, inetAddress)
      self.__connectHandler = connectHandler
      self.__proactor = weakref.ref(proactor)

   def handleNewConnection(self, dispatcher, sock, addr):
      connection = Connection(self.__proactor(), sock)

      # give it to our handler
      if self.__connectHandler:
         self.__connectHandler.handleConnect(connection)

      # register the new connection
      dispatcher.addReactable(connection)

   def wantsToRead(self):

      # if the handler is ready to close, deregister this object and close the
      # underlying socket.
      if self.__connectHandler and self.__connectHandler.readyToClose():
         self.__proactor().remove(self)
         self._sock.close()
         return False

      else:
         return True

class Proactor:
   """
      An abstract base class defining the Proactor interrface.  Proactor
      attempts to abstract all details of communication multiplexing away from
      the user.
   """

   def run(self):
      """
         Waits for events and dispatches them to handlers until all
         connections terminate.
      """
      raise NotImplementedError()

   def makeWrapper(self, file, dataHandler):
      """
         Creates and returns a wrapper around an existing file object.

         The use of this method should be avoided, as it may not be portable.
      """
      raise NotImplementedError()

   def makeListener(self, address, connectHandler):
      """
         Creates and returns a new listener.

         parms:
            address::
               [@Address]
      """
      raise NotImplementedError()

   def makeConnection(self, address, dataHandler):
      """
         Creates and returns a new connection.

         parms:
            address::
               [@Address]
      """
      raise NotImplementedError()

   def makePipe(self, readHandler, writeHandler):
      """
         Creates and returns a tuple of two new connections constituting a
         pipe.  The first is a read pipe, the second is a write pipe.

         parms:
            readHandler::
               [@DataHandler] data handler for the read side of the
               connection.
            writeHandler::
               [@DataHandler] data handler for the write side of the
               conneciton.
      """
      raise NotImplementedError()

   def makeControlQueue(self, queueHandler):
      """
         Creates a "control queue" which can be used to send messages to the
         proactor from another thread.

         parms:
            queueHandler::
               [callable<any>] a function that gets called (and passed the
               element) every time an element gets removed from the queue.

         returns: [ControlQueue] a new ControlQueue instance.
      """
      raise NotImplementedError()

   def makeSubprocess(self, cmd, stdinHandler = None, stdoutHandler = None,
                      stderrHandler = None
                      ):
      """
         Creates a subprocess and connections for standard input, output and
         error.  Returns a tuple<spug.util.process.ChildProcess, Connection,
         ...> containing as many connections as were created - same as the
         number of handlers passed in.

         The function allows passing handlers for standard input, standard
         output and standard error.  When these are not provided (passed in as
         None) the channels are unmanaged, and fall through to the
         standard input, output and error channels for the process.

         parms:
            cmd: [list<str>] the command to run.
            stdinHandler: [@DataHandler or None] Standard input handler.
            stdoutHandler: [@DataHandler or None] Standard output handler.
            stderrHandler: [@DataHandler or None] Standard error handler.
      """
      raise NotImplementedError()

   def add(self, object):
      """
         Adds the object from the set of managed objects.  /object/ must be an
         object returned from one of the "make" methods.

         XXX I have some doubts about addding this method - if one proactor
         tries to add objects created by another proactor using a very
         different implementation, things will probably break.  Should at
         least verify that the object is of the proper type for the proactor.

         Must be implemented by derived class.

         parms:
            object::
               [any] A proactor object created using one of the "make"
               methods.
      """
      raise NotImplementedError()

   def remove(self, object):
      """
         Removes the object from the set of managed objects.  /object/ must be
         an object returned from one of the "make" methods.

         parms:
            object::
               [any] A proactor object created using one of the "make"
               methods.
      """
      raise NotImplementedError()

   def hasConnections(self):
      """
         Returns true if the proactor has any connections.
      """
      raise NotImplementedError()

class ControlQueue:
   """
      A queue that can be used to communicate with a proactor from an external
      thread.
   """

   class _DataHandlerAdapter(DataHandler):
      """
         Provdes a data handler adapter facade for the queue so that it can
         be managed by the proactor.
      """

      def __init__(self, queue):
         self.__queue = queue

      def readyToGet(self):
         # the proactor-facing side of the connection is not a data source
         return False

      def readyToPut(self):
         return not self.__queue._closed

      def readyToClose(self):
         return self.__queue._closed

      def put(self, data):
         self.__queue.processElems(len(data))

   def __init__(self, writeStream, handler):
      self.__out = writeStream
      self.__elems = []
      self.__lk = RLock()
      self.__handler = handler
      self._closed = False

   def _getDataHandlerAdapter(self):
      """
         Returns a data handler for the class - this allows us to plug our
         queue into a proactor.
      """
      return self._DataHandlerAdapter(self)

   def add(self, elem):
      """
         Add a new element to the queue.

         parms:
            elem: [object] object that will be passed to the handler from the
               proactor loop.
      """
      self.__lk.acquire()
      try:
         self.__elems.append(elem)
         self.__out.write(b'x')
         self.__out.flush()
      finally:
         self.__lk.release()

   def processElems(self, count):
      """
         Process the specified number of eleements.
      """
      self.__lk.acquire()
      try:
         while count:

            # get the next element, call the handler
            elem = self.__elems.pop(0)
            self.__handler(elem)

            count -= 1
      finally:
         self.__lk.release()

   def close(self):
      """
         Close the queue.
      """
      self._closed = True

class ReactorProactor(Proactor):
   """
      Proactor implementation based on a reactor.
   """

   def __init__(self, reactor):
      self.__dispatcher = reactor

   def makeWrapper(self, file, dataHandler):
      conn = Connection(self, file, dataHandler = dataHandler)
      self.__dispatcher.addReactable(conn)
      return conn

   def makeListener(self, address, connectHandler):
      listener = \
         Listener(self, inetAddress = address, connectHandler = connectHandler)
      self.__dispatcher.addReactable(listener)
      return listener

   def makeConnection(self, address, dataHandler):
      debug('making connection %s, %s', address, dataHandler)
      connection = \
         Connection(self, addr = address, dataHandler = dataHandler)
      self.__dispatcher.addReactable(connection)
      return connection

   def makePipe(self, readHandler, writeHandler):
      reader, writer = os.pipe()
      reader = \
         Connection(self, os.fdopen(reader, 'rb'), dataHandler = readHandler)
      writer = \
         Connection(self, os.fdopen(writer, 'wb'), dataHandler = writeHandler)
      self.__dispatcher.addReactable(reader)
      self.__dispatcher.addReactable(writer)
      return reader, writer

   def makeControlQueue(self, queueHandler):
      reader, writer = os.pipe()

      # create a control queue
      queue = ControlQueue(os.fdopen(writer, 'wb'), queueHandler)

      reader = Connection(self, os.fdopen(reader, 'rb'),
                          dataHandler = queue._getDataHandlerAdapter()
                          )
      self.__dispatcher.addReactable(reader)

      return queue

   def makeSubprocess(self, cmd, stdinHandler = None, stdoutHandler = None,
                      stderrHandler = None
                      ):
      noStdIn = not stdinHandler
      noStdOut = not stdoutHandler
      noStdErr = not stderrHandler

      process = ChildProcess(cmd, True, noStdIn = noStdIn, noStdOut = noStdOut,
                             noStdErr = noStdErr
                             )

      result = (process,)
      if stdinHandler:
         stdin = Connection(self, process.getRawStdin(),
                            dataHandler = stdinHandler
                            )
         self.__dispatcher.addReactable(stdin)
         result = result + (stdin,)

      if stdoutHandler:
         stdout = Connection(self, process.getRawStdout(),
                            dataHandler = stdoutHandler
                            )
         self.__dispatcher.addReactable(stdout)
         result = result + (stdout,)

      if stderrHandler:
         stderr = Connection(self, process.getRawStderr(),
                             dataHandler = stderrHandler
                             )
         self.__dispatcher.addReactable(stderr)
         result = result + (stderr,)

      return result

   def add(self, object):
      debug('adding object %s', object)
      self.__dispatcher.addReactable(object)

   def remove(self, object):
      debug('removing object %s', object)
      self.__dispatcher.removeReactable(object)

   def schedule(self, when, action):
      """
         Schedules an action to be performed at a particular time.

         parms:
            when: [float] Time measured in seconds from now.  If this is
               negative or zero, the action will be performed the next time we
               get an event.
            action: [callable<>] Action to be performed.
      """
      self.__dispatcher.schedule(when, action)

   def hasConnections(self):
      return self.__dispatcher.hasReactables()

   def processOneEvent(self):
      self.__dispatcher.processOneEvent()

   def run(self):
      self.__dispatcher.run()

def createProactor():
   """
      Returns a new instance of the optimal proactor for the current platform.
   """
   return ReactorProactor(Dispatcher())

_proactorSingleton = None
def getProactor():
   """
      Returns the global proactor singleton, creating it if necessary.
   """
   global _proactorSingleton
   if _proactorSingleton is None:
      _proactorSingleton = ReactorProactor(Dispatcher())
   return _proactorSingleton

