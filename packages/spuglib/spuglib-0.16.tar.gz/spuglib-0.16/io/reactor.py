#==============================================================================
#
#  $Id$
#
"""
   Classes providing a basic reactor implementation.
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

import errno, select, socket, time
try:
   # python2
   from itertools import izip
except ImportError:
   izip = zip
from spug.util.log import debug

MTU = 4096

class Address:
   """
      Abstract base class for addresses.
   """

   def getProtoFamily(self):
      """
         Returns the protocol family constant for the address (the first
         argument to a socket() call)
      """
      raise NotImplementedError()

   def asBindArg(self):
      """
         Returns the address in a form suitable for use in the socket bind()
         or connect() calls.
      """
      raise NotImplementedError()

   def getConnectedAddress(self, addr):
      """
         Returns a new @Address derivative instance for the given low-level
         address (as returned from the accept() call).
      """
      raise NotImplementedError()

class INETAddress(Address):
   """
      Standard internet address.  IP address and port.
   """

   def __init__(self, host, port):
      """
         parms:
            host::
               [string] hostname or IP address.
            port::
               [int] port number
      """
      self.host = host
      self.port = port

   def getProtoFamily(self):
      return socket.AF_INET

   def asBindArg(self):
      return (self.host, self.port)

   def getConnectedAddress(self, addr):
      return INETAddress(addr[0], addr[1])

   def __str__(self):
      return 'INETAddress(%s:%s)' % (self.host, self.port)

class UNIXAddress(Address):
   """
      Unix domain socket address.

      Public-vars:
            path::
               [string] path name of socket file.
   """

   def __init__(self, path):
      self.path = path

   def getProtoFamily(self):
      return socket.AF_UNIX

   def asBindArg(self):
      return self.path

   def getConnectedAddress(self, addr):
      return UNIXAddress(addr)

   def __str__(self):
      return 'UNIXAddress(%s)' % self.path

class Reactable:

   def onPollFrame(self):
      """
         Called at the beginning of a poll frame, before any of the "wantsTo"
         methods and waiting for events.
      """
      pass

   def wantsToRead(self):
      """
         Returns true if the connection should be checked for readability
      """
      raise NotImplementedError()

   def wantsToWrite(self):
      """
         Returns true if the connection should be checked for writability.
      """
      raise NotImplementedError()

   def handleRead(self, dispatcher):
      """
         Called when the connection is ready to read.
      """
      raise NotImplementedError()

   def handleWrite(self, dispatcher):
      """
         Called when the connection is ready to write.
      """
      raise NotImplementedError()

   def handleError(self, dispatcher):
      """
         Called when there is an error.
      """
      raise NotImplementedError()

   def handleDisconnect(self, dispatcher):
      """
         Called when a disconnect occurs.
      """
      raise NotImplementedError()

   def fileno(self):
      """
         Returns the file descriptor.
      """
      raise NotImplementedError()

class Socket(Reactable):
   """
      Base class for socket types.  Just manages the handle.
   """

   def __init__(self, sock):
      self._sock = sock

   def fileno(self):
      return self._sock.fileno()

class ConnectionSocket(Socket):
   """
      Socket used for sending and receiving data.

      This is an abstract class, and must be implemented by derived classes.
      Derived classes must respect the state of the connected instance
      variable.  They should not attempt any reads or writes, or return true
      from @wantsToRead(), until "connected" becomes true.  Furthermore,
      @wantsToRead() must always return true until connected, and
      @handleWrite() must set connected to true.  This behavior is
      implemented in the base class methods.

      Public-vars:
         connected::
            [boolean] true if the socket is currently connected.
   """

   def __init__(self, sock = None, addr = None):
      debug('ConnectionSocket.__init__(sock = %s, addr = %s', sock, addr)
      if addr:
         # initiate the connection in non-blocking mode.  When the connection
         # is completed, the socket will be "ready to write"
         sock = socket.socket(addr.getProtoFamily(), socket.SOCK_STREAM, 0)
         sock.setblocking(False)
         try:
            bindArg = addr.asBindArg()
            debug('connecting to %s', bindArg)
            sock.connect(bindArg)
         except socket.error as ex:
            # an "in progress" error is expected in this situation
            if ex.errno != errno.EINPROGRESS:
               raise

         # indicate that we are not fully connected
         self.connected = False
      else:
         self.connected = True

      Socket.__init__(self, sock)

   def wantsToWrite(self):
      """
         Implements @Reactable.wantsToWrite() so that we can determine when we
         become connected.

         Derived classes may override, but they must always return True when
         the connected instance variable is false.
      """
      if not self.connected:
         return True

   def handleWrite(self, dispatcher):
      """
         Implements @Reactable.handleWrite() so that we can determine when
         we become connected.

         Derived classes may override, but they must always call the base
         class implementation when the connected instance variable is false.
      """
      if not self.connected:
         self.connected = True

class ListenerSocket(Socket):
   """
      A server side socket - listens for new connections and creates
      ConnectionSocket objects for them.
   """
   def __init__(self, sock = None, addr = None):
      if not sock:
         # XXX what about UDP, and UNIX sockets??
         sock = socket.socket(addr.getProtoFamily(), socket.SOCK_STREAM, 0)
         sock.setblocking(False)
         sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
         sock.bind(addr.asBindArg())
         sock.listen(5)
         self.__addr = addr
      # XXX how to I give an address to these?
      Socket.__init__(self, sock)

   def wantsToRead(self):
      # always ready to listen for a new connection
      return True

   def wantsToWrite(self):
      # never writable
      return False

   def handleRead(self, reactor):
      # get the new connection
      sock, addr = self._sock.accept()
      sock.setblocking(False)

      self.handleNewConnection(reactor, sock,
                               self.__addr.getConnectedAddress(addr)
                               )

   def handleNewConnection(self, dispatcher, sock, addr):
      """
         Called when a new connection is created.

         Must be implemented by derived classes.  Typical implementation would
         be to create a class derived from ConnectionSocket and register it
         with the reactor.

         parms:
            dispatcher::
               [@Dispatcher]
            sock::
               [socket] the newly accepted socket connection
            connection::
               [ConnectionSocket]
      """
      raise NotImplementedError()

class PollDispatcher:
   """
      Reactor implementation based on the poll() function.
   """

   def __init__(self):
      self.__objs = []
      self.__schedule = []

   def addReactable(self, obj):
      """
         Adds a new reactable to the set of managed objects.

         parms:
            obj::
               [Reactable]
      """
      self.__objs.append(obj)

   def schedule(self, when, action):
      """
         Schedules an action to be performed at a particular time.

         parms:
            when: [float] Time measured in seconds from now.  If this is
               negative or zero, the action will be performed the next time we
               get an event.
            action: [callable<>] Action to be performed.
      """
      # convert to absolute time
      when = time.time() + when

      # find the place in the queue to put it
      i = 0
      for i, (t, a) in izip(range(len(self.__schedule)), self.__schedule):
         if when < t:
            break
      else:
         i += 1

      self.__schedule.insert(i, (when, action))

   def __getPollFlags(self, obj):
      "Returns the poll flags for an object based on its state"
      errorFlags = select.POLLERR | select.POLLHUP | select.POLLNVAL
      flags = 0
      if obj.wantsToRead():
         flags |= select.POLLIN | errorFlags
      if obj.wantsToWrite():
         flags |= select.POLLOUT | errorFlags

      return flags

   def removeReactable(self, object):
      self.__objs.remove(object)

   def hasReactables(self):
      """
         Returns true if the dispatcher has reactables.
      """
      return bool(self.__objs)

   def processOneEvent(self):
      poll = select.poll()

      # register all of the objects
      map = {}
      objs = self.__objs[:]
      debug('polling')

      # First call of the start methods.
      for obj in objs:
         obj.onPollFrame()

      # Now get the flags.
      for obj in objs:
         flags = self.__getPollFlags(obj)

         # it is possible for an object to deregister itself in its "wantsTo"
         # callbacks.  So check to make sure it's still in objs before
         # registering it with the poll
         if obj in self.__objs:
            debug('  registering object for %d: %s', flags, obj)
            poll.register(obj, flags)
            map[obj.fileno()] = obj

      # if we didn't end up with any file descriptors and there are no
      # events scheduled, return now
      if not map and not self.__schedule:
         debug('nothing to do')
         return

      # calculate the timeout from the time of the next scheduled event
      if self.__schedule:
         timeout = (self.__schedule[0][0] - time.time()) * 1000
      else:
         timeout = None

      results = []
      while timeout is None or timeout > 0:
         try:
            debug('timeout = %s', timeout)
            results = poll.poll(timeout)
            break
         except select.error as ex:
            # errno 4 == EINTR - interrupted system call.  We got a signal.
            # Anything else we want to throw
            if ex.errno != 4:
               raise

      # dispatch the results
      for fd, events in results:
         debug('events = %s', events)
         obj = map[fd]
         gotRead = False
         if events & select.POLLIN:
            debug('read event on %s', obj)
            obj.handleRead(self)
            gotRead = True
         if events & select.POLLOUT:
            debug('write event on %s', obj)
            obj.handleWrite(self)
         if events & select.POLLERR:
            debug('error event on %s', obj)
            obj.handleError(self)
         if events & select.POLLHUP:
            debug('HUP event on %s', obj)
            obj.handleDisconnect(self)

      # perform all scheduled events
      curTime = time.time()
      while self.__schedule and curTime >= self.__schedule[0][0]:
         t, action = self.__schedule.pop(0)
         action()

   def run(self):
      while self.__objs:
         self.processOneEvent()

Dispatcher = PollDispatcher
