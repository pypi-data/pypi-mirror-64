#==============================================================================
#
#  $Id: wof.py 1316 2008-07-20 19:33:02Z mike $
#
"""
   The Web Object Framework.  This module contains the @Node class hierarchy,
   which describes pages in a URL tree, and a set of functions for rendering
   them.
"""
#
#  Copyright (C) 2003 Michael A. Muller
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

import os, re, shutil, socket, struct, sys, threading, time, types
from urlparse import urlparse

from spug.web import cgi, htmlo, xmlo
from spug.util import StdError

from spug.nml.block import TextBlock
from spug.nml.parse import *
from spug.nml.html import *
from spug.io.LineReader import LineReader

SPUGWEB_NS = 'http://www.mindhog.net/schemas/spugweb'

# table of default extensions for a mime type
_extension = \
   {
   'text/plain': '.txt',
   'text/html': '.html',
   'image/jpeg': '.jpg',
   'image/gif': '.gif',
   'image/png': '.png',
   'text/css': '.css',
   }

_moduleTimestamp = os.path.getmtime(__file__)
_moduleTimestamps = {}

def _getModuleTimestamp(module):
   
   # built-in module has no file.
   if not hasattr(module, '__file__'):
      return 0

   file = module.__file__
   
   # get to the pyc file if we came from a compiled file
   if file[-4:] in ('.pyc', '.pyo'):
      file = file[:-1]

   # XXX this is where we should be reloading the module and regenerating
   # all of the page nodes that it uses if it has been modified since its
   # last recorded timestamp
   
   ts = _moduleTimestamps[module.__name__] = os.path.getmtime(file)
   return ts

def _getClassTimestamp(cls):
   
   # first get the class' timestamp
   ts = _getModuleTimestamp(sys.modules[cls.__module__])
   
   # now check against each of the base classes
   for base in cls.__bases__:
      ts = max(_getClassTimestamp(base), ts)
   
   return ts

def error(msg):
   print msg

class Dependency:
   """
      Abstract interface for dependents - these are anything that have 
      timestamps.
   """
   
   def getTimestamp(self, request):
      """
         Returns the timestamp of the dependent.
         
         Must be implemented by derived classes.
         
         parms:
            request: [@Request]
      """
      raise NotImplementedError()

class FileDependency(Dependency):
   """
      Simple dependent implementation that returns the timestamp of a file.
   """
   
   def __init__(self, path):
      self.__ts = os.path.getmtime(path)
   
   def getTimestamp(self, request):
      return self.__ts

class ClassDependency(Dependency):
   """
      Dependency on a class.
   """
 
   def __init__(self, cls):
      """
         parms:
            cls: [@types.ClassType or type]
      """
      self.__ts = _getClassTimestamp(cls)
   
   def getTimestamp(self, request):
      return self.__ts

class NodeContext:
   """
      This class tracks the ancestry of a @Node in the context of a request.
   """
   
   def __init__(self, node, name, parent = None):
      """
         parms:
            node::
               [@Node] the node that this context is the context for
            name::
               [string] the name of the node in this context
            parent::
               [@NodeContext] parent context
      """
      self.__node = node
      self.__name = name
      self.__parent = parent
   
   def __getitem__(self, property):
      """
         Gets the value of a property recursively, searching first the node,
	 then the immediate parent, then the grandparent, etc.  If no parent
	 defines a value for the property, a *KeyError* is raised.
      """
      if self.__node.has_key(property):
         return self.__node[property]
      elif self.__parent:
         return self.__parent[property]
      else:
         raise KeyError(property)

   def get(self, property, defaultValue = None):
      """
         Gets the value of a property recursively, returns the /defaultValue/
         if the property is not defined.
         
         parms:
            property::
               [string] property name
            defaultValue::
               [any] value to return if property is not defined
      """
      if self.__node.has_key(property):
         return self.__node[property]
      elif self.__parent:
         return self.__parent.get(property, defaultValue)
      else:
         return defaultValue

   def has_key(self, property):
      """
         Returns true if the property is defined, false if not.
         
         parms:
            property::
               [string] property name
      """
      if self.__node.has_key(property):
         return 1
      elif self.__parent:
         return self.__parent.has_key(property)
      else:
         return 0

   def __getPath(self, pathProp):
      if self.__node.has_key(pathProp):
         return os.path.join(self.__node['cwd'], self.__node[pathProp])
      elif self.__parent:
         return os.path.join(self.__parent.__getPath(pathProp), self.__name)
      else:
         raise KeyError('cachePath')

   def getCachePath(self):
      """
         Returns the recursively evaluated "cache path" - the directory
         that the node page should be cached in.
         
         If any node in the ancestry chain has a "cachePath" property, 
         it is used as the base path for all child nodes.  The root node
         must have this property, or a *KeyError* will be raised.
      """
      return self.__getPath('cachePath')

   def getParent(self):
      """
         Returns the parent node context or *None* if there is no
         parent node (@NodeContext or None).
      """
      return self.__parent
   
   def getNode(self):
      """
         Returns the associated @Node instance.
      """
      return self.__node

   def getPath(self):
      """
         Returns the path traveled to get to the the node (@Path).
         
         For the root node, this returns an empty list.
      """
      if self.__parent:
         path = self.__parent.getPath()
         path.append(self.__name)
         return path
      else:
         return Path()

   def getPathString(self):
      """
         Returns the path traveled to get to this node as a string, complete
         with leading "`/`".
      """
      return '/' + '/'.join(self.getPath())

   def getPathToLocalRoot(self, treeName):
      """
         Returns the segment of the path to the local root of the named
         tree. (@Path)
         
         parms:
            treeName::
               [string] name of the local root to search for in the
               ancestry.  If this value is '.cur', the current node will
               always be returned.
      """
      if self.__node.isLocalRoot(treeName) or not self.__parent:
         return self.getPath()
      else:
         return self.__parent.getPathToLocalRoot(treeName)

class Node:
   """
      This class represents a node in the URL tree.  Every node will
      return an associated piece of data.
   """

   def __init__(self, **properties):
      self.__properties = properties
      cwd = self.__properties['cwd'] = os.getcwd()
      if not properties.has_key('absPath') and properties.has_key('path'):
         self.__properties['absPath'] = \
            os.path.join(cwd, properties['path'])
      self.__loaded = 0
      self.__localRoots = {}

   def getPageInContext(self, request, response):
      """
         Gets the page in its "native execution context" (for now, just
         the current working directory, but eventually this could have
         more meaning than that).
      """
      cwd = request.getProperty('cwd')
      oldDir = os.getcwd()
      os.chdir(cwd)
      
      # renew the session
      request.renewSession(response)
      
      try:
         self.getPage(request, response)
      finally:
         os.chdir(oldDir)
   
   def emitPageInContext(self, request, response):
      """
         This is a special purpose function to allow page delegation.
         Emits the page in its "native execution context".
      """
      cwd = request.getProperty('cwd')
      oldDir = os.getcwd()
      os.chdir(cwd)

      try:
         self.emitPage(request, response)
      finally:
         # restore the original directory on error
         os.chdir(oldDir)      
   
   def getPage(self, request, response):
      """
         Gets the content of the page identified in the request and
         writes it into the response.  If the request is for a static
         page, the cache is refreshed and the response is written from the
         cache.  If not, @emitPage() is called directly and is expected
         to write a page of content type specified by the @getContentType()
         method.
      """
      if self.isStatic(request):
         cachePath = self.getCachePath(request)
         self.refreshCache(request, cachePath)
         response.setContentType(self.getContentType(request))
         src = open(cachePath)
         response.write(src.read())
      else:
         response.setContentType(self.getContentType(request))
         self.emitPage(request, response)

   def emitPage(self, request, response):
      """
         Writes the page.  Should not attempt to set content type or other
         response headers on the response: this must be done in @getPage().
         
         Must be implemented by derived classes.
      """
      raise NotImplementedError()

   def getContentType(self, request):
      """
         Returns the content type of the node.  By default, this is 
         "text/html".
         
         May be overriden by derived classes.
      """
      return 'text/html'
   
   def getCachePath(self, request):
      """
         Returns the cache path for the node.  By default this is constructed
         from the cache path for the node with the extension for its content
         type appended.
         
         May be overriden by derived classes.
      """
      return self.fixExtension(request, request.context.getCachePath())

   def fixExtension(self, request, pathName):
      """
         Fixes the extension of /pathName/ so that it corresponds to the
         content type of the node.
      """
      contentType = self.getContentType(request)
      
      # check to see if there is a property defining the extension for the
      # content type
      ext = request.getProperty('ext.' + contentType)
      
      # if not, try to use a default value
      if ext is None:
         ext = _extension.get(contentType, '')
      
      # add the extension if the path does not already have it
      base, oldExt = os.path.splitext(pathName)
      if oldExt != ext:
         pathName += ext
      
      return pathName
   
   def getNodeAtPath(self, path, parentContext = None, name = ''):
      """
         Returns a tuple consisting of the node dereferenced by the given
         path, the node context and the remainder of the path info 
         (tuple<@Node, @NodeContext, string>).
         
         parms:
            path::
               [string] full path
            parentContext::
               [@NodeContext] the parent's context
            name::
               [string] the name that the node was referenced under (part of
               the path)
      """
      return self, NodeContext(self, name, parentContext), path

   def load(self):
      """
         "Loads" the node - this causes the node object to be fully
         initialized.  A node must be loaded prior to performing any other
         operations on it.
         
         Loading is disassociated from intialization so that we don't have
         to build the entire node tree during initialization.
         
         Derived classes should not override this: override @_load() instead.
      """
      if not self.__loaded:
         self._load()
         self.__loaded = 1
   
   def _load(self):
      """
         This function should be overriden by derived classes needing
         to do late initialization.
      """
      pass         
   
   def __getitem__(self, property):
      return self.__properties[property]
   
   def __setitem__(self, property, val):
      self.__properties[property] = val

   def has_key(self, property):
      return self.__properties.has_key(property)

   def isStatic(self, request):
      """
         Returns true if the node is "static" in the context of the given 
         request - if its construction does not vary based on its parameters.
         
         Must be implemented by derived classes.
      """
      raise NotImplementedError()
   
   def refreshCache(self, request, cachePath):
      """
         Refreshes the cached image of a cacheable node.  If the node is out
	 of date with its dependents (@getDependentsTimestamp() should
	 return the timestamp of the newest dependent) this calls
	 @emitPage() with a modified request that writes to the cache file.

         parms:
            request::
               [@Request]
            cachePath::
               [string] cache file name
      """
      if not os.path.exists(cachePath) or \
         os.path.getmtime(cachePath) < self.getDependentsTimestamp(request):
         
         # make sure that the cache directory exists
         cacheDir = os.path.split(cachePath)[0]
         if not os.path.exists(cacheDir):
            os.makedirs(cacheDir)

         response = CachedResponse(open(cachePath, 'w'))
         self.emitPage(request, response)

   def getDependentsTimestamp(self, request):
      """
         Returns the timestamp of the newest dependent (float).

         This method returns the timestamp based purely upon the timestamps
         of the modules of the classes (immediate and ancestor) of the 
         current page node.
         
         Derived classes should override it if they have dependencies on
         information that is outside of the scope of these modules, and
         should call the base class form of the method to obtain
         the "code timestamp" for comparison.
      """
      return _getClassTimestamp(self.__class__)

   def getSourcePath(self):
      """
         Returns the node's "source path".  This is not context dependent.
      """
      if self.has_key('absPath'):
         return self['absPath']
      elif self.has_key('path'):
         return self['path']
      else:
         return os.getcwd()

   def setLocalRoot(self, treeName):
      """
         This method defines a node as a "local root".  Local roots allow
         URLs to be constructed relative to a known base.  A local root
         parameter can be specified in @Request.getAbsolutePath().
         
         parms:
            treeName::
               [string] tree that the node is a local root for.  Values
               beginning with '.' are reserved and _should not be used_.
      """
      self.__localRoots[treeName] = 1
   
   def isLocalRoot(self, treeName):
      """
         Returns true if the node is the local root for the given tree name.
         
         parms:
            treeName::
               [string] tree to check for.  A value of '.cur' always
               returns true.
      """
      return treeName == '.cur' or self.__localRoots.get(treeName, 0)

   def buildCache(self, context, targetBaseURL, dynamicBaseURL = None):
      """
         Recursive function to build the cache for the node and its 
         descendents.

         parms:
            context::
               [@NodeContext] node invocation context.
            targetBaseURL::
               [string] base URL of the target location.  This will be the
               base of all absolute URLs used to refer to other static pages
               within the tree.  You need not specify the full URL: the 
               path portion (starting from the first slash after host name
               and optional port number) is normally adequate.
            dynamicBaseURL::
               [string or None] base URL of all dynamic web pages in the tree.
               This will be the base of all absolute URLs referred to by
               static pages.  If *None*, attempting to link to a dynamic
               node from a static node will cause an error.
      """
      #print 'building cache node %s' % context.getPath()
      request = _makeStaticRequest(context, targetBaseURL, dynamicBaseURL)
      
      if self.isStatic(request):
         cwd = request.getProperty('cwd')
         oldDir = os.getcwd()
         os.chdir(cwd)
         try:
            self.load()
            try:
               self.refreshCache(request, self.getCachePath(request))
            except Exception, ex:
               error('%s: Exception caught:\n%s' % 
                      (context.getPathString(), StdError.errorText(ex))
                     )
               raise
               
         finally:
            os.chdir(oldDir)
      else:
         return

class NullNode(Node):
   """
      This is the "Page not found" node.
      
      Properties:
         title::
            [string] Page title.  Defaults to "Page not found".
         parcel::
            [@spug.web.htmlo.HTMLElement] page contents.  Defaults to 
            a message with /title/ as a level 1 header, followed by the text
            "The requested URL does not exist.".
         wrapper::
            [@DocWrapper] the wrapper elemlet.
   """
   
   def isStatic(self, request):
      """
         Implements @Node.isStatic()
         
         Always returns false, so we don't go littering the cache with pages
         that were not found.
      """
      return 0

   def getContentType(self, request):
      return 'text/html'
   
   def emitPage(self, request, response):
      wrapper = request.getProperty('wrapper', DocWrapper)
      title = request.getProperty('title', 'Page not found')
      wrapper.setTitle(title)
      wrapper.setParcel(request.getProperty('parcel',
                                            htmlo.XNull(
                                             htmlo.H1(title),
                                             'The requested URL does not exist'
                                             )
                                            )
                        )
      wrapper.writeTo(response)

      
class ParentNode(Node):
   """
      A node with named child nodes.
      
      Properties:
         wrapper::
            [callable<@Request>] Factory to create the @DocWrapper for
            the outer page.
   """

   def __init__(self, **properties):
      Node.__init__(self, **properties)
      self.__children = {}
      self.__impPath = None
      self.__imp = None

   def setPageNode(self, node):
      """
         Sets the "page node": @getPage() requests will be delegated
         to this node if it has been defined.

	 *Deprecated* - use @setPagePath() instead.
      """
      self.__imp = node

   def setPagePath(self, path):
      """
	 Sets the path that @getPage() requests will be delegated to - this
	 allows a ParentNode to display something other than the default
	 directory index.
      """
      self.__impPath = path

   def getPage(self, request, response):
      # make sure the last path segment is empty string (indicating that
      # the path was terminated with a slash). If not, redirect them.
      if not request.isDirectoryPath():
         fixedPath = request.getRequestURL() + '/'
         response.setHeader('Location', fixedPath)
         response.setContentType('text/html')
         htmlo.XDoc(html.H1('Moved Permanently'), 'The document has moved ',
                    html.A('here', href = fixedPath),
                    title = '301 Moved Permanently'
                    ).writeTo(response)
         return
      else:
         Node.getPage(self, request, response)
   
   def emitPage(self, request, response):
      # check to see if there's a page node defined
      if self.__impPath:
	 request = request.getVirtualRequest(self.__impPath)
	 request.context.getNode().emitPage(request, response)
	 return

      # handle the obsolete behavior, too
      elif self.__imp:
         self.__imp.emitPage(request, response)
         return

      # create an unordered list of all children      
      content = htmlo.UL()
      for name, child in self.getOrderedChildren():
         if isinstance(child, ParentNode):
            linkName = name + '/'
            if request.staticContext:
               linkName += request.getProperty('indexFile', 'index')
         else:
            linkName = name
         
         if request.staticContext:
            linkName = child.fixExtension(request, linkName)
         
         link = htmlo.A(name, href = linkName)
         content.append(htmlo.LI(link))
      
      docFact = request.context.get('wrapper', DocWrapper)
      doc = docFact(request)
      doc.setTitle('Contents of %s' % '/'.join(request.traveledPath))
      doc.setParcel(content)
      
      doc.writeTo(response)

   def isStatic(self, request):
      return 1

   def getCachePath(self, request):
      """
         Overrides the @Node.getCachePath() to construct the cache path
         from the name of a file within the directory.
      """
      cachePath = os.path.join(request.context.getCachePath(),
                               request.getProperty('indexFile', 'index')
                               )
      return self.fixExtension(request, cachePath)
      
   
   def addChild(self, name, node):
      self.__children[name] = node
   
   def getChild(self, name):
      return self.__children[name]
   
   def getAllChildren(self):
      """
         Returns an unordered list of child objects 
         (list<tuple<string, @Node>>).
      """
      return self.__children.items()

   def deleteChild(self, name):
      """
	 Removes a specific child.  Raises a *KeyError* if the child does not
	 exist.

	 parms:
	    name::
	       [string] child name
      """
      del self.__children[name]

   def deleteAllChildren(self):
      """
	 Deletes all children of the node.
      """
      self.__children = {}

   def getOrderedChildren(self):
      """
         Returns a list of child names and objects (tuple<string, @Node>)
	 ordered by the "natural order" of the parent node.  By default,
	 this is alphabetical.
      """
      children = self.__children.items()
      children.sort()
      return children
      
   __pathSegmentRx = re.compile(r'([^/\?]*)')

   def getNodeAtPath(self, path, parentContext = None, name = ''):
      """
         Overrides @Node.getNodeAtPath() to actually implement the recursive
         path searching.
      """

      # make sure that the current node is loaded
      self.load()

      # create context for the local node
      context = NodeContext(self, name, parentContext)
      
      # if it starts with a question mark, the rest is query parms
      # XXX this level of parsing might belong elsewhere
      if not path or path == '/' or path[0] == '?':
         return self, context, path
      
      # if we start with a slash, remove it
      if path[0] == '/':
         path = path[1:]
      
      # check to see if there's another path segment
      m = self.__pathSegmentRx.match(path)
      next = m.group(1)
      rest = path[m.end():]

#      print 'next = %s' % next      
      if self.__children.has_key(next):
         return self.__children[next].getNodeAtPath(rest, context, next)
      else:
         return None, None, path

   def getDependentsTimestamp(self, request):
      if self.__impPath:
	 request = request.getVirtualRequest(self.__impPath)
	 return request.context.getNode().getDependentsTimestamp(request)
      elif self.__imp:
         return max(Node.getDependentsTimestamp(self, request),
                    self.__imp.getDependentsTimestamp(request)
                    )
      else:
         return Node.getDependentsTimestamp(self, request)

   def buildCache(self, context, targetBaseURL, dynamicBaseURL = None):
      "Overrides @Node.buildCache() to build children."
      Node.buildCache(self, context, targetBaseURL, dynamicBaseURL)
      #print '  is directory'

      for name, child in self.getAllChildren():
         #print '  doing child %s' % name
         childContext = NodeContext(child, name, context)
         child.buildCache(childContext, targetBaseURL, dynamicBaseURL)            

class PythonScript(ParentNode):
   """
      A node that corresponds to a python script.  Child nodes are public
      names (i.e. names not beginning with underscore) in the script's
      namespace, unless a "spugwebIndex" variable is defined.

      If the script has a "spugwebIndex" variable, it should be associated
      with a dictionary (dict<string, object>) mapping the child name
      to the node for that child.  The child node may be either an
      instance of a @Node derivative, or a callable object.  If it is a 
      callable object it will be converted to a @PythonFunc instance.
      
      If the script has a "spugwebPage" variable, it should be associated
      with either a callable object or a @Node derivative.  This variable
      can be used to override the presentation of the node for the script.
      It is important to note that spugwebPage does not affect child lookups:
      If you specify a path to a child of the script, it will still
      look in the spugwebIndex or global symbol table to resolve the child,
      it will not delegate child lookup to the spugwebPage node.
      
      Properties:
         path::
            [string] script path name.  If this is a relative path, it
            is relative to the current directory.
   """

   def __init__(self, **properties):
      ParentNode.__init__(self, **properties)
      self.__imp = None

   def getPage(self, request, response):
      if self.__imp:
         self.__imp.getPageInContext(request, response)
      else:
         ParentNode.getPage(self, request, response)

   def _load(self):
      context = {}
      execfile(self['path'], context)
      
      # check for a spugwebIndex variable
      if context.has_key('spugwebIndex'):
         index = context['spugwebIndex']
      else:
         
         # no index: construct from public variable names
         index = {}
         for key, val in context.items():
            if key[:1] != '_':
               index[key] = val
      
      # check for a spugwebPage variable defining the page implementation
      if context.has_key('spugwebPage'):
         imp = context['spugwebPage']
         if isinstance(imp, Node):
            self.__imp = imp
         elif callable(self.__imp):
            self.__imp = PythonFunc(func = imp)
      
      for key, val in index.items():
         if isinstance(val, Node):
            node = val
         elif callable(val):
            node = PythonFunc(func = val)
         else:
            # ignore the node
            continue

         self.addChild(key, node)      

   def isStatic(self, request):
      # if there is an implementation, we let him make the decision
      if self.__imp:
         return self.__imp.isStatic(request)
      else:
         return 1

   def getDependentsTimestamp(self, request):
      # XXX need to reload the script if it is newer than our "load time"
      return max(os.path.getmtime(self['path']), 
                 ParentNode.getDependentsTimestamp(self, request)
                 )

class PythonFunc(Node):
   """
      A node that corresponds to a python function.
      
      The function must accept three parameters:
      
         manager::
            [any] this parameter exists for backwards compatibility
            and is passed in as *None*.
         request::
            [@Request]
         response::
            [@Response]
      
      Properties:
         
         func::
            [callable<any, @Request, @Response>] python function to call.
   """
   
   def getPage(self, request, response):
      "Implements @Node.getPage()"
      request.context['func'](None, request, response)

   def isStatic(self, request):
      return 0

class Directory(ParentNode):
   """
      A node that corresponds to an actual directory in the file system.
   """
   
   def _load(self):
      source = self.getSourcePath()
      olddir = os.getcwd()
      os.chdir(source)
      
      try:
         if os.path.exists('index.py'):
            context = globals().copy()
            context['cur'] = self
            context['root'] = _root
            execfile('index.py', context)
         else:
            # scan the directory
            for file in os.listdir('.'):
               base, ext = os.path.splitext(file)
               if os.path.isdir(file):
                  self.addChild(file, 
                                Directory(path = os.path.join(source, file))
                                )
               elif ext in ('.html', '.htm'):
		  child = HTMLNode(path = file)
                  self.addChild(file, child)

		  # if this is an index page, use it for the directory
		  if base == 'index':
		     self.setPageNode(child)
               elif ext == '.py':
                  self.addChild(file, PythonScript(path = file))
               elif ext == '.nml':
                  self.addChild(file, NMLNode(path = file))
      finally:
         os.chdir(olddir)

   def getDependentsTimestamp(self, request):
      if os.path.exists('index.py'):
         return max(os.path.getmtime('index.py'), 
                    ParentNode.getDependentsTimestamp(self, request)
                    )
      else:
         return ParentNode.getDependentsTimestamp(self, request)

class NMLNode(Node):
   """
      Node for NML documents.
      
      Properties:
         wrapper::
            Standard document wrapper object.
         wrapperPath::
            [string] path to an HTML wrapper file (will probably replace this
            with a more generic notion of a wrapper).
   """

   class WOFHTMLFormatter(HTMLFormatter):
      """
	 Specializes the NML @HTMLFormatter class to override link resolution.
      """

      __localRootRx = re.compile(r'\$(\w+)(/(.*))?')

      def __init__(self, out, request):
	 self.__request = request
	 HTMLFormatter.__init__(self, out)

      def _fixRef(self, ref):
	 val = str(ref)

	 # if this is a raw reference, just stringify it
	 if isinstance(ref, TextBlock) and ref.type == 'sw.raw':
	    return val

	 # if it starts with a '$', get the appropriate local root
	 m = self.__localRootRx.match(val)
	 if m:
	    return self.__request.getAbsolutePath(m.group(3) or '', m.group(1))
	 else:
	    # all other paths are treated verbatim
	    return val

   # this is a pretty ugly hack - we take advantage of the lack of strict
   # inheritance and type safety in python to create something that can 
   # stand in for an Element derivative so we can format NML.
   class NMLWriter(xmlo.Element):

      def __init__(self, text, request):
         xmlo.Element.__init__(self, 'nmlwriter')
         self.text = text
	 self.request = request
      
      def _writeTo(self, out, nsLocalNames, options, curIndent = 0):
         formatter = NMLNode.WOFHTMLFormatter(out, self.request)
         formatter.format(self.text)
         formatter.close()

      def _copyInst(self):
	 """
	    Overrides @xmlo.Element._copyInst() since we have a non-standard
	    constructor.
	 """
	 return self.__class__(self.text, self.request)

   class HTMLWrapperFile:
      """
         Another hack to wrap the old-style HTML wrapper files.
      """
      
      def __init__(self, request):
         self.sourceFile = request.getProperty('wrapperFile')
         self.title = None
         self.parcel = None
      
      def setTitle(self, title):
         self.title = title
      
      def setParcel(self, parcel):
         self.parcel = parcel
      
      def getDependentsTimestamp(self, request):
         return os.path.getmtime(self.sourceFile)
      
      def writeTo(self, out):
         if self.sourceFile:
            
            # expand the source file
            src = open(self.sourceFile)
            for cur in src.readlines():
               if string.strip(cur) == '&expand':
                  self.parcel._writeTo(out, None, None, 0)
               else:
                  out.write(cur)
         else:
         
            # no source file, just expand a vanilla document
            doc = htmlo.XDoc()
            if self.title:
               doc.head.append(htmlo.Title(self.title))
            doc.body.append(self.parcel)
            doc.writeTo(out)            
   
   def isStatic(self, request):
      return 1
   
   def getNMLText(self, request):
      """
	 Returns the NML TextBlock for the document.  This loads it from the
	 source path by default, but can be overriden by derived classes.
      """
      sourcePath = self.getSourcePath()

      # read and parse the NML document
      reader = LineReader(open(sourcePath))
      parser = DocParser(reader)
      text = parser.parseDoc()
      return text

   def emitPage(self, request, response):
   
      wrapper = request.getProperty('wrapper', self.HTMLWrapperFile)
      text = self.getNMLText(request)
      wrapper.setParcel(self.NMLWriter(text, request))
      
      # get the title
      title = request.getProperty('title')
      if title is None:
         title = 'Document'
         for word in text.words:
            if isinstance(word, TextBlock) and word.type.isdigit():
               title = ' '.join(word.words)
               break
      wrapper.setTitle(title)
      
      # write the page
      wrapper.writeTo(response)

   def getDependentsTimestamp(self, request):
      wrapper = request.getProperty('wrapper', self.HTMLWrapperFile)
      return max(Node.getDependentsTimestamp(self, request), 
                 wrapper.getDependentsTimestamp(request),
                 os.path.getmtime(self.getSourcePath())
                 )

class FileNode(Node):
   """
      This is the base class for nodes representing files that are served in
      their source form with no translation.
   """

   def getPage(self, request, response):
      response.setContentType(self.getContentType(request))
      
      # we don't bother going to the cache for this: this is not a generated
      # page, quicker to get it right from the source
      response.write(open(self['path']).read())
   
   def isStatic(self, request):
      "Implements @Node.isStatic()"
      return 1
   
   def emitPage(self, request, response):
      """
         Even though we implement @getPage(), we have to also implement
         @emitPage() so that we can generate a cache entry.
      """

      source = open(self.getSourcePath(), 'rb')
      
      # copy the file from the source right onto output
      while 1:
         data = source.read()
         if not data:
            break
         response.write(data)

   def getContentType(self, request):
      """
         Returns the node's "content-type" field.
         
         Must be implemented by derived class.
      """
      raise NotImplementedError()

   def getDependentsTimestamp(self, request):
      """
         Implements @Node.getDependentsTimestamp() to return the timestamp
         of the source file.
      """
      return max(Node.getDependentsTimestamp(self, request),
                 os.path.getmtime(self.getSourcePath())
                 )

class HTMLNode(FileNode):
   """
      Node to represent a plain HTML page (which can be copied directly to
      the cache with no processing).
   """
   
   def getContentType(self, request):
      return 'text/html'

class CSSNode(FileNode):
   """
      Node to represent a CSS file.
   """
   
   def getContentType(self, request):
      return 'text/css'

class TextNode(FileNode):
   """
      Node to represent a plain text file.
   """
   
   def getContentType(self, request):
      return 'text/plain'

class JpegNode(FileNode):
   """
      Node to represent a JPEG image.
   """
   
   def getContentType(self, request):
      return 'image/jpeg'

class PNGNode(FileNode):
   """
      Node to represent a PNG image.
   """
   
   def getContentType(self, request):
      return 'image/png'

class ProtectedNode(Node):
   """
      A node with access protection.
      
      Each *ProtectedNode* has an associated implementation node, which
      does all of the actual node display.  The *ProtectedNode* simply
      manages the access protection for the implementation node.
      
      Properties:
         imp::
            [@Node] implementation node.
         accessDenied::
            [@Node] access denied node.  Defaults to @NullNode.
         privilege::
            [string] privilege name.  Defaults to "access".
         accessManager::
            [@AccessManager] object used to verify privilege.  Defaults to 
            @NullAccessManager.
   """
   
   def isStatic(self, request):
      "Overrides @Node.isStatic().  Protected nodes can not be static."
      return 0

   def getPage(self, request, response):
      accessManager = request.getProperty('accessManager', NullAccessManager())
      privilege = request.getProperty('privilege', 'access')
      if accessManager.hasAccess(request, privilege):
         request.getProperty('imp').getPage(request, response)
      else:
        page =  request.getProperty('accessDenied', NullNode())
        page.getPage(request, response)

class Path(list):
   """
      Represents a URL path.  Overrides *list* so that the string 
      representation is a slash separated path.
   """
   
   def __str__(self):
      return '/' + '/'.join(self)

   def __add__(self, other):
      result = Path(self)
      result.extend(other)
      return result
   
   def __getslice__(self, start, end):
      return Path(list.__getslice__(self, start, end))

   def __mul__(self, multiplier):
      return Path(list.__mul__(self, multiplier))
   
   def __rmul__(self, multiplier):
      return Path(list.__rmul__(self, multiplier))

   def __getitem__(self, key):
      "Overrides slice access to return a @Path instance."
      if isinstance(key, slice):
	 p = Path()
	 p[:] = self[key.start:key.stop]
	 return p
      else:
	 return list.__getitem__(self, key)

   def asAccessPath(self, request):
      """
	 Returns the "access path" (path used to access the resource
	 exterally, will add the appropriate extensions in static context) for
	 the "internal path" represented by *self*.  Returns a @Path instance.

	 parms:
	    request::
	       [@Request]
      """
      node = request.context.getNode()
      if node.isStatic(request):
	 return self[:-1] + [node.fixExtension(request, self[-1])]

class Request(cgi.CGIRequest):
   """
      Request object which adds the following to CGIRequest:
      
      Public-vars:
         context::
            [@NodeContext] the node context
	 remainingPath::
	    [list<string>] path components not used to get to the node.
         dynamicBaseURL::
            [string] base URL for dynamic requests called in a static context.
         staticContext::
            [boolean] true if the request occurs in a static context (while
            building the static page tree)
         locals::
            [dict<any, any>] local objects.  This dictionary can be
            used to store information that must be passed between different
            methods processing the same request.
   """
   
   def __init__(self, args, env, query, path, context, remainingPath,
                staticContext = 0,
                dynamicBaseURL = None
                ):
      cgi.CGIRequest.__init__(self, args, env, query, path)
      self.context = context
      self.remainingPath = remainingPath
      self.staticContext = staticContext
      self.dynamicBaseURL = dynamicBaseURL
      self.locals = {}

      # these values are calculated on demand and cached
#      self.__traveledPath = None
#      self.__fullPath = None
      
      # XXX cgi specific
      
      # parse the script name (base path) and filter out empty path components
      scriptName = self.env['SCRIPT_NAME'].split('/')
      self.basePath = Path([x for x in scriptName if x])

   def getProperty(self, property, defaultValue = None):
      """
         Returns the value of a property, performing all necessary transforms
         on it.
         
         The "raw value" of a property is the value of the property in the
         /context/ object.  If the raw value is a callable object, or an
         instance of @NodeProperty, it is called (with the request instance
         as its only parameter) and the return value will be returned as the
         "actual value" of the property.  Any non-callable raw value
         is simply returned as the actual value.
         
         parms:
            property::
               [string] property name
            defaultValue::
               [any] A default "raw value" of the attribute.  If the attribute
               is unassigned, this raw value is used and all of the transforms
               are applied.
      """
      rawValue = self.context.get(property, defaultValue)
      if callable(rawValue):
         return rawValue(self)
      else:
         return rawValue
   
   def getPropertyDependency(self, property, defaultValue = None):
      """
         Returns a @Dependency wrapper around a property, allowing us to make 
         cached values dependent on properties.
         
         If the raw value of a property is an instance of @Dependency, the raw 
         value is returned.  Otherwise, a dependent is constructed from the 
         class of the property.
         
         XXX we should also be considering the timestamp of the file where 
         the property was assigned, as this can certainly affect the value of 
         the property.
         
         parms:
            property: [string] property name
            defaultValue: [@Dependency or None] The value returned if the 
               property is not found.
      """
      val = self.context.get(property)
      if isinstance(val, Dependency):
         return val
      else:
         
         # in old style classes, the class is attached to the __class__ 
         # variable.  In new style classes, it is the type.
         valType = type(val)
         if valType is types.ClassType:
            return ClassDependency(val.__class__)
         else:
            return ClassDependency(valType)
            
      
   def getAbsolutePath(self, traveledPath, treeName = None):
      """
         Returns a string consisting of the absolute path necessary to 
         obtain the given traveled path.
         
         parms:
            traveledPath::
               [string] the path from the root of the spugweb tree to the
               referenced node.
            treeName::
               [string or None] if this is not *None*, the traveled path
               is relative to the "local root" of the given tree.
               See @Node.setLocalRoot().
               
               The special value '.cur' indicates that the root is the current
               node.  This is used for safely dereferencing a child across
               static\/dynamic contexts.
      """
      if treeName:
         localRootPath = self.context.getPathToLocalRoot(treeName)
      else:
         localRootPath = []
      
      absPath = str(self.basePath + localRootPath + [traveledPath]) 
         
      if self.staticContext:
         # if we are in static context, we need to resolve the node so that
         # we can see if it is a static node and determine what to use
         # as a prefix
         pathFromRoot = str(localRootPath + [traveledPath])
         referencedNode, context, remainingPath = \
            self.getRootNode().getNodeAtPath(pathFromRoot)
         
         # make sure this is a valid node
         if not referencedNode:
            error('%s: Reference to non-existent node %s' % 
                   (self.context.getPathString(), pathFromRoot)
                   )
            return absPath
         
         refRequest = \
            _makeStaticRequest(context, str(self.basePath),
                               self.dynamicBaseURL
                               )
         if not referencedNode.isStatic(refRequest):
            if self.dynamicBaseURL:
               return self.dynamicBaseURL + pathFromRoot
            else:
               error('%s: Dynamic object %s referenced: dynamic base '
                      'URL must be defined' %
                      (self.context.getPathString(), pathFromRoot)
                     )
         
         # if this is a parent node, make the request to the index file
         # XXX should really tuck this into the Node/ParentNode methods...
         if isinstance(referencedNode, ParentNode):
	    if absPath[-1] == '/':
	       connector = ''
	    else:
	       connector = '/'
            absPath = '%s%s%s' % \
               (absPath, connector, 
	        refRequest.getProperty('indexFile', 'index')
		)
         
         return referencedNode.fixExtension(refRequest, absPath)
            
      return absPath

   def newSession(self):
      """
         Creates a new @Session instance and returns it.
         
         Sets the following session keys by default:
            hostIP::
               [string] client IP address (used for later verification
               to prevent session theft)
            path::
               [string] session cookie path (defaults to the "base path" so
	       that it applies to the entire spugweb instance).
      """
      timeout = self.getProperty('sessionTimeout', 15 * 60)
      ses = _sesMgr.newSession(timeout)
      ses['hostIP'] = self.getHostIP()
      ses['path'] = '/%s/' % '/'.join(self.basePath)
      return ses

   def deleteSession(self, sessionId):
      """
         Delete the session indicated by the session id.
         
         parms:
            sessionId::
               [string]
      """
      del _sesMgr[sessionId]

   def getSession(self):
      """
         Returns the current session object (an instance of @Session), or
	 *None* if it does not exist.
      """
      return _sesMgr.get(self.getSessionId())

   def renewSession(self, response):
      """
         If there is a session for the request and its "renewel time" has
         expired, create a new session id and store it in the response.
      """
      ses = self.getSession()
      if ses and time.time() > ses.renewTime:
         _sesMgr.renew(ses)
         response.setSession(ses)

   # XXX implementations are CGI specific

   def getAuthority(self):
      """
	 Returns the "authority" section of the current path - host name and
	 optionally port number.
      """
      port = self.env['SERVER_PORT']
      if port == '80':
         port = ''
      else:
         port = ':' + port

      return self.env['SERVER_NAME'] + port

   def getRequestURL(self):
      
      queryString = self.env['QUERY_STRING']
      if queryString:
         queryString = '?' + queryString
      
      return 'http://%s%s%s' % \
         (self.getAuthority(), str(self.fullPath),
          queryString
          )

   def getHostIP(self):
      """
         Returns the host IP address (string).
      """
      return self.env['REMOTE_ADDR']

   __cookieRx = re.compile(r'session=(.*)')

   def getSessionId(self):
      """
         Returns the session id (a string) or *None* if there is no
         session id defined.
      """
      if self.env.has_key('HTTP_COOKIE'):
         m = self.__cookieRx.match(self.env['HTTP_COOKIE'])
         if m:
            return m.group(1)
      else:
         return None

   # Ok, we need to have some definitions here:
   #
   # Let's say we have the following URL:
   #   http://foobar.com/cgi-bin/swgw/container/page/extra/crap
   #
   # Assume that spugweb is referenced using the "swgw" program in the
   # cgi-bin directory.  Assume that "container" is a parent node, and
   # "page" is a final (non-parent) node, so that "extra/crap" is
   # additional path information passed into "page".
   #
   # The "authority" is the hostname/port number (as it is named in the formal
   # URI standard, "foobar.com" in our example)
   #
   # The _full path_ is the complete path component of the URL
   # ("cgi-bin/swgw/container/page/extra/crap" in our example)
   #
   # the _base path_ is the path to the root of the spugweb tree
   # ("cgi-bin/swgw" in our example)
   #
   # the _traveled path_ is the path from the base path to the node
   # who's getPath() method is actually evaluated ("container/page" in our
   # example)
   #
   # the _remaining path_ is any path information that is left over after
   # locating the node to be evaluated ("extra/crap").
   #
   # The _utilized path_ is the base path plus the traveled path - this
   # is the path that would be needed to get back to this node in a
   # subsequent request ("cgi-bin/swgw/container/page")
   #
   # the _path_ variable exists for backwards compatibility: it is equivalent
   # to the _traveled path_ plus the _remaining path_.

   def __getTraveledPath(self):
      val = self.traveledPath = self.context.getPath()
      return val
   traveledPath = property(__getTraveledPath)
   
   def __getFullPath(self):      
      val = self.fullPath = \
         self.basePath + self.traveledPath + self.remainingPath
      return val
   fullPath = property(__getFullPath)

   def __getUtilizedPath(self):
      val = self.utilizedPath = self.basePath + self.traveledPath
      return val
   utilizedPath = property(__getUtilizedPath)

   def isDirectoryPath(self):
      """
         Returns true if the full path is "a directory path" - i.e. if the
         path ends with a forward slash ("`/`").
      """
      return not self.fullPath or self.fullPath[-1] == ''

   def resolvePath(self, relativePath):
      """
         Returns a new full path relative to the existing utilized path
	 (list<string>). This is useful for traversing between "facades" of
	 a node. Current directory ("."), parent directory ("..") and root
	 directory ("/") function as they would in a shell when referencing
         a file system path.

         For example:

         If the utilized path is either "`/foo/bar`" or "`/foo/bar/`" and
	 /relativePath/ is "test", "#['foo', 'bar', 'test']#`" is returned.

         If the utilized path is "`/foo/bar`" and the /relativePath/ is
         "`../test`", "#['foo', 'test']#" is returned.
         
         If /relativePath/ begins with a slash ("`/`"), /relativePath/ is
         returned (converted to a list of strings).

         parms:
            relativePath::
               [string] path segment to append to the utilized path.

      """ #"
      
      # make a copy of the utilized path
      path = self.utilizedPath[:]

      # remove directory designator (if any)
      if path and path[-1] == '':
         path.pop()
      
      rel = relativePath.split('/')
      
      # if the relative path starts with a slash, this is easy
      if not rel[0]:
         return rel[1:]
      
      for part in rel:
         if part == '.':
            continue
         elif part == '..' and path:
            path.pop()
         else:
            path.append(part)
      
      return path      

   def getRootNode(self):
      """
         Returns the root node (@Node).
      """
      context = self.context
      parent = context.getParent()
      while parent:
         context = parent
         parent = context.getParent()

      return context.getNode()

   def getVirtualRequest(self, path, localRoot = None):
      """
         Creates a virtual request derived from self.  Returns a 
         @Request instance containing the virtual request.
         
         A virtual request is used to obtain node values from within
         the system.

         parms:
            path::
               [string] URL path of the request (may or may not include 
               leading forward slash)
            localRoot::
               [string] local root name to base the path at.
      """
      basePath = self.context.getPathToLocalRoot(localRoot)
      
      # strip leading and trailing slashes
      if path[0] == '/':
         path = path[1:]
      if path[-1] == '/':
         path = path[:-1]
      
      # construct the complete path
      path = basePath + path.split('/')
      
      # get the node and context
      node, context, remainingPath = \
         self.getRootNode().getNodeAtPath('/' + '/'.join(path))
      if node is None:
         raise Exception('Node at %s does not exist' % repr(path))
      
      # convert the remaining path to a list
      if remainingPath:
	 remainingPath = remainingPath.split('/')
      else:
	 remainingPath = []

      # create the request object
      request = \
         Request(self.args, self.env, self.query, self.path, context,
                 remainingPath,
                 self.staticContext,
                 self.dynamicBaseURL
                 )
      return request

def _makeStaticRequest(context, targetBaseURL, dynamicBaseURL):
   # XXX putrid ugly hack XXX
   # not sure what I was thinking when I labeled this a "putrid ugly hack",
   # unless I was talking about the fact that I'm stuffing CGI environment
   # variables into it (certainly ugly, if not putrid).  Request should
   # probably be abstracted to permit other modes of obtaining this
   # information.
   scheme, authority, path, parameters, query, fragment = \
      urlparse(targetBaseURL)
   envVars = {}
   if authority:

      # this code assumes the scheme is http/https
      assert scheme in ('http', 'https')

      # extract host name and port number (if provided)
      authority = authority.split(':')
      if len(authority) == 2:
	 port = authority[1]
      else:
	 port = '80'
      server = authority[0]

      envVars['SERVER_NAME'] = server
      envVars['SERVER_PORT'] = port
   envVars['SCRIPT_NAME'] = path
   envVars['QUERY_STRING'] = query

   return Request([], envVars, {}, context.getPath(), context, [],
                  staticContext = 1,
                  dynamicBaseURL = dynamicBaseURL
                  )


class Response:
   """
      The response object - passed into @Node.getPage() methods to allow
      a response to be written back to the client.
   """

   def __init__(self, out):
      """
         parms:
            out::
               [file.write] output stream that the response will be written
               to.
      """
      self._out = out
      self.__headers = { 'Content-type': 'text/plain' }
      self.__headersWritten = 0

   def setContentType(self, contentType):
      if self.__headersWritten:
         raise Exception('Headers have already been written')
      self.setHeader('Content-type', contentType)

   def setSession(self, session):
      """
         Sets the session cookie.
         
         parms:
            session::
               [@Session]
      """
      if self.__headersWritten:
         raise Exception('Headers have already been written')
      self.setHeader('Set-Cookie', 
                     'session=%s; Version=1; Path=%s; Max-Age=%d' % 
                      (session.id, session['path'], 
                       int(session.expireTime - time.time())
                       )
                     )
   
   def setHeader(self, header, value):
      if self.__headersWritten:
         raise Exception('Headers have already been written')
      self.__headers[header] = value

   def writeHeaders(self):
      """
         Writes the HTTP response headers.  This will be done automatically
         from @write() if it has not been done before the first write.
      """
      if self.__headersWritten:
         raise Exception('Headers have already been written')
      for header, value in self.__headers.items():
         self._out.write('%s: %s\n' % (header, value))
      self._out.write('\n')
      self.__headersWritten = 1
   
   def write(self, data):
      """
         Writes data to the output stream (back to the client).
         
         This will write headers if they have not already been written.
      """
      if not self.__headersWritten:
         self.writeHeaders()
      self._out.write(data)

class CachedResponse(Response):
   """
      Class to allow us to emit response pages to a cache file.
   """

   def setContentType(self, contentType):
      raise Exception('Headers have already been written')
   
   def setHeader(self, header, value):
      raise Exception('Headers have already been written')

   def writeHeaders(self):
      raise Exception('Headers have already been written')
   
   def write(self, data):
      self._out.write(data)

class Session(dict):
   """
      Implemenation of a session.  A session maps keys to values using the
      dictionary interface
   """
   
   __slots__ = [ 'id', 'expireTime', 'renewTime', 'expireInterval', 
                 'renewInterval' ]
   
   def __init__(self, sessionId, expireInterval, renewInterval):
      self.id = sessionId
      self.expireInterval = expireInterval
      self.renewInterval = renewInterval      
      dict.__init__(self)
      self.renew()
   
   def expired(self):
      "Returns true if the session is expired"
      return time.time() > self.expireTime

   def renew(self):
      """
         Resets expireTime and renewalTime from the expiration and renewal
         intervals.
      """
      curTime = time.time()
      self.expireTime = curTime + self.expireInterval
      self.renewTime = curTime + self.renewInterval

class SessionManager:
   """
      Manages all of the known sessions and keeps track of their expiration.
   """
   
   def __init__(self):
      self.__sessions = {}
   
   def get(self, sessionId):
      """
         Returns the given session or *None* if the session key is either
         undefined or expired.
      """
      ses = self.__sessions.get(sessionId)
      if ses and ses.expired():
         del self.__sessions[ses.id]
         ses = None
      
      return ses

   def __delitem__(self, sessionId):
      """
         Used to delete a session.
      """
      del self.__sessions[sessionId]

   def __getRandomId(self):
      # XXX not the best way to do randomness
      while 1:
         sessionId = '%08x' % struct.unpack('>I', open('/dev/random').read(4))[0]
         if not self.__sessions.has_key(sessionId):
            return sessionId
   
   def newSession(self, expireInterval, renewInterval = -1):
      """
         Creates and stores a new session object.  Returns the @Session 
         instance.
         
         parms:
            liveInterval::
               [float] session "time to live" in seconds.
            renewInterval::
               [float] session "time before renewal" in seconds.  If -1,
               66% of /liveInterval/ is used.
      """
      sessionId = self.__getRandomId()

      if renewInterval == -1:
         renewInterval = expireInterval * 0.66
      
      ses = Session(sessionId, expireInterval, renewInterval)
      self.__sessions[ses.id] = ses
      return ses

   def renew(self, session):
      """
         Renews the session by creating a new session key for it and changing
         the expiration and renewal times.
      """
      del self.__sessions[session.id]
      session.id = self.__getRandomId()
      self.__sessions[session.id] = session
      session.renew()

_sesMgr = SessionManager()

class AccessManager:
   """
      Basic interface for determining access levels.   
   """
   
   def hasAccess(self, request, priviliege):
      """
         Returns true if the client has the privilege.
         
         Must be implemented by derived classes.
         
         parms:
            request::
               [@Request]
            privilege::
               [string] privilege name
      """
      raise NotImplementedError()

class NullAccessManager(AccessManager):
   """
      Default access manager.  Always denies access, so if the programmer
      forgets to define an access manager access is always denied.
   """
   
   def hasAccess(self, request, privilege):
      "Implements @AccessManager.hasAccess()"
      return 0   

class DocWrapper(htmlo.XDoc):
   """
      Document wrapper.  This encapsulates the representation of outer page
      information so that clients can focus on providing the central
      page content.
   """

   def __init__(self, request):
      htmlo.XDoc.__init__(self)
   
   def setParcel(self, parcel):
      """
         Sets the parcel (the central content) of the document.
         
         parms:
            parcel::
               [@spug.htmlo.HTMLElement]
      """
      self[1] = parcel
   
   def setTitle(self, title):
      """
         Sets the page title.
         
         parms:
            title::
               [string] page title
      """
      self.head.append(htmlo.Title(title))
   
   def getDependentsTimestamp(self, request):
      """
         Returns the timestamp of the oldest dependent.
         
         parms:
            request: [@Request]
      """
      return _getClassTimestamp(self.__class__)

class NullElemlet(htmlo.XNull):
   """
      A "null element" factory - suitable for use in cases where elemlet
      property expansion is requested but the property is not defined.
   """
   
   def __init__(self, request):
      htmlo.XNull.__init__(self)

class XMLElemlet(htmlo.XNull):
   """
      An elemlet constructed from an XML document.  The source file
      should be a document in the XHTML namespace containing a single
      "content" node and zero or more "title" nodes (both in the spugweb
      namespace).
      
      Properties:
         xmldocwrapper.file::
            Source file for the XML wrapper page.
   """

   # nested class to be used as an explorer to edit the source document
   # and perform all transforms
   class Seeker:
      def __init__(self, request):
         self._request = request
      
      def _transform(self, name, node):
         """
            This method is provided so that derived classes may extend the
            set of nodes which may be transformed.  Returns true if the
            name was recognized.  Base class version of the method always
            returns false
            
            parms:
               name::
                  [string] local element name of the node under 
                  consideration.
               node::
                  [string or @spug.web.xmlo.Element] node under consideration.
         """
         return 0

      def __call__(self, node):
         if isinstance(node, xmlo.Element) and \
            node.getActualNamespace() == SPUGWEB_NS:
            
            name = node.getName()
            if name == 'element':
            
               # if this is an "element" node, replace it with the
               # value of the property right now
               parent = node.getParent()
               parent[parent.index(node)] = \
                  self._request.getProperty(node['property'], NullElemlet)

            elif name == 'attr':

               # get the value from the property attribute or from the
               # url attribute
               if node.has_key('property'):
                  val = self._request.getProperty(node['property'], '')
               elif node.has_key('url'):
               
                  # get the local root, if any
                  root = node.get('root')
                  
                  # and get the absolute path
                  val = self._request.getAbsolutePath(node['url'], root)
               else:
                  val = ''
               
               # if this is an "attr" node set the attribute of the parent
               # from the property value
               parent = node.getParent()
               parent[node['name']] = val
                  
               # remove the node, clean out any remaining whitespace
               parent.deleteItem(parent.index(node))
               parent.stripEmptyContents()

	    elif name == 'link':

	       # shortcut form of attribute substitution

	       # get the root, if any
	       root = node.get('root')

	       # create a new html "A" element with the correct path
	       newNode = \
		  htmlo.A(href = 
			   self._request.getAbsolutePath(node['href'], root)
			  )
	       for item in node:
		  newNode.append(item)

	       parent = node.getParent()
	       parent[parent.index(node)] = newNode
               
            else:
               self._transform(name, node)

         return xmlo.Element.EXPAND

   def __init__(self, request, doc = None, seeker = None):
      """
         parms:
            request::
               [@Request]
            doc::
               [@spug.web.xml.Element] document root.  If not provided,
               the document is obtained from the xmldocwrapper.file
      """
      if not doc:
         doc = xmlo.loadXML(request.query['xmldocwrapper.file'], 
                            htmlo.HTMLElementFactory()
                            )
      
      self.__doc = doc
      
      # perform the necessary transforms
      if not seeker:
         seeker = self.Seeker(request)
      doc.iterate(seeker)

      htmlo.XNull.__init__(self, doc)

class XMLElemletFactory(Dependency):
   """
      Factory to create an @XMLElemlet instance, allowing the document
      to be parsed only once.
   """
   
   def __init__(self, source):
      """
         parms:
            source::
               [string or @spug.web.xmlo.Element] If this is the string,
               it is the name of an XML or CXML file to load.  If it is
               an Element, it is the actual document object.
      """
      if isinstance(source, xmlo.Element):
         self._doc = source
         self.__timstamp = _getClassTimestamp(source.__class__)
      else:
         self._doc = xmlo.loadXML(source, htmlo.HTMLElementFactory())
         self.__timestamp = os.path.getmtime(source)

   def __call__(self, request):
      # XXX I think we should reload if the timestamp has changed
      return XMLElemlet(request, self._doc.copy())
   
   def getTimestamp(self, request):
      return self.__timestamp
      
class XMLDocWrapper(XMLElemlet):
   
   """
      Document wrapper generated from an XML source file.  
   """

   # this is a nice clean way to keep track of a node's position so we can
   # replace it
   class NodeSlot:
      def __init__(self, parent, index):
         self.parent = parent
         self.index = index
      def replace(self, newNode):
         self.parent[self.index] = newNode

   # this nested class is used as an explorer to locate the positions of
   # the title nodes and content node and to create the list of dependencies.
   # The 'title' and 'content' instance variables are a list of parent/index 
   # tuples
   # the 'head' and 'body' instance variables are the head and body elements
   class Seeker(XMLElemlet.Seeker):
      def __init__(self, request):
         XMLElemlet.Seeker.__init__(self, request)
         self.title = []
         self.content = []
	 self.head = None
	 self.body = None
	 self.dependents = []

      def __call__(self, node):
	 "Override the call method so we can trap 'head' and 'body'"
	 if  isinstance(node, xmlo.Element):
	    name = node.getName()
	    if node.getActualNamespace() == htmlo.XHTML_NS:
               if name == 'head':
                  self.head = node
               elif name == 'body':
                  self.body = node
            elif node.getActualNamespace() == SPUGWEB_NS and \
	         name == 'element':
               dep = self._request.getPropertyDependency(node['property'], None)
               if dep is not None:
                  assert isinstance(dep, Dependency), node['property']
                  self.dependents.append(dep)

	 return XMLElemlet.Seeker.__call__(self, node)

      def _transform(self, name, node):
         if name == 'content':
            list = self.content
         elif name == 'title':
            list = self.title
         else:
            return 0

         parent = node.getParent()
         list.append(XMLDocWrapper.NodeSlot(parent, 
                                            parent.index(node)
                                            )
                     )
         return 1      

   def __init__(self, request, doc, dep):
      """
         parms:
            request::
               [@Request]
            doc::
               [@spug.web.xml.Element] document root.  If not provided,
               the document is obtained from the xmldocwrapper.file
            dep::
               [@Dependency] A dependent object for the document source.
      """            
      # construct the base class with our own seeker
      seeker = self.Seeker(request)
      XMLElemlet.__init__(self, request, doc, seeker)
      
      # store title and content positions
      self.__title = seeker.title
      if seeker.content:
         self.__content = seeker.content
      else:
         self.__content = None

      # store head and body nodes
      self.head = seeker.head
      self.body = seeker.body
      self.dependents = [dep] + seeker.dependents
      
   def setParcel(self, parcel):
      if self.__content:
         self.__content[0].replace(parcel)
   
   def setTitle(self, title):
      for item in self.__title:
         item.replace(title)
   
   def getDependentsTimestamp(self, request):
      ts = 0
      for dep in self.dependents:
         ts = max(dep.getTimestamp(request), ts)
      return ts

class XMLDocWrapperFactory(XMLElemletFactory):
   """
      Factory class for XMLDocWrapper so that the wrapper can be created
      using the XML source file, thereby reading the source file only once.
   """

   def __call__(self, request):
      return XMLDocWrapper(request, self._doc.copy(), self)

def handleRequest(rootNode, env, argv, out, resp):
   cgiReq = cgi.getRequest(env, argv, out)
   node, context, remainingPath = \
      rootNode.getNodeAtPath(env.get('PATH_INFO', ''))
   if node is None:
      node = NullNode()
      context = NodeContext(node, '')
   remainingPath = remainingPath.split('/')[1:]
   req = Request(cgiReq.args, cgiReq.env, cgiReq.query, 
                 cgiReq.path,
                 context,
                 remainingPath
                 )
   node.getPageInContext(req, resp)

# XXX arghhh! We have no way of finding the root node outside of a request
# context, so we have to "toss it over the wall" from the top-level facade
# functions.

_root = None

def doCGIRequest(rootNode):
   global _root
   _root = rootNode
   resp = Response(sys.stdout)
   try:
      handleRequest(rootNode, os.environ, sys.argv, sys.stdout, resp)
   except Exception, ex:
      resp.write(StdError.errorText(ex))

class PCGIClientHandler:

   __varRx = re.compile(r'([^=]+)=(.*)')

   def __init__(self, client, rootNode):
      self.__client = client
      self.__buffer = ''
      self.__rootNode = rootNode
   
   def readString(self):
      index = self.__buffer.find('\0')
      while index == -1:
         self.__buffer += self.__client.recv(1024)
         index = self.__buffer.find('\0')
      tmp = self.__buffer[:index]
      self.__buffer = self.__buffer[index + 1:]
      return tmp
   
   def read(self):
      while 1:
         data = self.__client.recv(1024)
         if not data:
            break
         self.__buffer += data
      
      tmp = self.__buffer
      self.__buffer = ''
      return tmp
   
   def handlePCGIRequest(self):
      thrd = threading.Thread(target = self.__handleClient)
      thrd.setDaemon(1)
      thrd.start()
   
   def __handleClient(self):
      # read the arg count
      argc = int(self.readString())
      
      # read the arg list
      argv = []
      while argc:
         argv.append(self.readString())
         argc -= 1
      
      # read the environment
      env = {}
      while 1:
         var = self.readString()
         if not var:
            break
         m = self.__varRx.match(var)
         if m:
            var = m.group(1)
            val = m.group(2)
            env[var] = val

      # create a CGI Request object      
      resp = Response(self.__client.makefile('w'))
      try:
         handleRequest(self.__rootNode, env, argv, self, resp)
      except Exception, ex:
         resp.write(StdError.errorText(ex))

      self.__client.close()

def doPCGIServer(udsPath, rootNode, udsGroup = None, udsPerm = 0777):
   """
      Launches a persistent CGI server.  Persistent CGI servers
      listen for connections on a Unix Domain Socket.  Each connection
      corresponds to a request.  The format of the data read in 
      the request consists of a header followed by the parcel.
      
      The header is a sequence of null terminated strings.  The first
      string is the number of arguments of the CGI command (argc) encoded
      in ascii.  The following argc strings are the arguments themselves.
      All subsequent strings are environment variable definitions of the
      form "name=value".  The header section is terminated with an empty
      string.
      
      The parcel section consists of all data read from standard input
      of the CGI gateway program.
      
      Data written back in the response is written to standard output
      of the CGI gateway program.
      
      parms:
         udsPath::
            [string] path to Unix Domain Socket for the server.
         rootNode::
            [@Node] root node of the directory tree
         udsGroup::
            [int or None] group (gid) of the unix domain socket.  If
            *None*, default group is used.
         udsPerm::
            [int] permissions of the unix domain socket.
   """
   global _root
   _root = rootNode

   serv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
   serv.bind(udsPath)
   serv.listen(5)
   
   # change group if necessary
   if udsGroup is not None:
      info = os.stat(udsPath)
      os.chown(udsPath, info.st_uid, udsGroup)
   
   # change permissions
   os.chmod(udsPath, udsPerm)
   
   while 1:
      client, addr = serv.accept()
      handler = PCGIClientHandler(client, rootNode)
      handler.handlePCGIRequest()

def doBuildCache(rootNode, targetBaseURL, dynamicBaseURL = None):
   """
      Builds the entire cache from all static nodes in the tree, thereby
      constructing the entire static page tree.  This is used to build
      all of the static pages in a web site.
      
      parms:
         rootNode::
            [@Node] root node of the directory tree
         targetBaseURL::
            [string] base URL of the target location.  This will be the
            base of all absolute URLs used to refer to other static pages
            within the tree.  You need not specify the full URL: the 
            path portion (starting from the first slash after host name
            and optional port number) is normally adequate.
         dynamicBaseURL::
            [string or None] base URL of all dynamic web pages in the tree.
            This will be the base of all absolute URLs referred to by
            static pages.  If *None*, attempting to link to a dynamic
            node from a static node will cause an error.
   """
   global _root
   _root = rootNode

   node, context, remainingPath = rootNode.getNodeAtPath('/')
   rootNode.buildCache(context, targetBaseURL, dynamicBaseURL)
