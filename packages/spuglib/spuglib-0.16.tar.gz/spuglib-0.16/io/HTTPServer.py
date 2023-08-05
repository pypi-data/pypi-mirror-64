#==============================================================================
#
#  $Id$
#
"""
   Proactor based HTTP server implementation.
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

import re
from io import StringIO
import six
from spug.io.proactor import DataHandler, ConnectHandler
from spug.util.log import debug
from spug.web import cgi

class Headers:
    """Stores HTTP Headers."""
    
    def __init__(self):
        self.__vals = []
    
    def add(self, header, val):
        self.__vals.append((header, val))
    
    def addToLast(self, contents):
        """
            Add contents (a continuation line) to the value of the last header.
        """
        self.__vals[-1] = (self.vals[-1][0], self.vals[-1][1] + contents)
    
    def __getitem__(self, header):
        """Returns the value of the first matching header."""
        for hdr, val in self.__vals:
            if header == hdr:
                return val
        raise KeyError(header)
    
    def get(self, header, default = None):
        for hdr, val in self.__vals:
            if header == hdr:
                return val
        else:
            return default
    
    def writeTo(self, out):
        for hdr, val in self.__vals:
            out.write('%s: %s\r\n' % (hdr, val))
    
    def __str__(self):
        out = StringIO()
        self.writeTo(out)
        return out.getvalue()

    def __setitem__(self, header, val):
        """
            Replaces the first instance of the header with the new value or 
            adds the new value to the list.
        """
        for i in range(len(self.__vals)):
            if self.__vals[i][0] == header:
                self.__vals[i] = (header, val)
                break
        else:
            self.add(header, val)
    
    def iterAll(self, header):
        """Returns a generator for the values of all matching headers."""
        return (val for hdr, val in self.__vals if hdr == header)

class RequestHandler:
   """
      (Mostly) abstract interface for a request handler.  This very closely
      follows the interface for @spug.io.proactor.DataHandler, except that it
      doesn't follow the peek\/get paradigm.  The HTTPDataHandler will call
      @get() to pull data for peek and hold it until the subsequent get.
   """

   def __init__(self):
      pass

   def readyToGet(self):
      raise NotImplementedError()

   def readyToPut(self):
      return False

   def get(self, size):
      raise NotImplementedError()

   def put(self, data):
      """
         Puts data into the handler.  This will only be called for the post 
         method, and then for only as much data as is in the "content-length"
         header.  If there is no content-length header, it will be called 
         until the close of the connection.
      """
      raise NotImplementedError()

   def readyToClose(self):
      raise NotImplementedError()

   def getCode(self):
      """
         Returns the HTTP response code (an integer).  The base class
         implementation always returns 200.

         May be overriden by derived classes, usually to return an error code.
      """
      return 200

   def getMessage(self):
      """
         Returns the HTTP response message (a string).  The base class
         implementation always returns "OK".

         May be overriden by derived classes, usually to return an error
         message.
      """
      return 'OK'
   
   def emitStatusLine(self):
      """
         If true, the connection's DataHandler will write the initial HTTP 
         status line upon receipt of the request and headers from the client.
         
         Returns true by default.
      """
      return True

class BufferedResponseHandler(RequestHandler):
   """
      A request handler that works nicely for pages that are small enough to
      be stored in an buffer in memory (so pretty much anything).  You should
      avoid using it for pages that need to be read from disk (or any other
      device) because these should really be dealt with as an object in the
      proactor.
   """

   def _generateResponse(self, contents, contentType = 'text/html', 
                         headers = {}
                         ):
      """
         Convenience method for creating a string containing all of the
         headers and the body of the response.

         parms:
            contents::
               [string] the contents (parcel) of the page
            contentType::
               [string] content mime type
            headers::
               [dict<string, string>] Additional HTTP 
               response headers. Mapping from header name to value.
      """

      # format all of the extra headers
      headers = \
         '\r\n'.join(['%s: %s' % (hdr, val) for hdr, val in headers.items()])

      return 'Content-type: %s\r\nContent-length: %d\r\n%s\r\n%s' % \
             (contentType, len(contents), headers, contents)

   def __init__(self, output):
      """
         Constructs the request handler from the entire output buffer.

         parms:
            output::
               [string]
      """
      self.__buffer = output

   def readyToGet(self):
      if self.__buffer: return True

   def get(self, size):
      data = self.__buffer[:size]
      self.__buffer = self.__buffer[size:]
      return data

   def put(self, data):
      raise NotImplementedError()

   def readyToClose(self):
      return not self.__buffer

class BasicErrorHandler(BufferedResponseHandler):

   def __init__(self, errorCode, errorMsg):
      self.code = errorCode
      self.msg = errorMsg

      # construct the output contents
      contents = '<html><head><title>%(code)s - %(msg)s</title></head>' \
         '<body><h1>%(code)s - %(msg)s</h1></body></html>' % \
         { 'code': errorCode, 'msg': errorMsg }
      response = self._generateResponse(contents)
      BufferedResponseHandler.__init__(self, response)

class HTTPCGIAdapter(RequestHandler):
   """
      Serves as a RequestHandler for spug.web CGI objects.
   """

   # handler states
   READING = 0
   PROCESSING = 1
   WRITING = 2

   def __init__(self, req, manager):
      """
         parms:
            req::
               [@Request] The HTTP request.
            manager::
               [@spug.web.cgi.CGIManager] the CGI manager to receive the
               request.  Actually, this need not be a CGIManager, but can be
               any object that implements process(CGIRequest, CGIResponse)
      """
      self.__req = req
      self.__inputBuffer = ''
      self.__handler = manager
      self.__outputBuffer = None
      debug('servicing %s request with headers %s' % 
             (req.method, req.headers)
            )
      if req.method in ('POST', 'PUT'):
         # if we're posting, we'll want to read more data from the connection
         # hopefully, they will provide a "content-length" header to tell us
         # how much to read.  If not, we cap the input at 64K
         try:
            self.__inputSize = int(req.headers.get('content-length', ''))
         except ValueError:
            self.__inputSize = 0x10000
         debug('  expecting %d bytes of POST input' % self.__inputSize)
         self.__state = self.READING
      else:
         self.__inputSize = 0

         # process the request
         self.__process()

   def __process(self):

      # split the request into the query and the path
      path = self.__req.path[1:].split('/')
      parms = path[-1].split('?')
      if len(parms) > 1:
         path = path[:-1] + [parms[0]]
         parms = ['?'.join(parms[1:])]
         queryStr = parms[0]
      else:
         parms = []
         queryStr = ''

      # construct input stream from the input buffer
      src = StringIO(self.__inputBuffer)

      # create the request (this is really ass-backwards)
      req = cgi.getRequest({'PATH_INFO': '/' + '/'.join(path),
                            'QUERY_STRING': queryStr
                            }, 
                           parms, 
                           src
                           )

      # parse the cookies
      req.cookies = {}
      for cookieHeader in self.__req.headers.iterAll('cookie'):
          req.cookies.update(cgi.parseCookies(cookieHeader))

      # create a response object with a stream to write to
      outputStream = StringIO()
      resp = cgi.CGIResponse(outputStream)

      # pass it on to the handler
      self.__handler.process(req, resp)

      # store the output
      self.__outputBuffer = outputStream.getvalue()

      self.__state = self.WRITING

   def readyToPut(self):
      return len(self.__inputBuffer) < self.__inputSize

   def put(self, data):
      debug('got POST data: %s' % repr(data))
      self.__inputBuffer += data
      if len(self.__inputBuffer) >= self.__inputSize:
         debug('POST input filled: processing')
         self.__state = self.PROCESSING
         self.__process()

   def readyToGet(self):
      return self.__state == self.WRITING

   def get(self, size):
      assert self.__state == self.WRITING
      data = self.__outputBuffer[:size]
      self.__outputBuffer = self.__outputBuffer[size:]
      return data

   def readyToClose(self):
      return self.__state == self.WRITING and not self.__outputBuffer

class HandlerResolver:
   """
      Interfaces for classes that return instances of @RequestHandler's
   """

   def getRequestHandler(self, request):
      """
         Returns a @RequestHandler for the given request.

         Must be implemented by derived classes.
         
         parms:
            request: [@Request]
      """
      raise NotImplementedError()

   def getErrorHandler(self, error, errorMsg):
      """
         Returns a @RequestHandler to serve the given error code and message.

         Must be implemented by derived classes.

         parms:
            error::
               [int] HTTP error code
            errorMsg::
               [string] error text to display prominently.
      """
      return BasicErrorHandler(error, errorMsg)

class Request:
   """
      Public-vars:
         method::
            [string] The HTTP method (GET, PUT ...)
         path::
            [string] the resource path (as obtained from the request line)
         headers::
            [dict<string, string>] the request headers.  Header names are
            converted to lower case.
   """

   def __init__(self, method, path, version):
      self.method = method
      self.path = path
      self.headers = Headers()
      self.version = version

   def setHeader(self, header, value):
      """
         Sets the header to the value in the 'headers' dict, doing case
         normalization on the header.

         parms:
            header::
               [string]
            value::
               [string]
      """
      self.headers[header.lower()] = value

class HTTPDataHandler(DataHandler):

   INIT = 0
   GOT_FIRST_LINE = 1
   GOT_HEADERS = 2
   GOT_REQUEST = 3

   def __init__(self, handlerResolver):
      self.__buffer = b''
      self.__outBuffer = b''
      self.__state = self.INIT
      self.__handler = None
      self.__resolver = handlerResolver
      
      # remaining bytes of post data (initialized from content-length header)
      self.__postBytesRemaining = 0
      
      # set to true when the client has requested a close.
      self.__closeRequested = False

   def readyToPut(self):
      return self.__state < self.GOT_REQUEST or \
         self.__handler and self.__handler.readyToPut()

   def readyToGet(self):
      result = self.__state == self.GOT_REQUEST and \
         (self.__outBuffer or self.__handler.readyToGet())
      return result

   __headerRx = re.compile(r'(\S+):\s*(.*)')
   def __handleHeaderLine(self, line):
      line = six.ensure_str(line)

      # if the line ended with CRLF, store the fact that we want to use CRLF
      # in the responses
      if line[-1:] == '\r':
         self.__useCRLF = True
         line = line[:-1]

      if self.__state == self.INIT:
         # process the first line
         fields = line.split()
         if len(fields) == 3:

            # HTTP 1.0/1.1 request
            if fields[2] in ('HTTP/1.1', 'HTTP/1.0'):
               # construct the request
               self.__request = Request(fields[0], fields[1], fields[2])
               self.__state = self.GOT_FIRST_LINE
            else:
               # bad request
               self.__handler = \
                  self.__resolver.getErrorHandler(400,
                                                  'Malformed HTTP Request'
                                                  )
               self.__state = self.GOT_REQUEST
               debug('got malformed request: %s' % repr(line))

         elif len(fields) == 2:

            # HTTP 0.9 style request - we're done
            self.__request = Request(fields[0], fields[1], 'HTTP/0.9')
            self.__handler = \
               self.__resolver.getRequestHandler(self.__request)
            if self.__handler.emitStatusLine():
               self.__outBuffer = b'HTTP/1.0 %d %s\n' % \
                  (self.__handler.getCode(), self.__handler.getMessage())
            self.__state = self.GOT_REQUEST

         else:
            # more than three or less than two fields in the request line -
            # bad request
            self.__handler = \
               self.__resolver.getErrorHandler(400,
                                               'Malformed HTTP Request'
                                               )
            self.__state = self.GOT_REQUEST

      elif self.__state == self.GOT_FIRST_LINE:

         # blank line indicates the end of the headers
         if not line:
            self.__handler = \
               self.__resolver.getRequestHandler(self.__request)
            if self.__handler.emitStatusLine():
               self.__outBuffer = b'HTTP/1.1 %d %s\n' % \
                  (self.__handler.getCode(), 
                   six.ensure_binary(self.__handler.getMessage()))
            
            # set the number of post bytes
            try:
               self.__postBytesRemaining = \
                  int(self.__request.headers.get('content-length', 0))
            except ValueError:
               self.__postBytesRemaining = 0
            
            # see if a close was requested
            self.__closeRequested = \
               self.__request.headers.get('connection') == 'close'
            
            # if there is content, switch to the GOT_REQUEST state so that we 
            # can process it.  Otherwise switch back to the INIT state to get 
            # the next request.
            if self.__postBytesRemaining:
               self.__state = self.GOT_HEADERS
            else:
               self.__state = self.GOT_REQUEST
            return

         m = self.__headerRx.match(line)
         if m:
            self.__request.headers.add(m.group(1).lower(), m.group(2))
         else:
            self.__handler = \
               self.__resolver.getErrorHandler(400,
                                               'Malformed request headers'
                                               )

   def put(self, data):

      self.__buffer += six.ensure_binary(data)
      while self.__buffer:
      
         # if we've already processed the header, the data goes directly to the
         # handler.  Otherwise we process a header line.
         if self.__state == self.GOT_HEADERS:
            if len(self.__buffer) > self.__postBytesRemaining:
               data = self.__buffer[:self.__postBytesRemaining]
               self.__buffer = self.__buffer[self.__postBytesRemaining:]
            else:
               data = self.__buffer
               self.__buffer = ''
            self.__handler.put(data)
            self.__postBytesRemaining -= len(data)

            # see if we're done
            if not self.__postBytesRemaining:
               self.__state = self.GOT_REQUEST
         else:
            # we're still in the request header.  process headers one line at 
            # a time
            lines = self.__buffer.split(b'\n', 1)
            if len(lines) > 1:
               line, self.__buffer = lines
               self.__handleHeaderLine(line)
            else:
               # not enough to process - quit
               return

   def peek(self, size):
      # if more data is requested than is available and the handler is ready
      # to provide more data, pull some data from the handler
      if len(self.__outBuffer) < size and self.__handler.readyToGet():
         self.__outBuffer += \
            self.__handler.get(size - len(self.__outBuffer))
      return self.__outBuffer[:size]

   def get(self, size):
      self.__outBuffer = self.__outBuffer[size:]
      
      # if we have completely flushed the data queued up from the handler and 
      # the handler is ready to close, return to initial state.
      if not self.__outBuffer and self.__handler and \
         self.__handler.readyToClose():
         self.__state = self.INIT

   def readyToClose(self):
      return self.__closeRequested and self.__handler and \
         self.__handler.readyToClose()

class HTTPConnectHandler(ConnectHandler):

   def __init__(self, resolver):
      """
         parms:
            resolver::
               [@HandlerResolver] instance to resolve requests to request 
               handlers
      """
      self.__resolver = resolver
      self.__closed = False

   def handleConnect(self, connection):
      connection.dataHandler = HTTPDataHandler(self.__resolver)

   def readyToClose(self):
      return self.__closed
   
   def close(self):
      self.__closed = True
