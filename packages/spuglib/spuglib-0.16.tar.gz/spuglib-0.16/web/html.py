#==============================================================================
#
#  $Id: html.py 870 2005-10-14 11:18:00Z mike $
#
"""
   This is yet another Python wrapper around HTML.
   
   This solution aims for simplicity and consistency above all else.
   All of the tag classes accept sequence and keyword arguments
   in their constructors: the sequence arguments are always placed in the 
   contents of the tag, the keyword arguments are always used as attributes
   to the tag.
   
   If a sequence argument is a list or tuple, it is recursively flattened 
   into a string.  All other arguments are stringified.
   
   Classes prefaced by the letter "X" are extensions to the basic html
   classes and do not neccessarily correspond to the rule identified above.
   Typically, they try to adhere to these rules as much as possible, and offer
   exceptions so that these objects can be easier to use.
   
   This module currently include lowercase functional forms of many of these
   classes: they exist only for backwards compatibility and their use is
   deprecated.
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
#  $Log: html.py,v $
#  Revision 1.7  2005/10/14 11:18:00  mike
#  Added some documentation
#
#  Revision 1.6  2003/06/26 14:21:19  mike
#  Added the XNull tag - allowing us to derive from sequences of content with
#  no enclosing tags.
#
#  Revision 1.5  2002/07/30 01:28:24  mike
#  Added ability to encode strings, replacing special chars with ampersand
#  codes.
#
#  Revision 1.4  2000/02/12 23:46:50  mike
#  When a value of None is given for an attribute, the attribute is not
#  emitted.
#
#  Revision 1.3  1999/12/22 01:30:55  mike
#  Added the "BR" tag
#
#  Revision 1.2  1999/10/09 18:49:49  mike
#  Added XTable, Img and Pre tags.  Added value propagation code.
#
#  Revision 1.1.1.1  1999/08/13 23:14:48  mike
#  spug-html package
#
#
#==============================================================================


import string, re
from types import ListType, TupleType, StringType, IntType

doctype = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">\n'

def _attrs(kw):
   attrStr = ''
   for attr, val in kw.items():
      if val is not None:
         attrStr = attrStr + ' %s="%s"' % (attr, val)
   return attrStr

def _str(obj):
   
   if type(obj) in (TupleType, ListType):
      return string.join(map(_str, obj))
   else:
      return str(obj)

def tag(tag, parms, kw):
   return '<%s%s>%s</%s>\n' % (tag, _attrs(kw), 
                                 string.join(map(_str, parms)),
                                 tag
                                 )

def ol(*parms, **kw):
   return tag('ol', parms, kw)

def ul(*parms, **kw):
   return tag('ul', parms, kw)

def li(*parms, **kw):
   return tag('li', parms, kw)

def table(*parms, **kw):
   return tag('table', parms, kw)

def tr(*parms, **kw):
   return tag('tr', parms, kw)

def td(*parms, **kw):
   return tag('td', parms, kw)

def h1(*parms, **kw):
   return tag('h1', parms, kw)

def h2(*parms, **kw):
   return tag('h2', parms, kw)

def h3(*parms, **kw):
   return tag('h3', parms, kw)

def h4(*parms, **kw):
   return tag('h4', parms, kw)

def h5(*parms, **kw):
   return tag('h5', parms, kw)

def h6(*parms, **kw):
   return tag('h6', parms, kw)

def h7(*parms, **kw):
   return tag('h7', parms, kw)

def h8(*parms, **kw):
   return tag('h8', parms, kw)

def h9(*parms, **kw):
   return tag('h9', parms, kw)

def p(*parms, **kw):
   return tag('p', parms, kw)

def body(*parms, **kw):
   return tag('body', parms, kw)

def a(*parms, **kw):
   return tag('a', parms, kw)

def title(*parms, **kw):
   return tag('title', parms, kw)

def head(*parms, **kw):
   return tag('head', parms, kw)

def html(*parms, **kw):
   return tag('html', parms, kw)

def form(*parms, **kw):
   return tag('form', parms, kw)

def center(*parms, **kw):
   return tag('center', parms, kw)

def font(*parms, **kw):
   return tag('font', parms, kw)

def input(*parms, **kw):
   return tag('input', parms, kw)

def x_ul(*parms, **kw):
   """
      Like "ul" only converts each positional parameter to a list item.
   """
   return apply(ul, map(li, parms), kw)
   
def x_ol(*parms, **kw):
   """
      Like "ol" only converts each positional parameter to a list item.
   """
   return apply(ol, map(li, parms), kw)
   
def x_htmldoc(*parms, **kw):
   """
      Returns a complete HTML document.  Keyword arguments all go into
      the body tag, except for the following special arguments:
      
      *title*::
         Becomes the title of the document.
   """
   if kw.has_key('title'):
      docparms = [ head(title(kw['title'])) ]
      del kw['title']
   else:
      docparms = [ head() ]
   
   docparms.append(apply(body, parms, kw))
         
   return doctype + apply(html, docparms)

def x_text(*parms, **kw):
   kw['type'] = 'text'
   return tag('input', parms, kw)

def x_submit(*parms, **kw):
   kw['type'] = 'submit'
   return tag('input', parms, kw)

def doc(*parms, **kw):
   return doctype + \
      tag('html', [ apply(body, parms, kw) ], {})


def _writeList(list, dest):
   for item in list:
      if isinstance(item, Tag):
         item.writeOn(dest)
      elif type(item) in (ListType, TupleType):
         _writeList(item, dest)
      else:
         dest.write(str(item))

class Tag:
   
   """
      This is, IMHO, the ultimate representation of an HTML (or XML) construct.
      
      An HTML tag can be represented by the tag itself, its attributes,
      and its contents.
      
      It is up to the derived classes to provide the tag by defining the
      #`_tag`# variable at the class level.
      
      Attributes and contents (which we are calling /items/) can be
      manipulated using the types of methods that we normally use to 
      manipulate dictionaries and lists.
      
      Attributes and items can be passed in at the time of construction using
      the keyword parameters and positional parameters, respectively.
      
      The bracket operators (#`__setitem__`#, #`__getitem__`# and 
      #`__delitem__`#) refer to either an attribute or an item depending
      on whether the value in the brackets is a string or an integer.
      
      If the value is an integer, then the operator is being used to index
      an item.  If it is a string, then it refers to an attribute.
      
      Normally, attribute values are quoted and emitted as part of the
      attribute list of the tag when @writeOn() or @__str__() is invoked.
      However, as a special exception, if the value is *None*, neither
      the attribute name or value is emitted.  This allows you to "turn off"
      boolean attributes by specifying a value of *None*.
   """
   
   def __init__(self, *parms, **kw):
      self.__items = list(parms)
      self.__attrs = kw

   def _writeItems(self, out):
      _writeList(self.__items, out)
   
   def writeOn(self, writeable):
      writeable.write('<%s%s>' % (self._tag, _attrs(self.__attrs)))
      self._writeItems(writeable)
      writeable.write('</%s>\n' % self._tag)

   def __str__(self):
      return tag(self._tag, self.__items, self.__attrs)
      
   def append(self, item):
      self.__items.append(item)
   
   def __setitem__(self, key, val):
      if type(key) is StringType:
         self.__attrs[key] = val
      elif type(key) is IntType:
         self.__items[key] = val
      else:
         raise ValueError('Key must be a string or an integer.')

   def __getitem__(self, key):
      if type(key) is StringType:
         return self.__attrs[key]
      elif type(key) is IntType:
         return self.__items[key]
      else:
         raise ValueError('Key must be a string or an integer.')

   def __delitem__(self, key):
      if type(key) is StringType:
         del self.__attrs[key]
      elif type(key) is IntType:
         del self.__items[key]
      else:
         raise ValueError('Key must be a string or an integer.')

   def __len__(self):
      return len(self.__items)

   def has_key(self, key):
      return self.__attrs.has_key(key)

   def __delslice__(self, start, end):
      del self.__items[start:end]

   def getValue(self, dict):
      """
         If the tag has a "name" attribute, and there is a key in the 
         dictionary /dict/ of this name, this method will assign
         the value in the dictionary to the value of the Tag.
         
         "Value of the tag" means whatever is appropriate for the tag, 
         usually it means setting the tags "value" attribute, so that
         is the default behavior.  Tags wishing to override this behavior
         should override the @_setValue() method.
         
         The recommended use of this is to easily extract information
         from a CGIRequest's "query" dictionary.
         
         This method will recurse through all nested html objects.
      """
      if  self.__attrs.has_key('name') and \
          dict.has_key(self.__attrs['name']):
         self._setValue(dict[self.__attrs['name']])
      for item in self.__items:
         if isinstance(item, Tag):
            item.getValue(dict)

   def _setValue(self, value):
      self.__attrs['value'] = value

class B(Tag):
   _tag = 'B'
class U(Tag):
   _tag = 'U'
class I(Tag):
   _tag = 'I'
class OL(Tag):
   _tag = 'OL'
class UL(Tag):
   _tag = 'UL'
class LI(Tag):
   _tag = 'LI'
class Table(Tag):
   _tag = 'Table'
class TR(Tag):
   _tag = 'TR'
class TD(Tag):
   _tag = 'TD'
class H1(Tag):
   _tag = 'H1'
class H2(Tag):
   _tag = 'H2'
class H3(Tag):
   _tag = 'H3'
class H4(Tag):
   _tag = 'H4'
class H5(Tag):
   _tag = 'H5'
class H6(Tag):
   _tag = 'H6'
class H7(Tag):
   _tag = 'H7'
class H8(Tag):
   _tag = 'H8'
class H9(Tag):
   _tag = 'H9'
class P(Tag):
   _tag = 'P'
class Body(Tag):
   _tag = 'Body'
class A(Tag):
   _tag = 'A'
class Title(Tag):
   _tag = 'Title'
class Head(Tag):
   _tag = 'Head'
class HTML(Tag):
   _tag = 'HTML'
class Form(Tag):
   _tag = 'Form'
class Center(Tag):
   _tag = 'Center'
class Font(Tag):
   _tag = 'Font'
class Option(Tag):
   _tag = 'option'
class Script(Tag):
   _tag = 'script'
class Img(Tag):
   _tag = 'img'
class Pre(Tag):
   _tag = 'pre'
class Br(Tag):
   _tag = 'br'
class Div(Tag):
   _tag = 'div'
class Span(Tag):
   _tag = 'span'

class Select(Tag):
   _tag = 'select'
   
   def _setValue(self, value):
      for option in self:
         if isinstance(option, Option):
            if option.has_key('value') and option['value'] == value:
               option['selected'] = '1'
            elif len(option) == 1 and option[0] == value:
               option['selected'] = '1'
            else:
               if option.has_key('selected'):
                  del option['selected']

class Input(Tag):
   """
      Attributes:

	 type::
	    'entry' (text entryfield), 'submit' (submit button), 'reset'
	    (reset button), 'password' (password entry field), 
	 name::
	    Control id
	 size::
	    For 'entry' and 'password' types, this is the width of the field
	    in columns.
	 value::
	    For 'entry' and 'password' types, this is the initial text.  For
	    buttons, it is the button label.
   """
   _tag = 'Input'

   def _setValue(self, value):
      if  self.has_key('type') and \
          self['type'] == 'checkbox':
         self['checked'] = value
      else:
         Tag._setValue(self, value)

class TextArea(Tag):
   _tag = 'textarea'
   
   def _setValue(self, value):
      del self[:]
      self.append(value)
   
class XNull(Tag):
   """
      This is a tag that simply writes out it's contents with no enclosing
      element.
      
      For the most part, this function can be served by passing lists into
      the constructor parameters and element insert methods.  The XNull
      class is mainly to allow derived classes to do funky things.
   """
   
   def writeOn(self, out):
      self._writeItems(out)
   
   def __str__(self):
      return string.join(map(_str, parms))

class XUL(UL):
   """
      Like an unordered list, but automatically wraps all sequence
      parameters that are not list items (LI) in list items.
   """
   def __init__(self, *parms, **kw):
      newParms = []
      for p in parms:
         if not isinstance(p, LI):
            p = LI(p)
         newParms.append(p)
      apply(UL.__init__, (self,) + tuple(newParms), kw)

class XText(Input):

   def __init__(self, *parms, **kw):
      kw['type'] = 'text'
      apply(Input.__init__, (self,) + parms, kw)

class XSubmit(Input):
   
   def __init__(self, *parms, **kw):
      kw['type'] = 'submit'
      apply(Input.__init__, (self,) + parms, kw)

class XSelect(Select):
   """
      Just like *Select* except that all constructor parameters that
      are strings are automatically translated to Option instances.
      
      No such transformations are attempted on the append and 
      `__setitem__` methods.
   """
   def __init__(self, *parms, **kw):
      choices = []
      for p in parms:
         if type(p) is StringType:
            choices.append(Option(p))
         else:
            choices.append(p)
      apply(Select.__init__, (self,) + tuple(choices), kw)

class XScript(Script):
   """
      Generates a true JavaScript Script (complete with the *language*
      attribute and beginning and ending comment delimiters).
      
      These should be constructed with a single string containing the 
      java script.
   """
   
   def __init__(self, script):
      Script.__init__(self, '\n<!--\n' + script + '\n//-->\n', 
                      language = 'JavaScript'
                      )

class XTable(Table):
   """
      Just like a *Table* except that all constructor parameters that are
      lists or tuples are automatically converted to rows, and all items in
      those lists that are not *TD*'s are converted to *TD*'s.
   """
   
   def __init__(self, *parms, **kw):
      rows = [self]
      for item in parms:
         if type(item) in (ListType, TupleType):
            item = self.__convertRow(item)
         rows.append(item)
      apply(Table.__init__, tuple(rows), kw)
   
   def __convertRow(self, row):
      tr = TR()
      for item in row:
         if not isinstance(item, TD):
            item = TD(item)
         tr.append(item)
      return tr            

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
      self.body = apply(Body, parms, kw)
      
      HTML.__init__(self, self.head, self.body)
      
      if kw.has_key('title'):
         title = kw['title']
         del kw['title']
      else:
         title = ''
      
      if title:
         self.head.append(Title(title))

   def writeOn(self, out):
      """
         Overrides @Tag.writeOn() so as to prefix the output with the
         special DOCTYPE tag.
      """
      out.write(doctype)
      HTML.writeOn(self, out)

   def __str__(self):
      """
         Overrides @Tag.__str__() so as to prefix the return value with the
         special DOCTYPE tag.
      """
      return doctype + HTML.__str__(self)

_specialRx = re.compile('[<>&"]')
def _fixSpecial(match):
   val = match.group()
   return {
      '<': '&lt;',
      '>': '&gt;',
      '&': '&amp;',
      '"': '&quot;',
      }[val]     
                                                                  
def encode(data):
   """
      Encodes the string: replacing characters that have special meaning
      within HTML.  Returns the encoded string.
      
      parms:
         data::
            [string] data to encode
   """
   return _specialRx.sub(_fixSpecial, data)
   
