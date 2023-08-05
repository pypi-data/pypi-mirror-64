#==============================================================================
#
#  $Id: htmlo.py 1011 2006-01-23 02:27:27Z mike $
#
"""
   New HTML Object Model based on @spug.web.xmlo objects.
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

from xmlo import Element, _RenderingOptions
from cxml import ElementFactory

# The XHTML namespace
XHTML_NS = 'http://www.w3.org/1999/xhtml'

class _HTMLRenderingOptions(_RenderingOptions):

   def __init__(self, indent = 0, indentContent = 0, xhtml = 0):
      _RenderingOptions.__init__(self, indent, indentContent)
      self.xhtml = xhtml

class HTMLElement(Element):
   # indicates that the tag can be used without an end tag
   _monoTag = 0

   def _copyInst(self):
      """
         We override @HTMLElement._copyInst() because constructors don't
         accept a name parameter.
      """
      return self.__class__()

   def __init__(self, *parms, **kw):
      Element.__init__(self, self._tag, *parms, **kw)

   def _writeNamespaceDefs(self, output, nsLocalNames, options):
      """
         Overrides namespace definition output so we can eliminate
         namespace definitions for plain HTML.
      """
      # if "options" is not our HTMLRenderingOptions, we can assume that we
      # have been invoked from an XML node must therefore generate XHTML.
      # Otherwise decide based on the xhtml attribute
      if not isinstance(options, _HTMLRenderingOptions) or options.xhtml:
         Element._writeNamespaceDefs(self, output, nsLocalNames, options)

   def _writeTo(self, output, nsLocalNames, options, curIndent = 0):
      """
         Overrides @spug.web.xml.Element.writeTo() to provide for HTML's
         funky output rules
      """
      if options.indent:
         indenter = '\n' + curIndent * ' '
         output.write(indenter)
      
      prefix = self._writeStartTag(output, nsLocalNames, options)
      
      # if we're not in XHTML mode and this is a mono tag, we can just
      # render the end of it
      gotContents = self.hasContents()
      if not gotContents and not options.xhtml and self._monoTag:
         output.write('>')
      # if we are in XHTML mode and the tag has no contents, we can end with
      # a />
      elif not gotContents and options.xhtml:
         output.write('/>')
      # otherwise, we need to generate contents and the end tag
      else:
         output.write('>')
         gotNewline = self._writeContents(output, nsLocalNames, options, 
                                          curIndent
                                          )
         
         # indent for the end tag (if necessary)
         if options.indent and gotNewline:
            output.write(indenter)
         
         # write the end tag
         name = self.getName()
         if prefix:
            output.write('</%s:%s>' % (prefix, name))
         else:
            output.write('</%s>' % name)

   def __getHTMLNSDict(self, xhtml):
      """
	 Returns the namespace dictionary (maps URI's to namespace prefices
	 for an HTMLElement.  This is 
      """
      if xhtml:
	 return self._getNSDict()
      else:
	 # for plain HTML documents, there are no namespaces.  We fake out the
	 # same effect by always defining _only one_ namespace (the XHTML ns)
	 # and mapping it to the default prefix
	 return { XHTML_NS: None }

   def writeTo(self, output, xhtml = 0):
      """
         Overrides @spug.web.xml.Element.writeTo() to provide an XHTML
         parameter.
         
         parms:
            output::
               [file.write]
            xhtml::
               [boolean] if true, node and contents will be written in
               XHTML instead of normal HTML.
      """
      nsLocalNames = self.__getHTMLNSDict(xhtml)
      self._writeTo(output, nsLocalNames, _HTMLRenderingOptions(xhtml = xhtml))

   def formatTo(self, output, indentContent = 0, indent = 2, xhtml = 0):
      """
         Overrides @spug.web.xml.Element.formatTo() to provide an XHTML 
         parameter.
         
         parms:
            output::
               [file.write] output stream
            indentContent::
               [boolean] if true, multiline content is indented.
            indent::
               [int] number of characters to indent children
            xhtml::
               [boolean] if true, node and contents will be written in
               XHTML instead of normal HTML.
      """
      nsLocalNames = self.__getHTMLNSDict(xhtml)
      self._writeTo(output, nsLocalNames, 
                    _HTMLRenderingOptions(indent, indentContent, xhtml)
                    )

   def populate(self, valueDict):
      """
	 Populates this element and all nested elements from the value
	 dictionary.

	 If there is a key in valueDict matching a "name" attribute in this
	 element, sets the value of the element in a manner appropriate to the
	 element type.

	 This method is intended to allow you to populate an entire form from
	 the values in a query dictionary.

	 The value of the element is set using the @set() method.  This
	 is what is generally overriden to vary the way control values are
	 defined.
      """
      if self.has_key('name') and valueDict.has_key(self['name']):
	 self.set(valueDict[self['name']])
      else:
	 # apply this recursively through all child elements
	 for elem in self.getAllChildren():
	    elem.populate(valueDict)

   def set(self, value):
      """
	 Sets the value of an element in the manner prescribed for the
	 element.  This is really only relevant for form controls.  The base
	 class version of this just sets the "value" attribute.  Derived
	 classes should override as appropriate.
      """
      self['value'] = value

class SingleTagElement(HTMLElement):
   _monoTag = 1

class B(HTMLElement):
   _tag = (XHTML_NS, 'b')
class U(HTMLElement):
   _tag = (XHTML_NS, 'u')
class I(HTMLElement):
   _tag = (XHTML_NS, 'i')
class OL(HTMLElement):
   _tag = (XHTML_NS, 'ol')
class UL(HTMLElement):
   _tag = (XHTML_NS, 'ul')
class LI(HTMLElement):
   _tag = (XHTML_NS, 'li')

class Table(HTMLElement):
   """
      Attributes:

	 border::
	    0 for none, 1 for a border.
   """
   _tag = (XHTML_NS, 'table')

class TR(HTMLElement):
   _tag = (XHTML_NS, 'tr')
class TH(HTMLElement):
   _tag = (XHTML_NS, 'th')

class TD(HTMLElement):
   """
      Attributes:

	 colspan::
	    Columns of the table to span.
	 rowspan::
	    Rows of the table to span.
   """
   _tag = (XHTML_NS, 'td')

class H1(HTMLElement):
   _tag = (XHTML_NS, 'h1')
class H2(HTMLElement):
   _tag = (XHTML_NS, 'h2')
class H3(HTMLElement):
   _tag = (XHTML_NS, 'h3')
class H4(HTMLElement):
   _tag = (XHTML_NS, 'h4')
class H5(HTMLElement):
   _tag = (XHTML_NS, 'h5')
class H6(HTMLElement):
   _tag = (XHTML_NS, 'h6')
class H7(HTMLElement):
   _tag = (XHTML_NS, 'h7')
class H8(HTMLElement):
   _tag = (XHTML_NS, 'h8')
class H9(HTMLElement):
   _tag = (XHTML_NS, 'h9')
class P(HTMLElement):
   _tag = (XHTML_NS, 'p')
class Body(HTMLElement):
   _tag = (XHTML_NS, 'body')
class A(HTMLElement):
   _tag = (XHTML_NS, 'a')
class Title(HTMLElement):
   _tag = (XHTML_NS, 'title')
class Head(HTMLElement):
   _tag = (XHTML_NS, 'head')
class HTML(HTMLElement):
   _tag = (XHTML_NS, 'html')
class Form(HTMLElement):
   _tag = (XHTML_NS, 'form')

class Input(SingleTagElement):
   """
      Attributes:

	 type::
	    'entry' (text entryfield), 'submit' (submit button), 'reset'
	    (reset button), 'password' (password entry field), 'hidden'
	    (hidden input), 'checkbox' (a toggleable checkbox button)
	 name::
	    Control id
	 size::
	    For 'entry' and 'password' types, this is the width of the field
	    in columns.
	 value::
	    For 'entry' and 'password' types, this is the initial text.  For
	    buttons, it is the button label.  For 'checkbox' it is the value 
	    associated with the name in the submitted query when the checkbox is 
	    checked.
   """
   _tag = (XHTML_NS, 'input')
   
   def set(self, value):
      # the checkbox gets special treatment
      if self.get('type') == 'checkbox':
         if value: self['checked'] = True
      else:
         SingleTagElement.set(self, value)

class Select(HTMLElement):
   _tag = (XHTML_NS, 'select')

   def set(self, value):
      for option in self.getAllChildren():
	 if isinstance(option, Option):
	    option.set(value)

class TextArea(HTMLElement):
   _tag = (XHTML_NS, 'textarea')

   def set(self, value):
      self.setValue(value)

class Center(HTMLElement):
   _tag = (XHTML_NS, 'center')
class Font(HTMLElement):
   _tag = (XHTML_NS, 'font')
class Option(HTMLElement):
   _tag = (XHTML_NS, 'option')

   def set(self, value):
      # if there is a value attribute, compare its value.  Otherwise, compare
      # the element contents
      if self.has_key('value'):
	 if self['value'] == value:
	    self['selected'] = 1
	    return

      # this check may be problematic - if the option contains nested elements
      # getValue() will throw an exception.  Don't think that's valid html.
      elif self.getValue() == value:
	 self['selected'] = 1
	 return

      # at this point, the object should not be selected.  If it is, turn it
      # off
      if self.get('selected', '0') != '0':
	 del self['selected']

class Script(HTMLElement):
   _tag = (XHTML_NS, 'script')
class Img(HTMLElement):
   _tag = (XHTML_NS, 'img')
class Pre(HTMLElement):
   _tag = (XHTML_NS, 'pre')
class Br(HTMLElement):
   _tag = (XHTML_NS, 'br')
class Div(HTMLElement):
   _tag = (XHTML_NS, 'div')
class Span(HTMLElement):
   _tag = (XHTML_NS, 'span')
class Em(HTMLElement):
   _tag = (XHTML_NS, 'em')
class Strong(HTMLElement):
   _tag = (XHTML_NS, 'strong')
class Link(SingleTagElement):
   _tag = (XHTML_NS, 'link')
class Style(HTMLElement):
   _tag = (XHTML_NS, 'style')


class XNull(HTMLElement):
   """
      This is a tag that simply writes out it's contents with no enclosing
      element.
   """
   _tag = 'XNull'

   def _writeTo(self, output, nsLocalNames, options, curIndent = 0):
      """
         Overrides @HTMLElement._writeTo() to emit only contents.
      """
      self._writeContents(output, nsLocalNames, options, 
                          curIndent - options.indent
                          )

class XUL(UL):
   """
      Like an unordered list, but automatically wraps all children
      that are not list items (LI) in list items.
   """
   
   def _fixContentItem(self, child):
      if type(child) in (list, tuple):
         return LI(*child)
      elif not isinstance(child, LI):
         return LI(child)
      else:
         return child

class XSelect(Select):
   """
      Just like *Select* but automatically wraps all children that are not
      Option instances as Option instances.
   """
   def _fixContentItem(self, child):
      if type(child) in (list, tuple):
         return Option(*child)
      elif not isinstance(child, Option):
         return Option(child)
      else:
         return child

class XTable(Table):
   """
      Just like a *Table* except that all children that are
      lists or tuples are automatically converted to rows, and all items in
      those lists that are not *TD*'s are converted to *TD*'s.
   """
   
   def _fixContentItem(self, item):
      if isinstance(item, (list, tuple)):
         tr = TR()
         for col in item:
            if not isinstance(col, (TD, TH)):
               col = TD(col)
            tr.append(col)
         return tr
      elif not isinstance(item, TR):
         return TR(item)
      else:
         return item

class XDoc(HTML):

   """
      A complete html document.  Consists of the outer HTML tag with an
      embedded HEAD tag and BODY tag, both of which are available as
      public variables:
      
      /head/::
         An instance of @Head which represents the HEAD tag of the
         document.
      /body/::
         An instance of @Body which represents the BODY tag of the
         document.

      All sequence and keyword arguments are passed to the BODY tag, 
      except for the following special attributes:
      
      /title/::
         A string representing the title of the document.  This will cause
         a TITLE tag to be added to the contents of the HEAD tag.
   """
      
   def __init__(self, *parms, **kw):
      self.head = Head()
      self.body = Body(*parms, **kw)
      
      HTML.__init__(self, self.head, self.body)
      
      if kw.has_key('title'):
         title = kw['title']
         del kw['title']
      else:
         title = ''
      
      if title:
         self.head.append(Title(title))
      
      # give myself the proper namespace
      self['xmlns'] = XHTML_NS

   def _writeTo(self, out, nsLocalNames, options, curIndent = 0):
      """
         Overrides @HTMLElement.writeTo() so as to prefix the output with the
         special DOCTYPE tag.
      """
      if options.xhtml:
         out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
         out.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '
                    '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
                   )
      else:
         out.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">\n')
      HTML._writeTo(self, out, nsLocalNames, options, curIndent)

class HTMLElementFactory(ElementFactory):

   def makeElement(self, name, actualNS):
      if isinstance(name, tuple):
         localName = name[1]
      else:
         localName = name
      if actualNS == XHTML_NS:
         return \
            {
            'b': B,
            'u': U,
            'i': I,
            'ol': OL,
            'ul': UL,
            'li': LI,
            'table': Table,
            'tr': TR,
            'td': TD,
            'h1': H1,
            'h2': H2,
            'h3': H3,
            'h4': H4,
            'h5': H5,
            'h6': H6,
            'h7': H7,
            'h8': H8,
            'h9': H9,
            'p': P,
            'body': Body,
            'a': A,
            'title': Title,
            'head': Head,
            'html': HTML,
            'form': Form,
            'input': Input,
            'select': Select,
            'textarea': TextArea,
            'center': Center,
            'font': Font,
            'option': Option,
            'script': Script,
            'img': Img,
            'pre': Pre,
            'br': Br,
            'div': Div,
            'span': Span,
            'em': Em,
            'strong': Strong,
            'link': Link,
            'style': Style,
            }.get(localName, lambda c=name: Element(name))()
      else:
         return Element(name)

if __name__ == '__main__':
   import sys
   doc = XDoc(H1('this is the title'), P('this is content'),
              Input(type = 'submit'),
              title = 'this is the title',
              )
#   doc['xmlns', 'html'] = XHTML_NS
   doc.formatTo(sys.stdout, xhtml = 1)
