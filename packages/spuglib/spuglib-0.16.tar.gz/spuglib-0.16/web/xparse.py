#==============================================================================
#
#  $Id$
#
"""
   This module extends the SAX parsing mechanism to permit XML document
   handling via an XML-element to method mapping.

   Example:

      NS_URI = 'http://www.mindhog.net/schemas/example.xml'

      class ItemHandler(ElemHandler):

         def __init__(self):
            self.__item = DataObject()

         @Element(uri = NS_URI, name = 'name')
         def handle_name(self, info):
            return SimpleContentHandler(self.__item.setName)

         @Element(uri = NS_URI, name = 'desc')
         def handle_desc(self, info):
            return SimpleContentHandler(self.__item.setDesc)

      class MyDocHandler(ElemHandler):

         @Element(uri = NS_URI, name = 'doc'):
         def handle_item(self, info):
            return ItemHandler()
"""
#
#  Copyright (C) 2005 Michael A. Muller
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

import xml.sax
from xml.sax.handler import ContentHandler, feature_namespaces

class Element:
   """
      This is meant to be used as a method decorator to define a mapping from
      an XML element to a method.

      Both or either of the namespace URI and the element name may be omitted
      - in this case the method name is used as the element name and the
      default namespace is used.

      Example:
      
      {{
         @Element('http://www.mindhog.net/schemas/example.xml', 'elem-name')
         def elemName(self, elemInfo):
            ...
      }}
   """

   def __init__(self, uri = None, name = None):
      self.uri = uri
      self.name = name
      self.method = None

   def __call__(self, method):
      self.method = method
      return self
   
   def getKey(self):
      return self.uri, self.name

# some trickery to get the _Function type
def _bogus(self):
   pass
_Function = type(_bogus)
del _bogus

class _NameMapper(type):
   """
      This is the metaclass for @ElemHandler.  It iterates over the @Element
      definitions in the class body and uses them to construct a dictionary.
   """

   def __new__(metaclass, name, parents, body):

      # create the element lookup dictionary XXX should merge elemMap from the
      # base classes into this
      body['_elemMap'] = elemLookup = {}

      for name, item in body.items():
         if isinstance(item, Element):
            # add the method to the lookup table
            elemLookup[item.getKey()] = item.method

            # store the method (discarding the Element decorator)
            body[item.method.__name__] = item.method
         elif name.startswith('handle_') and \
            isinstance(item, _Function):
            elemLookup[None, name[7:]] = item

      return type.__new__(metaclass, name, parents, body)

class ElemHandler:

   __metaclass__ = _NameMapper

   def characters(self, data):
      """
         Called to handle raw character content.  Derived classes may override
         this to capture character data, base class implementation does 
         nothing.
      """
      pass

   def default(self, info):
      """
         Called when a nested element is found that does not match any
         elements defined for the handler.  Derived classes may override this,
         base class implementation does nothing.
      """
      pass

   def end(self, info):
      """
         Called when the end tag of the current element is parsed.  Base class
         implementation pops the handler.

         parms:
            info::
               [@ElemInfo]
      """
      pass

class SimpleContentCollector(ElemHandler):
   """
      Collects the element character content and passes it to a function.
      Element contents must consist of character content only - if nested
      elements are discovered, a ValueError will be raised.
   """

   def __init__(self, callback):
      """
         parms:
            callback::
               [callable<string>] function that accepts a string as input.
               Used to feedback the contents of the element.
      """
      self.__callback = callback
      self.__buffer = ''
   
   def default(self, info):
      """
         Overrides @ElemHandler.default() to always raise a @ValueError when a
         nested element is discovered.
      """
      raise ValueError('Nested elements not allowed')

   def characters(self, data):
      self.__buffer += data

   def end(self, info):
      self.__callback(self.__buffer)

class ElemInfo:

   def __init__(self, uri, name, qname, attrs):
      self.uri = uri
      self.name = name
      self.qname = qname
      self.attrs = attrs

class XParseHandler(ContentHandler):
   """
      A content handler that keeps a stack tracking the nested elements in a
      document and calls methods in the currently defined @ElemHandler.

      This class basically serves as an adapter between SAX and the
      ElemHandler interface.
   """
   
   class ElemFrame:
      """
         A stack frame corresponding to an element.
      """

      def __init__(self, info, handler, bound = False):
         self.info = info
         self.handler = handler
         self.bound = bound

   def __init__(self, topHandler):
      self.__stack = [self.ElemFrame(None, topHandler, True)]

   def setHandler(self, handler):
      """
         Sets the handler for the current element and all nested elements
         until another handler is defined.  When the element's end tag is
         parsed, the handlers "end()" method will be called.
      """
      top = self.__stack[-1]
      top.handler = handler
      top.bound = True

   def startElementNS(self, name, qname, attrs):
      # split out the name into namespace URI and local name
      uri, name = name
      info = ElemInfo(uri, name, qname, attrs)

      # get the handler at the top of the stack
      handler = self.__stack[-1].handler

      # create a new stack frame
      self.__stack.append(self.ElemFrame(info, handler))

      # try to lookup a a start element callback
      startElemCallback = handler._elemMap.get((uri, name))
      if startElemCallback:
         result = startElemCallback(handler, info)
      else:
         result = handler.default(info)

      if result:
         self.setHandler(result)

   def endElementNS(self, name, qname):
      top = self.__stack.pop()
      info = top.info
      assert name == (info.uri, info.name)
      if top.bound:
         top.handler.end(info)

   def characters(self, data):
      self.__stack[-1].handler.characters(data)

def parseXML(topHandler, src):
   parser = xml.sax.make_parser()
   parser.setContentHandler(XParseHandler(topHandler))
   parser.setFeature(feature_namespaces, True)
   parser.parse(src)

if __name__ == '__main__':

   doc = '''<?xml version="1.0"?>
<doc>
   <test>This is a test</test>
   <nested>
      <test>This is a nested test</test>
   </nested>
</doc>
'''

   def callback(data):
      print('got %s' % repr(data))

   class DocHandler(ElemHandler):

      # should be registered purely by virtue of its name
      def handle_test(self, info):
         return SimpleContentCollector(callback)

      def default(self, info):
         print('in default:', info)

   class MyHandler(ElemHandler):

      @Element(name = 'doc')
      def handle_doc(self, info):
         return DocHandler()

   from StringIO import StringIO
   parseXML(MyHandler(), StringIO(doc))
