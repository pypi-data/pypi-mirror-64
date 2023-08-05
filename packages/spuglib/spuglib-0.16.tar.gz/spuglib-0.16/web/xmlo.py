#==============================================================================
#
#  $Id: xmlo.py 1011 2006-01-23 02:27:27Z mike $
#
"""
   This module provides object model for capturing XML documents that I think
   is superior to DOM for most purposes.
"""
#
#  Copyright (C) 2002 Michael A. Muller
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

import weakref, re, os, copy
import xml.sax
import xml.sax.handler
from cStringIO import StringIO
import cxml

class Translator:
   
   def __init__(self, rx, subst):
      self.rx = re.compile(rx)
      self.subst = subst
   
   def sub(self, match):
      return self.subst.get(match.group())
   
   def translate(self, data):
      return self.rx.sub(self.sub, data)

_sqAttrTrans = \
   Translator(r"[<>&']", 
              {'<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;'}
              )

_dqAttrTrans = \
   Translator(r'[<>&"]', 
              {'<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;'}
              )

_charsTrans = \
   Translator(r'[<&>]',
              {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
              )

def encodeAsAttrVal(data):
   if '"' in data and "'" not in data:
      outer = "'"
      xlate = _sqAttrTrans
   else:
      outer = '"'
      xlate = _dqAttrTrans
   return outer + xlate.translate(data) + outer

def encodeChars(data):
   return _charsTrans.translate(data)

class _RenderingOptions:
   """
      Contains XML rendering options.  Instances of this class are used
      internally by the @Element rendering functions.
   """
   
   def __init__(self, indent = 0, indentContent = 0):
      self.indent = indent
      self.indentContent = indentContent

class Element:
   """
      Representation of an XML element.  Attributes can be accessed using
      the dictionary interface, child elements can be accessed using the
      sequence interface.
      
      When accessing attributes, either a string or a tuple of two strings
      may be used as an accessor: if a tuple of two strings is used, the
      first string is the namespace and the second string is the name.  A 
      single string refers to an attribute without any namespace.
   """
   
   def __init__(self, *parms, **kw):
      """
         parms:
            /parms/::
               [tuple<string or tuple<string, string>, string or Element...>] 
	       The tag name and its children.

	       "parms" must contain at least one item, the element name.  This
	       was originally a separate argument, but the choice of a name
	       for it ("name") conflicted with the commonly used "name"
	       attribute passed in through "kw".  Since any identifier could
	       have such an issue, it was decided that the best way to avoid
	       this was to hide it as the first element of "parms".

	       The element name is either a simple name or a combination of
	       namespace URI and simple name.  If it is a simple name, the
	       namespace is assumed to be that of the enclosing element.

	       The child elements (the remaining arguments) can either be
	       @Element instances or strings.  If they are strings they are
	       assumed to be CTEXT.
	    kw::
	       [dict<string, string>] attributes.
      """
      # verify that we got a name and put the parameter variables the way
      # that we'd like them to be
      assert len(parms) > 0
      name = parms[0]
      parms = parms[1:]

      # the parent (a weakref.proxy of the parent element to avoid reference
      # cycles)
      self.__parent = None

      self.__setName(name)
      
      # create the contents list
      self.__contents = []
      for item in parms:
         item = self._fixContentItem(item)
         if isinstance(item, Element):
            item.__setParent(self)
         self.__contents.append(item)
      
      self.__elements = None            

      # construct the attribute dictionary and nsLocalNames (a mapping
      # from namespace URI to the associated local prefix)
      self.__attrs = {}
      self.__nsLocalNames = {}
      self.__nsURIs = {}
      initAttrs = kw
      for attr, val in initAttrs.items():
         self[attr] = val

   def __setParent(self, parent):
      """
         Internal method to set the parent of the element.
      """
      self.__parent = weakref.proxy(parent)

   def getNamespace(self, prefix):
      """
         Returns the namespace URI for the given prefix.  Returns None
         if no such prefix is defined.
         
         parms:
            prefix::
               [string] namespace prefix
      """
      uri = self.__nsURIs.get(prefix)
      if uri:
         return uri
      elif self.__parent:
         return self.__parent.getNamespace(prefix)
      else:
         return None

   def getFullName(self):
      """
         Returns the namespace and name of the of the element 
         (tuple<string, string>).  Note that the namespace is the 
         /specified namespace/, not the /actual namespace/.
      """
      return self.__namespace, self.__name

   def getActualNamespace(self):
      """
         Returns the actual namespace of the element name.  The "actual
         namespace" is the specified namespace if there is one, 
         it is the default namespace if there was no specified namespace.
      """
      if self.__namespace:
         return self.__namespace
      else:
         return self.getDefaultNamespace()

   def getName(self):
      """
         Returns the simple unqualified name of the element.
      """
      return self.__name

   def __setName(self, name):
      """
         Sets the full name of the element.
         
         parms:
            name::
               [tuple<string, string> or string] Either an unqualified name or
               a tuple of namespace URI and local name.
      """
      if type(name) is tuple:
         self.__namespace, self.__name = name
	 assert (isinstance(self.__namespace, (unicode, str)) or \
	    self.__namespace is None) and \
	    isinstance(self.__name, (unicode, str))
      else:
	 assert isinstance(name, str)
         self.__namespace = None
         self.__name = name
   setName = __setName

   def hasChildren(self):
      """
         Returns true if the element has child elements.
      """
      return self.getAllChildren() and 1 or 0

   def getValue(self):
      """
         Returns the value of the element as one big string.  This will
	 raise a ValueError if the element contains nested child elements.
      """
      if self.getAllChildren():
         raise ValueError('Element has nested children')
      return ''.join(self.__contents)

   def __setValue(self, newValue):
      """
         Deletes all current contens of the element, and replaces it with
         the new value.
         
         parms:
            newValue::
               [string]
      """
      self.__contents = [newValue]
      self.__elements = []
   setValue = __setValue

   def getParent(self):
      """
         Returns the parent object (actually, a proxy to the parent object), 
         *None* if there is no parent.
      """
      return self.__parent

   def getChild(self, namespace, name):
      """
         Returns the first child with the given name.  Returns None if no
         such child exists.
         
         parms:
            namespace::
               [string] namespace URI
            name::
               [string]
      """
      for elem in self.getAllChildren():
         if elem.__namespace == namespace and elem.__name == name:
            return elem
      else:
         return None
   
   def getChildren(self, namespace, name):
      """
         Returns all children with the given name.

         parms:
            namespace::
               [string] namespace URI
            name::
               [name]
      """
      result = []
      for elem in self.getAllChildren():
         if elem.__namespace == namespace and elem.__name == name:
            result.append(elem)
      return result
   
   def getAllChildren(self):
      """
         Returns all child elements (list<@Element>).  This actually returns
	 a reference to an internal list, so the caller should not modify
	 the value returned.
      """
      if self.__elements is None:
         # extract the elements from contents and set the parent of each child 
         # element
         self.__elements = \
            [item for item in self.__contents if isinstance(item, Element)]
      return self.__elements

   def hasContents(self):
      """
         Returns true if the element has contents (children or character
         data).
      """
      return self.__contents and 1

   def getDefaultNamespace(self):
      """
         Returns the default namespace URI for the node (string or None,
         None means that the default namespace is the global namespace).
      """
      return self.getNamespace(None)

   def getPrefix(self, uri):
      """
         Returns the namespace prefix for the given URI.  Returns
         None if no prefix is found for this URI.
         
         parms:
            uri::
               [string] namespace URI to find the prefix for
      """
      prefix = self.__nsLocalNames.get(uri)
      if prefix:
         return prefix
      elif self.__parent:
         return self.__parent.getPrefix(uri)
      else:
         return None

   def __getitem__(self, accessor):
      """
         Gets the specified attribute or content item, depending on whether
         /accessor/ is a string (or tuple) or integer.
         
         parms:
            accessor::
               [string or tuple<string, string> or int] If this is a string
               or tuple, returns the associated attribute.  If it is an 
               integer, returns the associated content item.
               
               If this is a single string, returns the value of an attribute
               in the global namespace.  If it is a tuple of two strings,
               the first string is a namespace URI.
               
               If this is an integer, returns the value of a child element.
               Interspersed text is ignored.
      """
      if type(accessor) is int:
         return self.__contents[accessor]
      elif type(accessor) is tuple:
         return self.__attrs[accessor]
      elif type(accessor) is str:
         return self.__attrs[None, accessor]
      else:
         raise KeyError(accessor)
   
   def get(self, attr, default = None):
      if type(attr) is tuple:
         return self.__attrs.get(attr, default)
      else:
         return self.__attrs.get((None, attr), default)
   
   def setdefault(self, attr, default):
      return self.__attr.setdefault(attr, default)

   def has_key(self, attr):
      """
         Returns true if the element has the given attribute.
         
         parms:
            attr::
               [string or tuple<string, string>] attribute to check for.
      """
      if type(attr) is str:
         return self.__attrs.has_key((None, attr))
      else:
         return self.__attrs.has_key(attr)

   def index(self, item):
      """
         Returns the index of the item within the contents list (an integer).
         
         parms:
            item::
               [string or @Element]
      """
      return self.__contents.index(item)

   def __len__(self):
      """
         Returns the number of content nodes in the element.
      """
      return len(self.__contents)

   def __nonzero__(self):
      """
         Because we define "len", we have to define this to always return
         true so that all instances of @Element are considered "true".
      """
      return 1

   # --- insertion methods ---
   # Note: everything that modifies content elements should set __elements to 
   #       None.
   #       All insertion methods should call _fixContentItem() (and 
   #       __setParent() if the item inserted is an element)

   def _fixContentItem(self, item):
      """
         Performs any necessary transforms on a new piece of content
         to be inserted.  The base class implementation returns the item.
         
         Derived classes may override this to perform arbitrary transforms
         on new children.
      """
      return item

   def __setitem__(self, accessor, value):
      if type(accessor) is int:
      
         value = self._fixContentItem(value)
         
         # clear the
         if accessor < len(self.__contents):
            oldItem = self.__contents[accessor]
         else:
            oldItem = None
         
         # store the new item
         self.__contents[accessor] = value
      
         # if it's an element, set the parent and invalidate the element
         # list
         if isinstance(value, Element):
            value.__setParent(self)
            self.__elements = None      
         
         # if the old item is an element, clear its parent
         if oldItem:
            oldItem.__parent = None
         
      elif type(accessor) is tuple:
         # if the namespace is "xmlns", store this as a namespace
         # identifier
         if accessor[0] == 'xmlns':
            self.__nsLocalNames[value] = accessor[1]
            self.__nsURIs[accessor[1]] = value
         else:         
            self.__attrs[accessor] = value
         
      else:
         # if the attribute is "xmlns", store this as the default namespace
         if accessor == 'xmlns':
         
            # handle the special case of an empty URI, which resets
            # the default namespace to the global namespace
            if value == '':
               value = None
            
            self.__nsLocalNames[value] = None
            self.__nsURIs[None] = value
         else:
            self.__attrs[None, accessor] = value

   def append(self, val):
      """
         Appends a new element or text string to the contents of the element.
         
         parms:
            val::
               [string or @Element]
      """
      val = self._fixContentItem(val)
      if isinstance(val, Element):
         self.__elements = None
         val.__setParent(self)
      self.__contents.append(val)

   def insert(self, index, val):
      val = self._fixContentItem(val)
      self.__contents.insert(index, val)
      if isinstance(val, Element):
         self.__elements = None
         val.__setParent(self)

   # --- delete methods ---
   
   def deleteItem(self, index):
      """
         Deletes the item at the specified index from the contents.
         The more "correct" way to do this is through `__delitem__`:
         i.e. "#del node[index]#".  However, in Python 2.2.3, doing this
         to a proxy (as return from the @getParent() method) causes
         a *SystemError* due to a bug in the weak reference code.
      """
      val = self.__contents[index]
      if isinstance(val, Element):
         self.__elements = None
      
      del self.__contents[index]
   
   def __delitem__(self, accessor):
      if isinstance(accessor, int):
         self.deleteItem(acceessor)
      elif isinstance(accessor, tuple):
         if accessor[0] == 'xmlns':
            del self.__nsLocalNames[self.__nsURIs[accessor[1]]]
            del self.__nsURIs[accessor[1]]
         else:
            del self.__attrs[accessor]
      else:
         if accessor == 'xmlns':
            del self.__nsLocalNames[self.__nsURIs[None]]
            del self.__nsURIs[None]
         else:
            del self.__attrs[None, accessor]

   __blankLine = re.compile(r'\s*\n')
   __wsRx = re.compile(r'\s*')

   def strip(self, stripContent = 0):
      """

         Strips all "unnecessary" whitespace from the element and all nested
	 elements.  Unncessary whitespace is whitespace between child
	 elements - when using XML for structured data representation, 
         this is usually just for formatting.

         parms:
            stripContent::
               [boolean] if true, indicates that indentation of content
               elements (nodes with no nested children
      """

      def reformat(text):
         # if the first line isn't empty, don't reformat
         if not self.__blankLine.match(text):
            return text
         
         # split up into lines, discard the first line, and find the line with
         # the least indentation.
         lines = [line.expandtabs() for line in text.split('\n')[1:]]
         minIndent = -1
         for line in lines:
            # ignore lines with no content...
            if line.strip():
               m = self.__wsRx.match(line)
               indent = len(m.group(0))
               if minIndent == -1 or indent < minIndent:
                  print 'setting indent to %d for %s' % (indent, repr(line))
                  minIndent = indent
         
         # if minIndent hasn't changed, there can't be any content!
         if minIndent == -1:
            return ''
         
         # remove up to the minimal level of indentation
         newLines = []
         for line in lines:
            
            # convert empty lines to just newline
            if not line.strip():
               newLines.append('')
               
            # truncate indentation of non-empty lines
            else:
               newLines.append(line[minIndent:])
         
         return '\n'.join(newLines)
                  
      def addText():
         """
            Adds last text between children to the newContents list.  This
            can only be used for text interspersed between child elements
            since it always removes and ignores text consisting entirely
            of whitespace.
         """
         if not lastText.strip():
            return i, ''
         elif stripContent:
            newText = reformat(lastText)
         else:
            newText = lastText
         print 'adding text %s' % repr(newText)
         newContents.append(newText)
         newI = i + 1
         newText = ''
         return newI, newText
      
      if not self.hasChildren() and stripContent:
         self.__setValue(reformat(self.getValue()))
      else:
         i = 0
         newContents = []
         lastText = ''
         for item in self.__contents:
            # if the item is an element, change its index and add it
            if isinstance(item, Element):
               if lastText:
                  i, lastText = addText()
               item.__index = i
               i += 1
               newContents.append(item)
               
               # descend into the child
               item.strip(stripContent)
            
            # if the item is an empty string, discard it
            elif type(item) is str and item.strip() == '':
               pass
            
            # otherwise just add the string value to the current text
            else:
               lastText += item
         
         # add any trailing text
         if lastText:
            i, lastText = addText()
         
         # reset contents
         self.__contents = newContents      

   def stripEmptyContents(self):
      """
         If the element contents consists of nothing but whitespace, deletes
         all contents.  Otherwise makes no changes to the element.
         
         Returns true if contents were removed, false if not.
         
         This can used to "clean out" whitespace content after removing a
         child element.
      """
      for item in self.__contents:
         if not isinstance(item, str) or item.strip():
            return 0
      self.__contents = []
      return 1
   
   def _getNSDict(self):
      """
         Constructs the namespace-URI to prefix dictionary for this node from
         the local dictionary and all ancestors.
      """
      
      # get the parent dictionary or create a new dict
      if self.__parent:
         dict = self.__parent._getNSDict()
      else:
         dict = {}
      
      # update (and override) with the local information
      dict.update(self.__nsLocalNames)

      return dict

   def __insureNSPrefix(self, nsLocalNames, uri):
      """
         Insures that the give URI has a prefix defined.  Returns the
         prefix.
      """
      # if we have a namespace, make sure that the namespace has an
      # entry within the prefix table
      if uri and not nsLocalNames.has_key(uri):
      
         # generate a unique prefix for the namespace
         i = 0
         while 'ns%d' % i in nsLocalNames.values():
            i += 1
         
         prefix = 'ns%d' % i
         nsLocalNames[uri] = prefix
         self.__nsLocalNames[uri] = prefix
         self.__nsURIs[prefix] = uri
         return prefix
      else:
         return nsLocalNames.get(uri)

   def _writeStartTag(self, output, nsLocalNames, options):
      """
         Writes the beginning of the start tag (up to the closing ">" or "/>")
         and returns the namespace prefix.
      """
      output.write('<')
      
      # get the namespace prefix
      prefix = self.__insureNSPrefix(nsLocalNames, self.__namespace)
      if prefix:
         output.write(prefix + ':')
      
      output.write(self.__name)
      
      # write all of the attributes
      for (ns, attr), val in self.__attrs.items():
         if ns:
	    attrPrefix = self.__insureNSPrefix(nsLocalNames, ns)
            output.write(' %s:%s=%s' % 
			  (attrPrefix, attr, encodeAsAttrVal(str(val)))
			 )
         else:
            output.write(' %s=%s' % (attr, encodeAsAttrVal(str(val))))
      
      # write all namespace definitions
      self._writeNamespaceDefs(output, nsLocalNames, options)
   
      return prefix      

   def _writeNamespaceDefs(self, output, nsLocalNames, options):
      for pfx, uri in self.__nsURIs.items():
         if not pfx:
            output.write(' xmlns=%s' % encodeAsAttrVal(uri))
         else:
            output.write(' xmlns:%s=%s' % (pfx, encodeAsAttrVal(uri)))

   def _writeContents(self, output, nsLocalNames, options, curIndent):
      """
         Writes the elements contents, returns true if we ended on a newline.
      """
      if options.indent:
         childIndentLevel = curIndent + options.indent
         childIndentStr = '\n' + childIndentLevel * ' '
      else:
         childIndentLevel = 0
      gotNewline = 0

      # write contents         
      for item in self.__contents:
         if isinstance(item, Element):
            tempNSMap = nsLocalNames.copy()
            tempNSMap.update(item.__nsLocalNames)
            item._writeTo(output, tempNSMap, options, childIndentLevel)
            gotNewline = 1
         else:
         
            newlineInContent = '\n' in item
         
            # only indent content if we are supposed to and either
            # it is multi-line content or there is content interspersed
            # with elements
            if options.indentContent and (self.__elements or newlineInContent):
               output.write(childIndentStr)
               
               # split into lines and remove the trailing line (so we don't
               # add an extra indent
               childLines = item.split('\n')
               if childLines[-1] == '':
                  del childLines[-1]
               
               # reconstruct the item with embedded indentation
               item = childIndentStr.join(childLines)
               gotNewline = 1
            elif newlineInContent:
               gotNewline = 1
            output.write(encodeChars(str(item)))
      return gotNewline

   def _writeTo(self, output, nsLocalNames, options, curIndent = 0):
      """
         Internal writeTo method.
      """
      if options.indent:
         indenter = '\n' + curIndent * ' '
         output.write(indenter)
      
      prefix = self._writeStartTag(output, nsLocalNames, options)
      
      # if there are no contents, we're done.  Otherwise, write the contents
      # and end tag
      if not self.__contents:
         output.write('/>')
      else:
         output.write('>')
         gotNewline = self._writeContents(output, nsLocalNames, options,
                                          curIndent
                                          )
         
         # indent for the end tag (if necessary)
         if options.indent and gotNewline:
            output.write(indenter)
         
         # write the end tag
         if prefix:
            output.write('</%s:%s>' % (prefix, self.__name))
         else:
            output.write('</%s>' % self.__name)

   def writeTo(self, output):
      """
         Writes the element to the given output stream.
         
         parms:
            output::
               [file.write]
      """
      nsLocalNames = self._getNSDict()
      self._writeTo(output, nsLocalNames, _RenderingOptions())
   
   def toSparseStr(self):
      """
         Returns the element written to a string (uses writeTo()).
      """
      out = StringIO()
      self.writeTo(out)
      return out.getvalue()

   def formatTo(self, output, indentContent = 0, indent = 2):
      """
         Writes the element to the given output stream, indenting nested
         elements.
         
         parms:
            output::
               [file.write] output stream
            indentContent::
               [boolean] if true, multiline content is indented.
            indent::
               [int] number of characters to indent children
      """
      nsLocalNames = self._getNSDict()
      self._writeTo(output, nsLocalNames, 
                    _RenderingOptions(indent, indentContent)
                    )
   
   def toFormattedStr(self):
      """
         Returns the element formatted to a string (uses formatTo()).
      """
      out = StringIO()
      self.formatTo(out)
      return out.getvalue()
   
   def __str__(self):
      """
         Stringizer that defaults to using toFormattedStr().
      """
      return self.toFormattedStr()

   def _copyInst(self):
      """
         Creates and returns a basic copy of the object (an empty element
         where only the name is actually copied.
         
         Derived classes should override this if they do not provide a
         constructor which accepts only the element name.
      """
      return self.__class__(self.getFullName())

   def copy(self):
      """
         Returns a deep copy of the element.
      """
      # create a new instance of the class
      elem = self._copyInst()
      
      # copy the namespace dictionaries
      elem.__nsLocalNames = self.__nsLocalNames.copy()
      elem.__nsURIs = self.__nsURIs.copy()
      
      # ... and the attributes
      elem.__attrs = self.__attrs.copy()
      
      # finally, copy and append all contents
      for item in self.__contents:
         if isinstance(item, Element):
            elem.append(item.copy())
         else:
            elem.append(item)
      
      return elem

   # options for content tree iteration
   EXPAND = 1
   CONTINUE = 2
   ABORT = 3

   def iterate(self, explorer):
      """
         Selectively iterates over the tree using the given explorer in 
         a depth-first traversal.
         
         parms:
            explorer::
               [callable<any>] This object will be called for the node.
               The value it returns indicates how the iteration proceeds.
               The following return values are allowed:
               
                  EXPAND::
                     Iterate over the children of the node.
                  CONTINUE::
                     Do not iterate over the children of the node, continue
                     iteration with the next node in the parent's child list.
                  ABORT::
                     Abort iteration.
      """
      action = explorer(self)
      if action in (self.ABORT, self.CONTINUE):
         return action
      
      for child in self.__contents:
         if isinstance(child, Element):
            action = child.iterate(explorer)
         else:
            action = explorer(child)
         
         if action == self.ABORT:
            return self.ABORT

class RawText(Element):
   """
      Container for raw, pre-encoded XML.  Can be used to embed existing XML 
      elements unescaped into an Element document.
   """

   def __init__(self, contents):
      Element.__init__(self, 'raw', contents)

   def _writeTo(self, output, nsLocalNames, options, curIndent = 0):
      output.write(self[0])

class ContentHandler(xml.sax.handler.ContentHandler):
   """
      Content handler to parse an Element from an XML document.
   """
   
   def __init__(self, elementFactory):
      xml.sax.handler.ContentHandler.__init__(self)
      self.__stack = []
      self.__nsMap = {}
      self.__elemFact = elementFactory

   def startElement(self, name, attrs):
      elem = self.__elemFact.makeElement(name, None)

      # store all attributes
      for name, val in attrs.items():
         elem[None, name] = val

      self.__startAnyElem(elem)
         
   def startElementNS(self, name, qname, attrs):
   
      # actual namespace is always the first element of the name tuple
      actualNS = name[0]
      
      # explicit namespace is the actual namespace if the element is qualified
      if qname and ':' in qname:
         elem = self.__elemFact.makeElement(name, actualNS)
      else:
         elem = self.__elemFact.makeElement(name[1], actualNS)
      
      # store all attributes
      for (ns, name), val in attrs.items():
         elem[ns, name] = val

      self.__startAnyElem(elem)

   def __startAnyElem(self, elem):
      "Common code for both startElement funcs"
      # add all of the namespace mappings for the element
      for prefix, uri in self.__nsMap.items():
         if prefix:
            elem['xmlns', prefix] = uri
         else:
            elem['xmlns'] = uri
      
      # clear the namespace map for the next node
      self.__nsMap = {}
      
      if self.__stack:
         self.__stack[-1].append(elem)
      self.__stack.append(elem)
      
   def startPrefixMapping(self, prefix, uri):
      self.__nsMap[prefix] = uri

   def endElement(self, name):
      self.endElementNS(name, None)
   
   def endElementNS(self, name, namespace):
      elem = self.__stack.pop(-1)
      if not self.__stack:
         self.gotDocNode(elem)

   def characters(self, chars):
      if self.__stack:
         self.__stack[-1].append(chars)

   def gotDocNode(self, elem):
      """
         Called when the top-level document element is completely parsed.
      
         This may be overriden by derived classes: derived classes choosing
         to override it should call the base class version so that
         getDocNode() remains useable.
         
         parms:
            elem::
               [@Element] the root element of the document
      """
      self.__root = elem

   def getDocNode(self):
      """
         Returns the root element of the document.  Returns *None* if the
         document has not been completely parsed.
      """
      return self.__root

def loadXML(fileName, elementFactory = None, fileType = None):
   """
      Loads an XML or CXML file given a filename.  Returns the document
      object (an @Element).
   
      parms:
         fileName: [str] name of the file to load.
         elementFactory: [@spug.web.cxml.ElementFactory or None] object used 
            to create elements.  If *None*, the 
            @spug.web.cxml.DefaultElementFactory is used.
         fileType: [str or None] If specified, this is the type of file 
            (should be "xml" or "cxml").  If unspecified, the file extension 
            must be one of those strings.
         

   """
   if elementFactory is None:
      elementFactory = cxml.DefaultElementFactory()
   
   # get the fileType from the extension
   if not fileType:
      base, ext = os.path.splitext(fileName)
      fileType = ext[1:]

   if fileType == 'cxml':
      parser = cxml.ElementParser(open(fileName), elementFactory)
      parser.parse()
      root = parser.getRootElem()
   elif fileType == 'xml':
      parser = xml.sax.make_parser()
      handler = ContentHandler(elementFactory)
      parser.setContentHandler(handler)
      parser.setFeature(xml.sax.handler.feature_namespaces, 1)
      parser.setFeature(xml.sax.handler.feature_external_ges, False)
      parser.parse(open(fileName))
      root = handler.getDocNode()
   else:
      raise Exception('%s does not have aknown XML file extension' % fileName)
   return root

if __name__ == '__main__':
   import sys  
   ns = 'http://www.mindhog.net/test'
   e = Element((ns, 'foo'),
         Element('bar', test = 'first'),
         Element('bar', 'contents'),
         )
   e['xmlns', 'foo'] = ns
   e.writeTo(sys.stdout)
   print '-' * 78

   class TestContentHandler(ContentHandler):
      
      def gotDocNode(self, elem):
         ContentHandler.gotDocNode(self, elem)
         elem.writeTo(sys.stdout)
	 

   src = StringIO('''<?xml version="1.0"?>
      <test xmlns='http://www.mindhog.net/test'>
         <foo:bar foo:test='someval' xmlns:foo='http://www.mindhong.net/foo' >
            <foo:goo>this is sweet</foo:goo>
            <xxx attr="&quot;attribute">some funky characters: &amp; &gt; &lt; '"></xxx>
         </foo:bar>
      </test>
   ''')

   parser = xml.sax.make_parser()
   parser.setContentHandler(TestContentHandler(cxml.DefaultElementFactory()))
   parser.setFeature(xml.sax.handler.feature_namespaces, 1)
   parser.parse(src)

   print '-' * 78

   src = StringIO('''<?xml version="1.0"?>
      <test>
         <bar test="ain&apos;t that sweet?">
            <goo>this is sweet!</goo>
            <xxx attr='holy friggin crap!'>some stuff</xxx>
         </bar>
      </test>''')

   parser = xml.sax.make_parser()
   parser.setContentHandler(TestContentHandler(cxml.DefaultElementFactory()))
   parser.parse(src)

   # straightforward tests
   elem = Element('foo', '   ', '\n', '\t')   
   if not elem.stripEmptyContents() or len(elem):
      print 'ERROR: stripEmptyContents() did not do its job'
   for elem in (Element('foo', '   ', 'test', '\n'),
                Element('foo', '   ', Element('bar'), '\t')
                ):
      if elem.stripEmptyContents() or not len(elem):
         print 'ERROR: stripEmptyContents() stripped a non-empty element'

   # bug-fix test - attribute prefix was being used for end-tag
   elem = Element('outer')
   elem['xmlns', 'foo'] = 'uri:foo'
   elem['uri:foo', 'test'] = 'attrib value'
   elem.append('some text')
   dst = StringIO()
   elem.formatTo(dst)
   assert dst.getvalue().strip() == '<outer foo:test="attrib value" ' \
      'xmlns:foo="uri:foo">some text</outer>'
