#==============================================================================
#
"""
    Mike's gateway interface.
    
    Hopefully a better interface for webservers than WSGI.
"""
#
#   Copyright (C) 2009 Michael A. Muller
#
#   This file is part of spuglib.
#
#   spuglib is free software: you can redistribute it and/or modify it under
#   the terms of the GNU Lesser General Public License as published by the
#   Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   spuglib is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with spuglib.  If not, see <http://www.gnu.org/licenses/>.
#
#==============================================================================

import copy, os, re, sys, weakref
from StringIO import StringIO
# trickery to force the import of python's cgi module
py_cgi = __import__('cgi')
from spug.util import log
import cgi

class Request:
    """
        Represents a processed HTTP request.  Also includes the code to 
        write a response.

    Public-vars
        args: [list<str>] Argument list of the original CGI command.
        contents: [RequestContents or None] the body of the request.  If the 
            body of the request was just application/x-www-form-urlencoded,
            this will not be filled in: rather the data will have been parsed 
            and added to 'query'.
        cookies: [dict<str, str>] A dictionary mapping cookie names to values.
        path: [list<str>] The CGI command path info, broken up into a list.  
            Path info is the URL path that follows the command name.  If the URL 
            is `"http://somehost/cgi-bin/cgipdisp/service/name"`, then this 
            variable would contain ['service', 'name'].
        query: [dict<str, list<str>>] Query parameters of the original CGI 
            command parsed into a dictionary.
        hostName: [str] the host name portion of the URL.  This could be an IP 
            address.
        port: [int] the server port number.
        scriptName: [str] the path portion of the url before the start of the 
            path info.
        method: [str] the HTTP method.  Usually "GET" or "POST".
        session: [any or None] if present, this is an object identifying the 
            session.  The type of the object used is left to be defined by the 
            framework, this attribute is just a placeholder provided for 
            convenience.
        user: [any or None] if present, this is an object identifying the user.  The 
            exact type of object that is used to identify the user is left to 
            be defined by the framework.  This attribute is just a placeholder 
            provided as a convenience.
        ssl: [any or None] if present, this is an object indicating 
            information about the SSL connection.  If None, the request came 
            from a non-ssl encrypted channel.
        out: [file.write] the raw output stream.  This should generally not be 
            used directly, use the write*() methods instead.  It is public to 
            allow gateways to access it in a returned response.
        bag: [dict<class, any>] this is a dictionary where you can store 
            whatever you want.  It is intended for use with request processors 
            in a chain that need to pass information along with the request.  
            In order to provide a unique namespace, it is recommended that the 
            keys in this dictionary be class objects.
    """
    
    def __init__(self, out, args, query, hostName, port, scriptName, path, ssl,
                 contents, 
                 cookies = None,
                 session = None,
                 user = None,
                 method = None
                 ):
        """
            parms:
                (see Public-vars)
        """
        self.out = out
        self.args = args
        self.query = query
        self.hostName = hostName
        self.port = port
        self.scriptName = scriptName
        self.path = path
        self.ssl = ssl
        self.contents = contents
        if contents:
            contents.req = weakref.proxy(self)
        self.cookies = cookies or {}
        self.session = session
        self.user = user
        self.method = method
        self.bag = {}
        self.__contentType = None
        self.__headersWritten = False
        self.__extraHeaders = {}
    
    def __getstate__(self):
        d = self.__dict__.copy()
        if self.contents:
            d['contents'] = contents = copy.copy(self.contents)
            contents.req = None
        return d
    
    def __setstate__(self, state):
        self.__dict__ = state
        if self.contents:
            self.contents.req = weakref.proxy(self)
    
    def setHeader(self, header, value):
        """
            Sets a header to the specified value.  This must be called before 
            the headers are written.
        """
        assert not self.__headersWritten
        self.__extraHeaders[header] = value
    
    def writeHeaders(self, contentType = 'text/html', contentLength = None,
                     otherHeaders = {}
                     ):
        """
            Writes the headers if they have not already been written.
           
            The "Content-type" header is the only one that is always written.
            "Content-Length" is common enough to merit its own keyword 
            argument. If any other headers are desired, they may be added in 
            the /otherHeaders/ list, which should be a list of string headers 
            with their associated values but no line terminators.
           
            parms:
                contentType: [str] content mime type.
                contentLength: [int or None] length of the content in bytes.
            
        """
        if not self.__headersWritten:
            self.__headersWritten = True
            self.__contentType = contentType
            self.out.write('Content-type: %s\n' % contentType)
            for header, val in self.__extraHeaders.iteritems():
                self.out.write('%s: %s' % (header, val))
            for header, val in otherHeaders.iteritems():
                self.out.write('%s: %s' % (header, val))
            self.out.write('\n\n')

    def write(self, data):
        """
            Writes data to the output stream.  If the headers have not been 
            written, they will be written automatically.  Content-type will be 
            set to 'text/html' and content-length will not be defined.
            
            parms:
                data: [str] the data to write
        """
        if not self.__headersWritten:
            self.writeHeaders()
        self.out.write(data)

    def writeAll(self, parcel, contentType = 'text/html'):
        """
            Write an entire response with headers to the output stream.
            
            This must not be called if the headers or any data have already 
            been written.
            
            parms:
                parcel: [str] the complete response contents.
                contentType: [str] contents mime type.
        """
        assert not self.__headersWritten
        self.writeHeaders(contentType = contentType,
                          contentLength = len(parcel)
                          )
        self.write(parcel)
    
    def writeRedirect(self, url):
        """
            Writes a complete redirect message.
            
            Nothing else must have been written.
            
            parms:
                url: [str] the url to redirect to.
        """
        assert not self.__headersWritten
        # XXX this will work for CGI, but not for direct HTTP
        self.out.write('Location: %s\n\n' % url)
   
    def headersWritten(self):
        """
            Returns True if the headers have been written.
        """
        return self.__headersWritten
   
    def getContentType(self):
        """
            Returns the content type string of the output stream.  If the
            headers have not been written, this will be None.
        """
        return self.__contentType
    
    def encapsulate(self):
        """
            Encapsulates the request by pulling in all external dependencies 
            so that the request can be marshalled and transmitted.  In order 
            to do request marshalling, stdout must be a StringIO object (or 
            some other file-like object that can be pickled).  cStringIO 
            objects can not be pickled.
        """
        if self.contents:
            self.contents.encapsulate()
    
    def _self(self):
        """Test support method, returns self."""
        return self
    
    def makeBaseURL(self):
        """
            Returns the 'http://host:port' portion of the url.
        """
        if self.ssl and self.port == 443 or \
           not self.ssl and self.port == 80:
            port = ''
        else:
            port = ':%s' % self.port
        return 'http%s://%s%s' % (self.ssl and 's' or '', self.hostName, port)
    
    def makeURL(self, *path, **options):
        """
            Make a URL off the script name for the specified path.
            
            parms:
                path: [*str] set of path components.
                options: [dict<str, any>] additional options.  Currently 
                    supported are:

                    full: [bool] if true, construct the complete URL 
                        (including the protocol descriptor, hostname and 
                        possibly port number).  By default, this just returns 
                        the path.

        """
        # make sure all of the options are what we expect
        for opt in options:
            if opt not in ('full',):
                raise ValueError('Unsupported option %s' % opt)
                           
        path = '%s/%s' % (self.scriptName, '/'.join(path))
        if options.get('full'):
            return self.makeBaseURL() + path
        else:
            return path
    
    def clear(self):
        """
            Clear all of the fields that have arbitrary contents.  This is 
            useful when a request object is passed back through a gateway 
            where the client may not be able to access object types that are 
            internal to the server.
        """
        self.bag = {}
        self.user = None
        self.session = None
        self.ssl = None

class RequestContents:
    """
        This is yet another class for accessing the raw contents of a request.
        It is similar in concept to cgi.FieldStorage.        
    """
    
    __headerRx = re.compile(r'([^\s:]+):\s*(.*\s)?\s*')
    __indentRx = re.compile(r'\s+\S')
    
    def __init__(self, contentLength, contentType, contentTypeParams, src,
                 contentDisp = None,
                 contentDispName = None,
                 contentDispFilename = None
                 ):
        self.req = None
        self.contentLength = contentLength
        self.contentType = contentType
        self.boundary = contentTypeParams.get('boundary')
        self.src = src
        self.contentDisp = contentDisp
        self.contentDispName = contentDispName
        self.contentDispFilename = contentDispFilename
    
    def __iter__(self):
        """
            Iterate over the contents of a multipart content.  Iteration will 
            return objects of type RequestContents.  Form data objects will 
            automatically be merged into the query parameters of the request 
            (in addition to being returned).
        """
        
        if self.contentType == 'multipart/form-data':
            while True:
                # read the next section of the file

                headers = {}
                lastHeader = None
                reader = _MultipartReader(self.src, self.boundary)
                gotLines = False
                
                while True:
                    line = reader.readline()
                    if not line:
                        # it might just be an empty section (like the one 
                        # caused at the beginning of multipart contents by the 
                        # leading boundary).  If there really is no more data, 
                        # we're done.
                        if not gotLines and reader.hardEOF:
                            break
                        else:
                            reader = _MultipartReader(self.src, self.boundary)
                            continue
                    
                    # check for a header
                    m = self.__headerRx.match(line)
                    if m:
                        header = m.group(1).lower()
                        headers[header] = m.group(2)
                        lastHeader = header
                    
                    # check for a continuation
                    elif self.__indentRx.match(line) and lastHeader:
                        headers[header] += line.strip()
                    
                    # check for the blank line   
                    elif not line.strip():
                        break
                    
                    # report and ignore
                    else:
                        log.error('Invalid line found in headers: %s' %
                                   repr(line)
                                  )
                
                # check for end of file
                if not line:
                    break
                
                # process content length
                try:
                    contentLength = int(headers['content-length'])
                except (ValueError, KeyError):
                    contentLength = None
                
                try:
                    contentType, contentTypeParmams = \
                        py_cgi.parse_header(headers['content-type'])
                except (ValueError, KeyError):
                    contentType = None
                    contentTypeParams = {}
                
                # check for form data
                contentDisp = contentDispName = contentDispFilename = None
                try:
                    contentDisp, dispParams = \
                        py_cgi.parse_header(headers['content-disposition'])
                    if contentDisp == 'form-data':
                        contentDispName = dispParams['name']

                        # if this is a file, get me out of here
                        if 'filename' in dispParams:
                            contentDispFilename = dispParams['filename']
                            raise ValueError

                        # this is a form field.  Read the contents and replace 
                        # it with a StringIO object
                        fieldValue = reader.read()
                        reader = StringIO(fieldValue)
                        
                        # remove trailing (cr)lf
                        if fieldValue.endswith('\r\n'):
                            fieldValue = fieldValue[:-2]
                        elif fieldValue.endswith('\n'):
                            fieldValue = fieldValue[:-1]
                        
                        # add the value to the existing values
                        values = self.req.query.get(contentDispName)
                        if values:
                            values.append(fieldValue)
                        else:
                            self.req.query[contentDispName] = [fieldValue]
                except (ValueError, KeyError):
                    pass

                yield RequestContents(contentLength, contentType, 
                                      contentTypeParams,
                                      reader,
                                      contentDisp = contentDisp,
                                      contentDispName = contentDispName,
                                      contentDispFilename = 
                                          contentDispFilename,
                                      )
    
    def encapsulate(self):
        """Convert the source stream to a StringIO object."""
        data = self.src.read(self.contentLength)
        self.src = StringIO(data)

class _MultipartReader:
    """
        Implements a file-like read interface that only reads to the next 
        boundary.
    """
    
    def __init__(self, src, boundary):
        self.__src = src
        self.__boundary = boundary
        self.__boundaries = ('--' + self.__boundary,
                             '--%s--' % self.__boundary
                             )
        assert len(boundary) < 1024 # large boundaries break the read
        
        # lines buffered (these aren't necessarily lines, we truncate them at 
        # 1024 chars - check for a newline at the end)
        self.__lines = []
        
        # number of bytes buffered
        self.__bytes = 0
        
        # true if we've read to the end of file or the boundary
        self.__eof = False
        
        # true if the end of file was due to an end-of-file in the enclosing 
        # stream
        self.hardEOF = False

    def __readLimitedLine(self):
        """
            Read up until the next newline or chunk size and add it to the 
            buffer.
        """
        if self.__eof: return

        line = self.__src.readline(1024)

        if not line or line.strip() in self.__boundaries:
            self.__eof = True
            self.hardEOF = not line
            return
    
        self.__lines.append(line)
        self.__bytes += len(line)

    def __read(self, size):
        """Read from the file until end of file or bytes buffers >= size."""
        while self.__bytes < size and not self.__eof:
            self.__readLimitedLine()
    
    def __getLine(self):
        """
            Return the next line from the buffer, reading it from the file if 
            necessary.
        """
        if not self.__lines:
            self.__readLimitedLine()
        if not self.__lines:
            return None
        line = self.__lines.pop(0)
        self.__bytes -= len(line)
        return line
    
    def __putBack(self, line):
        """Put a line or line fragment back into the buffer."""
        self.__lines.insert(0, line)
        self.__bytes += len(line)

    def read(self, size = None):
        """
            Normal file-like read function.  Read up to size byte or the 
            entire file if size is None.
        """
        if size is None:
            # read the entire file contents into the buffer
            amt = 1024
            while not self.__eof:
                self.__read(amt)
                amt *= 2
            
            # grab all of the lines in the buffer and return them as a big blob
            data = ''.join(self.__lines)
            self.__lines = []
            self.__bytes = 0
            return data
        else:
            # read until we have enough data
            self.__read(size)
            
            # build a "scoop" list that will contain enough of the buffer list 
            # to constitute the requested size
            scoop = []
            count = 0
            while count < size and self.__lines:
                
                # if the next line is less than the size limit, just tranfer it
                line = self.__getLine()
                if count + len(line) <= size:
                    scoop.append(line)
                else:
                    # it's greater - we need to split it and return a portion 
                    # of it to the buffer list
                    portion = size - count
                    scoop.append(line[:portion])
                    self.__putBack(line[portion:])

            return ''.join(scoop)
    
    def readline(self):
        result = []
        while not result or result[-1][-1] != '\n':
            nextLine = self.__getLine()
            if not nextLine:
                break
            result.append(nextLine)
        return ''.join(result)

def getCGIRequest(env = os.environ, args = sys.argv, stdin = sys.stdin, 
                  stdout = sys.stdout
                  ):
    """
        Returns a @Request object created from the standard CGI parameters.
        
        Expectations of the parameters are as defined by the CGI specification.
        
        parms:
            env: [dict<str, str>] Environment variables.
            args: [list<str>] the argument list.
            stdin: [file.read] the process standard input.
            stdout: [file.write] the process output stream.
    """

    try:
        path = env['PATH_INFO'][1:].split('/')
    except KeyError:
        path = []

    try:
        query = cgi.parseQuery(env['QUERY_STRING'], valsAlwaysLists=True)
    except KeyError:
        query = {}
    
    try:
        hostName = env['SERVER_NAME']
    except KeyError:
        hostName = ''
    
    try:
        port = env['SERVER_PORT']
    except KeyError:
        port = 80
    
    try:
        script = env['SCRIPT_NAME']
    except KeyError:
        script = ''
    
    try:
        method = env['REQUEST_METHOD']
    except KeyError:
        method = ''
    
    # XXX I think this only works for apache
    try:
        ssl = env['HTTPS'] == 'on'
    except KeyError:
        ssl = None
    
    try:
        cookies = cgi.parseCookies(env['HTTP_COOKIE'])
    except KeyError, cgi.ParseError:
        cookies = None
    
    # process the request contents.
    try:
        contentLength = int(env['CONTENT_LENGTH'])
    except (KeyError, ValueError), ex:
        contentLength = 0
    
    # the request contents, which will either be None or an instance of 
    # RequestContents
    contents = None
    if contentLength:    
        try:
            contentType, contentTypeParams = \
                py_cgi.parse_header(env['CONTENT_TYPE'])
        except KeyError:
            contentType = None
            contentTypeParams = {}

        # check for form data - process it into query if we've got it.
        if contentType == 'application/x-www-form-urlencoded':
            # XXX what if we run out of data or hang?
            for key, val in \
                cgi.parseQuery(stdin.read(contentLength), 
                               valsAlwaysLists=True).iteritems():

                curVal = query.get(key)
                if curVal:
                    curVal.extend(val)
                else:
                    query[key] = val
        else:
            contents = RequestContents(contentLength, contentType, 
                                       contentTypeParams,
                                       stdin
                                       )

    return Request(stdout, args, query, hostName, port, script, path, ssl,
                   contents,
                   cookies = cookies,
                   method = method
                   )
