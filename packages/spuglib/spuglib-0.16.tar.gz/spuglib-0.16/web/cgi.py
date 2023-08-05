#==============================================================================
#
#  $Id: cgi.py 1056 2006-08-23 23:06:34Z mike $
#
"""
   Universal CGI classes and functions.
"""
#
#  Copyright (C) 1999 Michael A. Muller
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
#  $Log: cgi.py,v $
#  Revision 1.5  2005/10/14 11:17:26  mike
#  Added cookies to CGIRequest
#
#  Revision 1.4  2000/05/17 23:44:39  mike
#  doc fixes.
#
#  Revision 1.3  1999/12/22 01:30:40  mike
#  Added option "response" paramater to CGIManager.process() to make it more
#  friendly to non-persistent cgi apps.
#
#  Revision 1.2  1999/10/09 18:50:59  mike
#  Added encodeString() method and fixed string decoding bug (wasn't converting
#  spaces from '+')
#
#  Revision 1.1.1.1  1999/08/13 23:14:48  mike
#  spug-html package
#
#
#==============================================================================

import string, re, threading, os
try:
   # python2
   from types import ListType
except ImportError:
   ListType = list
import html

from io import StringIO

class CGIRequest:
   """
      This is just a bundle of the parameters in a CGI request.
      Public variables:
      *args*::
         Argument list of the original CGI command.
      *env*::
         Environment of the original CGI command (a dictionary).
      *query*::
         Query parameters of the original CGI command parsed into a
         dictionary.
      *path*::
         The CGI command path info, broken up into a list.  Path info
         is the URL path that follows the command name.  If the URL
         is `"http://somehost/cgi-bin/cgipdisp/service/name"`, then this
         variable would contain ['service', 'name'].
      *cookies*::
         A dictionary mapping cookie names to values.
   """
   
   def __init__(self, args, env, query, path, cookies = None):
      self.args = args
      self.env = env
      self.query = query
      self.path = path
      self.cookies = cookies or {}

class CGIResponse:
   
   """
      This is another bundle of attributes designed to deliver a response
      to the client.
      
      Public variables:
      
      *out*::
         The cgi output stream.
         service = args[1]
   """

   def __init__(self, out):
      self.out = out
      self.__headersWritten = 0
      self.__contentType = ''

   def writeHeaders(self, contentType = 'text/html', otherHeaders = []):
      """
         Writes the headers if they have not already been written.
         
         The "Content-type" header is the only one that is always written.
         If any other headers are desired, they may be added in the
         /otherHeaders/ list, which should be a list of string headers
         with their associated values but no line terminators.
      """
      if not self.__headersWritten:
         self.__headersWritten = 1
         self.__contentType = contentType
         self.out.write('Content-type: %s\n' % contentType)
         self.out.write('\n'.join(otherHeaders))
         self.out.write('\n\n')
   
   def headersWritten(self):
      return self.__headersWritten
   
   def getContentType(self):
      """
         Returns the content type string of the output stream.  If the
         headers have not been written, this will be an empty string.
      """
      return self.__contentType

class _ModuleInfo:
   
   """
      A utility class for CGIManager, which is used to record information
      on a python module that has been loaded into the system so that it
      can be reloaded when appropriate.
   """
   
   def __init__(self, mod, mtime):
      self.mod = mod
      self.mtime = mtime

class CGIManager:

   """
      This class is intended to serve as the basic implementation of
      a CGI _dispatcher_.  It routes a @CGIRequest to python objects and
      modules that service the request.
      
      This class uses the path information associated with the request
      to determine how the request is routed.  If there is no path info
      associated with the request, the @defaultHandler() method is called.

      If the first component of the path is an object stored in the managers
      object dictionary, the request goes to the object. If the object is a
      @CGIObject, the rest of the path information is ignored and the
      object's processRequest() method is called.  For any other kind of
      object, if there is a second path component, the manager will attempt
      to call a method of that name on the object.  If there is no second
      path component, the object /itself/ will be called.

      If the first component is not an object stored in the manager, the
      manager checks to see if there is a python module in the current
      working directory of that name.  In this case, there must be a second
      path component and it is the function that is called within the
      module. The module will be reloaded if its file has been changed since
      the last time that it was loaded, making the CGIManager very well
      suited to interactive debugging.

      All functions and methods (including processRequest()) that are
      provided to the manager must accept the following argument list:

      /manager/::
         The CGIManager instance that is initiating the call.
      /request/::
         The @CGIRequest object.
      /response/::
         The @CGIResponse object.
      
      The CGIManager can be used within the context of stand-alone CGI
      programs, but it is really designed to be housed in a running process
      into which smaller cgi programs can feed it requests, either through
      distributed object method invocations or some other means.
      
   """

   def __init__(self):
      self.__lk = threading.Lock()
      self.__objects = {}
      self.__modules = {}

   def process(self, request, response = None):
      self.__lk.acquire()
      try:

         # if the caller didn't provide one, create a response object that can 
         # be sent back to the client process
         if response is None:
            response = CGIResponse(StringIO())

         # if there was no path info after the script, go to the default
         # handler
         if not request.path:
            self.defaultHandler(request, response)

         # if there request names an object in the dictionary, this should
         # be a method on that object.
         elif request.path[0] in self.__objects:
         
            obj = self.__objects[request.path[0]]

            # if the object is a CGIObject, the request is not a method 
            # invocation, but rather is to be delivered to the object's
            # processRequest() method.
            if isinstance(obj, CGIObject):
               obj.processRequest(self, request, response)
            
            # otherwise, do a method invocation
            else:
            
               # if there was a method specified, the function that we will
               # call is the method, otherwise we just assume that this is
               # a callable object and go ahead and call it.
               if len(request.path) > 1:
                  func = getattr(obj, request.path[1])
               else:
                  func = obj
               func(self, request, response)
         
         # if the request names a python script in the current directory, 
         # make sure that we have the latest version of the script loaded
         # and execute a function within the script.
         elif request.path[0] in self.__modules or \
              os.path.exists(request.path[0] + '.py'):
            mod = self.__loadModule(request.path[0])
            getattr(mod, request.path[1])(self, request, response)
         
         # if all else fails, complain
         else:
            self.error(request, response)
         
         # return the response object
         return response
                     
      finally:
         self.__lk.release()

   def defaultHandler(self, request, response):
      
      response.out.write("""Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<html> 
<body>
   <h1>Usage Error</h1>
   <p>The URL provided doesn't do anything useful.
</body>
</html>
""")

   def addObject(self, key, val):
      self.__objects[key] = val

   def removeObject(self, key):
      del self.__objects[key]

   def test(self, request, response):

      response.writeHeaders()
      response.out.write(
html.doc( 
   html.h1('Successful Test!!'),
   html.p('This was entirely gratifying'),
   html.p(html.a('first window', href = 'makeWindow'))
   )
      )

   def error(self, request, response):
      
      response.writeHeaders()
      response.out.write(
         html.doc( 
            html.h1('Error'),
            html.p('The command "%s" does not exist.' % 
                    string.join(request.path, '/')
                   ),
            )
         )

   def __loadModule(self, moduleName):
      st_mode, st_ino, st_dev, st_nlink, st_uid, st_gid, st_size, st_atime, \
      st_mtime, st_ctime = os.stat(moduleName + '.py')
      if moduleName not in self.__modules:
         ctx = {}
         exec("import %s; mod = %s" % (moduleName, moduleName), ctx)
         mod = self.__modules[moduleName] = _ModuleInfo(ctx['mod'], st_mtime)
      elif st_mtime > self.__modules[moduleName].mtime:
         mod = self.__modules[moduleName]
         mod.mod = reload(mod.mod)
         mod.mtime = st_mtime
      else:
         mod = self.__modules[moduleName]
      return mod.mod

class CGIObject:
   
   """
      This is an abstract base class for objects that implement the
      processRequest() method.  When requests are sent to these objects,
      the processRequest() method is always called and it is up to the
      derived class to process the request.
   """
   
   def processRequest(self, manager, request, response):
      """
         Called whenever a request is sent to the object.  /manager/
         is the CGIManager instance, /request/ is a @CGIRequest instance,
         and /response/ is a @CGIResponse instance.
      """
      raise ImplementedBySubclassError()


def _fixEscape(escape):
   if escape.group(1):
      return chr(int(escape.group()[1:], 16))
   else:
      return ' '

class ParseError(Exception):
   """Raised when something in the request cannot be parsed."""

def parseCookies(cookieStr):
   """
      Parses the cookies out of the cookie header value.  Returns them in a
      dictionary.
      
      Raises ParseError if the cookie is unparseable.
   """
   _parmRx = \
       re.compile(r'\s* ( (?P<name>[^\s=]+) = '
                   r'     ( < (?P<val0>[^>]*) > | '
                   r'       " (?P<val1>[^"]*) " | '
                   r'         (?P<val2>[^<"][^;]*) )'
                   r'|([^;]))\s*(;|$)',
                  re.X
                  )
   cookies = {}
   while cookieStr:
      m = _parmRx.match(cookieStr)
      if m:
         if m.group('name'):
            cookies[m.group('name')] = \
               m.group('val0') or m.group('val1') or m.group('val2') 
         cookieStr = cookieStr[m.end():]
      else:
         raise ParseError('bad cookie')

   return cookies

_escapeRx = re.compile(r'(%[0-9A-Fa-f]{2})|\+')
_parmRx = re.compile(r'([^=]+)=(.*)')

def parseQuery(queryString, valsAlwaysLists=False):
   """
      Parses a CGI query string and returns a dictionary containing its
      values.
      
      parms:
         valsAlwaysLists: [bool] If true, parameter values are always lists of 
            strings.  If false, single value parameters are just stored as 
            strings.
   """
   dict = {}
   if not queryString:
      return dict
   vars = queryString.split('&')
   for var in vars:
      m = _parmRx.match(var)
      if not m:
         raise ValueError('Badly formed variable definition in query parms:'
                           ' %s' % repr(var)
                          )
      var = m.group(1)
      val = m.group(2)
      val = _escapeRx.sub(_fixEscape, val)
      if valsAlwaysLists:
         dict.setdefault(var, []).append(val)
      else:
         # check for an existing value, wrap existing single values in a list 
         # and append to them
         if var in dict:
            if type(dict[var]) is ListType:
               dict[var].append(val)
            else:
               dict[var] = [ dict[var], val ]
         else:
            dict[var] = val
   return dict

def getRequest(env, args, src = None):
   """
      Returns a @CGIRequest from the dictionary /env/.  /env/ should 
      contain the standard CGI environment variables.
      
      if /src/ is provided, it should be a file object (usually the CGI
      program's standard input stream) from which to parse query parameters
      that have come in through a form's "POST" method.
      
      /args/ should be the CGI command's argument list.      
      
      The following variables are currently used if they exist:
      /`PATH_INFO`/::
         Additional path info added after the cgi program name.
      /`QUERY_STRING`/::
         A string containing the standard CGI representation of
         query parameters.
   """
   if 'PATH_INFO' in env:
      path = env['PATH_INFO'][1:].split('/')
   else:
      path = []
   
   if 'QUERY_STRING' in env:
      query = parseQuery(env['QUERY_STRING'])
   else:
      query = {}
   
   if src:
      data = src.read()
      query.update(parseQuery(data))
   
   return CGIRequest(args, env, query, path)

_unsavoryRx = re.compile(r'[^A-Za-z0-9]')
def _encodeMatch(m):
   return '%%%02x' % ord(m.group())

def encodeString(str):
   """
      Encodes a text string, converting all of the unsavory characters
      to the officially sanctioned '%' escape sequences.
   """
   return _unsavoryRx.sub(_encodeMatch, str)
