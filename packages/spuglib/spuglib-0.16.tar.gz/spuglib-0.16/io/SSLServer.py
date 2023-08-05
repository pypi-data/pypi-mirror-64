#==============================================================================
#
#  $Id$
#
"""
   Proactor based SSLServer implementation.
   
   This now also functions as an SSL client, the module needs to be renamed.

   The SSL data handler is designed to wrap another data handler, allowing you
   to easily SSLify any protocol with a data handler.
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

from spug.io.proactor import DataHandler, ConnectHandler
from spug.util.log import debug, warn, error
from _minssl import *

class SSLDataHandler(DataHandler):
   """
      Data handler for both client and server-side connections.
   """

   ACCEPTING = 'ACCEPTING'
   PRECONNECT = 'PRECONNECT'  # still doing TCP connection   
   CONNECT = 'CONNECT'
   CONNECTED = 'CONNECTED'
   SHUTDOWN_PENDING = 'SHUTDOWN_PENDING'
   CLOSED = 'CLOSED'


   def __init__(self, delegate, keyFile, certFile, server):
      """
	 parms:
	    delegate::
	       [@DataHandler] we pass all method invocations to this object as
	       soon as the SSL initialization sequence is established.
	    keyFile::
	       [string] name of the SSL private key file
	    certFile::
	       [string] name of the SSL certificate file
	    server:
	       [bool] True if this is a server (starts in acceptING state, otherwise 
	       start in PRECONNECT state)
      """
      self.__delegate = delegate
      self.__output = ''
      self.__ssl = None

      # create two memory BIOs
      self.__readBIO = BIO_new(BIO_s_mem())
      self.__writeBIO = BIO_new(BIO_s_mem())

      # create the context and associate it with the certificate and private
      # key files
      self.__ctx = SSL_CTX_new(SSLv23_method())
      if SSL_CTX_use_certificate_file(self.__ctx, certFile, 
                                      SSL_FILETYPE_PEM) != 1:
         raise Exception('Error loading certificate file')
      if SSL_CTX_use_PrivateKey_file(self.__ctx, keyFile, 
                                     SSL_FILETYPE_PEM) != 1:
         raise Exception('Error loading private key')

      # create the SSL object, associated it with the read and write buffers
      self.__ssl = SSL_new(self.__ctx)
      SSL_set_bio(self.__ssl, self.__readBIO, self.__writeBIO)

      # put it into pre-connect state
      if server:
         SSL_set_accept_state(self.__ssl)
         self.__state = self.ACCEPTING
      else:
         self.__state = self.PRECONNECT
      self.__readyToRead = True

   # so here's the basic idea: 
   #
   # when we're connected, we want to just serve as an intermediary to the
   # delegate.  When we're in the ACCEPTING or any of the shutdown states, we
   # want to call the SSL_accept and SSL_shutdown functions respectively until
   # they tell us they're done.
   #
   # The sole channel for communication with the rest of the functions is the
   # read and write BIOs.  __output is used as a staging area for data that
   # has been peeked but not gotten, but that is above the level of the state
   # machine.

   def onPollFrame(self):
      # XXX Changed the conect clause for client, I think that's all.
      if self.__state in (self.CONNECT, self.ACCEPTING):
         self.__readyToRead = False
         if self.__state == self.CONNECT:
            rc = SSL_connect(self.__ssl)
         else:
            rc = SSL_accept(self.__ssl)
         if rc == 1:
            self.__state = self.CONNECTED
         else:
            rc = SSL_get_error(self.__ssl, rc)
            if rc == SSL_ERROR_WANT_READ:
               self.__readyToRead = True
               return
            elif rc == SSL_ERROR_SSL:
               # protocol error - log an error message and drop the connection
               error('Protocol error')
               self.__output = ''
               self.__state = self.CLOSED
            else:
               raise Exception('got ssl error: %d' % rc)

      if self.__state == self.CONNECTED:

         # if we're connected, everything falls through to the delegate

         if self.__delegate.readyToClose():
            self.__state = self.SHUTDOWN_PENDING

         else:
            # instead of 1024, should use the last MTU size received from the
            # proactor

            # feed the delegate data from the SSL object until either we run
            # out or he can't take no more
            data = True
            while self.__delegate.readyToPut():
               data = SSL_readx(self.__ssl, 1024)
               if data == SSL_ERROR_WANT_READ:
                  self.__readyToRead = True
                  break
               elif not data:
                  debug('out of data in read buffer')
                  self.__delegate.put('')
                  break
               else:
                  debug('putting data %s' % repr(data))
                  self.__delegate.put(data)

            if self.__delegate.readyToGet() and \
               BIO_ctrl_pending(self.__writeBIO) < 1024:

               # pull the data from the delegate
               data = self.__delegate.peek(1024)
               self.__delegate.get(len(data))
               debug('got data %s' % repr(data))
               
               # push it through SSL
               SSL_write(self.__ssl, data)
            
            if self.__delegate.readyToClose():
               self.__state = self.SHUTDOWN_PENDING

      if self.__state == self.SHUTDOWN_PENDING:

         self.__readyToRead = False
         rc = SSL_shutdown(self.__ssl)
         if rc > -1:
            # if we've pushed everything to the client, we're done
            if BIO_ctrl_pending(self.__writeBIO) == 0:
               self.__state = self.CLOSED
         else:
            errCode = SSL_get_error(self.__ssl, rc)
            if errCode == SSL_ERROR_WANT_READ:
               self.__readyToRead = True
            elif errCode != SSL_ERROR_WANT_WRITE:
               raise Exception('got error during shutdown: %d' % errCode)

   def readyToGet(self):
      return BIO_ctrl_pending(self.__writeBIO) and True or False

   def readyToPut(self):
      return self.__readyToRead

   def readyToClose(self):
      return not self.__output and self.__state == self.CLOSED

   def handleConnect(self):
      self.__state = self.CONNECT
   
   def handleError(self):
      debug('got error')
      self.__delegate.handleError()

   def peek(self, size):
      if len(self.__output) < size:
         self.__output += BIO_readx(self.__writeBIO, size - len(self.__output))
      data = self.__output[:size]
      debug('peeking %s' % repr(data))
      return data

   def get(self, size):
      self.__output = self.__output[size:]

   def put(self, data):
      debug('putting %s' % repr(data))
      BIO_write(self.__readBIO, data)

   def __del__(self):
      # clean up all of the allocated SSL objects (we don't need to free the
      # BIO's - this will be done by the SSL object)
      if self.__ssl:
         SSL_free(self.__ssl)
         SSL_CTX_free(self.__ctx)

class SSLConnectHandler(ConnectHandler):
   """
      Simple SSL HTTP Server implementation.
   """

   def __init__(self, delegateFactory, keyFile, certFile):
      """
         parms:
            delegateFactory::
               [callable<>] function that returns a delegate DataHandler
               for a new connection.  This will actually be the final producer
               and consumer of data passed through an @SSLDataHandler.
	    keyFile::
	       [string] name of the SSL private key file
	    certFile::
	       [string] name of the SSL certificate file
      """

      self.__delegateFactory = delegateFactory
      self.__shutdown = False
      self.__keyFile = keyFile
      self.__certFile = certFile

   def handleConnect(self, connection):
      connection.dataHandler = \
	 SSLDataHandler(self.__delegateFactory(), self.__keyFile, 
                        self.__certFile,
                        server=True)

   def shutdown(self):
      self.__shutdown = True

   def readyToClose(self):
      return self.__shutdown
