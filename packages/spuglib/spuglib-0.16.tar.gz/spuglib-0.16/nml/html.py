#==============================================================================
#
#  $Id: html.py 1298 2008-04-21 18:34:36Z mike $
#
#  Formatter to write an NML TextBlock to html.
#
#  Copyright (C) 1998 Michael A. Muller
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#  $Log: html.py,v $
#  Revision 1.13  2005/03/06 23:35:41  mike
#  Fixed html encoding func.
#
#  Revision 1.12  2005/03/06 17:30:22  mike
#  Added support for extracting and displaying a title (obtained from the first
#  header in the document)
#
#  Revision 1.11  2003/10/08 00:04:17  mike
#  Added table borders by default.
#
#  Revision 1.10  2002/04/28 19:09:29  mike
#  Added support for tables.
#
#  Revision 1.9  2000/02/18 01:34:05  mike
#  Fixed broken references.
#
#  Revision 1.8  1999/05/10 22:17:02  mike
#  Fixed 'code' keyword - should have been 'tele'
#
#  Revision 1.7  1999/02/03 01:49:57  mike
#  Fixed tabs and docstrings, added support for references and comments.
#
#  Revision 1.6  1998/12/03 13:08:40  mike
#  Cosmetic fix: added paragraph marker after definition item so that
#  graphical browsers format definition lists nicely.
#
#  Revision 1.5  1998/12/02 20:43:54  mike
#  Put a couple of extra newlines into some select places.
#
#  Revision 1.4  1998/11/11 00:13:54  mike
#  Fixed bug which caused special symbols after the beginning of a word to
#  go un-fixed.
#
#  Revision 1.3  1998/08/14 15:25:13  mike
#  System now correctly converts HTML special characters during output.
#
#  Revision 1.2  1998/06/14 00:42:38  mike
#  Added support for type 'n' - line break (newline).
#
#  Revision 1.1  1998/06/11 01:34:05  mike
#  Initial revision
#
#
#==============================================================================

import re, string
from types import *
from StdFormatter import StdFormatter
from block import getHeader, TextBlock

# regular expressions for substitution of HTML characters that need to
# be escaped
_specialrx = re.compile(r'[<>&]')
_ltrx = re.compile(r'<')
_gtrx = re.compile(r'>')
_amprx = re.compile(r'&')

def encode(text):
   """
      Utility method to encode text as HTML (escaping the appropriate
      characters).  Returns the HTML encoded representation of /text/.

      parms:
	 text::
	    [string]
   """
   if _specialrx.search(text):
      text = _amprx.sub('&amp;', text)
      text = _ltrx.sub('&lt;', text)
      text = _gtrx.sub('&gt;', text)
   return text

def headerToAnchor(words):
   """Convert a header to a form suitable for use as an anchor.
   
   parms:
      words:
         [list<block or str>]
   """
   return string.lower(string.join(map(str, words), '_'))
 
class HTMLFormatter(StdFormatter):
   """
      An HTML Formatter formats TextBlock objects into HTML.
   """
   
   # states of the last word written (used to determine how much whitespace
   # to put before the next word.
   newline = 0
   punct = 1
   word = 2
   period = 3
   
   # regular expressions for determining if the current word matches
   # one of the above states
   punctrx = re.compile(r'.*[^\w\.]$')
   wordrx = re.compile(r'\w+')
   periodrx = re.compile(r'.*\.')
   
   # used to define the maximum line width for the output.
   maxLineWidth = 79
   
   def __init__(self, out):
      """
         Constructs an HTML formatted from an output stream.
      """
      StdFormatter.__init__(self)
      self.out = out
      self.last = HTMLFormatter.newline

   def _getTags(self, type):
      """
         Returns a tuple of the leading and trailing tags for the given type.
      """
      if type == 'para':
         return '\n<P>', ''
      elif type == 'underline':
         return '<U>', '</U>'
      elif type == 'italic':
         return '<I>', '</I>'
      elif type == 'bold':
         return '<B>', '</B>'
      elif type == 'tele':
         return '<TT>', '</TT>'
      elif type == 'definitionList':
         return '\n<DL>', '\n</DL>\n'
      elif type == 'definitionItem':
         return '<DT>', ''
      elif type == 'prelit' or type == 'pre':
         return '\n<PRE>\n', '</PRE>'
      elif type == 'table':
         return '\n<TABLE border="1">', '</TABLE>\n'
      elif type == 'row':
         return '\n<TR>', '</TR>'
      elif type == 'col':
         return '<TD>', '</TD>'
      else:
         return '', ''

   def _fix(self, val):
      """
         Converts '>', '<' and '&' to HTML escape sequences.
      """
      return encode(val)

   def _fixRef(self, ref):
      """
	 Fixes a reference.  Used to transform the first element of a "ref"
	 block or "img" block.  Default is to convert it to a string, derived
	 classes may override to provide more sophisticated referencing
	 behavior.

	 parms:
	    ref::
	       [string or @TextBlock]
      """
      return str(ref)

   def format(self, block):
      """
         Formats the block as its HTML equivalent.
      """

      if not block.tightLeft:
         self._writeSpace()

      if block.type == 'definitionItem':
         self._write("<DT>")
         self.format(block.words[0])
         self._write('\n<DD>')
         self.format(block.words[1])
         self._write('<P>\n')
      elif block.type == 'unorderedList':
         self._write('\n<UL>\n')
         for x in block.words:
            self._write('\n<LI>')
            self.format(x)
         self._write('\n</UL>\n')
      elif block.type == 'ref':
         self._write('<A HREF="' + self._fixRef(block.words[0]) + '">')
         self._writeWords(block.words[1:])
         self._write('</A>')
      elif block.type == 'img':
         self._write('<IMG SRC="' + self._fixRef(block.words[0]) + '">')
      elif block.type == 'n':
         self._write('<BR>\n')
      elif len(block.type) == 1 and block.type in string.digits:
         self._write('\n<A NAME="')
         self._write(headerToAnchor(block.words))
         self._write('">')
         self._write('\n<H' + block.type + '>')
         self._writeWords(block.words)
         self._write('</H' + block.type + '></A>\n')
      elif block.type == 'X':
         # XXX should be a lot more flexible
         self._write('<A HREF="#')
         self._write(string.lower(string.join(map(str, block.words), '_')))
         self._write('">')
         self._writeWords(block.words)
         self._write('</A>')
      elif block.type == 'C':
         self._write('\n<!--')
         self._writeWords(block.words)
         self._write('-->\n')
      elif block.type in ('doc', 'text'):
	 self._writeWords(block.words)
      else:
         lead, trail = self._getTags(block.type)
         self._write(lead)
         self._writeWords(block.words)
         self._write(trail)
      
      if not block.tightRight:
         self._writeSpace()

   def _writeWords(self, words):
      """
         Writes a list of words and subblocks.
      """
      # the /needSpace/ variable is used to indicate to the next cycle
      # through the following for loop that the previous object needed
      # to be followed by whitespace.
      needSpace = 0
      
      for cur in words:
         if type(cur) is StringType:
         
            # if we need some whitespace, write it.  Otherwise indicate that
            # we need some space next time.
            if needSpace:
               self._writeSpace()
            else:
               needSpace = 1
               
            self._write(self._fix(cur))
         else:
            self.format(cur)
            needSpace = 0
      
   def _commit(self, data):
      """
         Provides mandatory override of
	 @spug.nml.StdFormatter.StdFormatter._commit(), writing the /data/
	 to the output file.
      """
      self.out.write(data)

   def __emitHeaders(self, headerList, level):
      # if the list is empty, we do nothing
      if headerList:
         indent = '  ' * level
         baseIndent = ('  ' * (level - 1))
         self._write('\n%s<OL>' % baseIndent)

         for item in headerList:
            if isinstance(item, list):
               self.__emitHeaders(item, level + 1)
            else:
               self._write('\n%s<LI><A HREF="#%s">' %
                               (indent, headerToAnchor(item.words))
                              )
               self._writeWords(item.words)
               self._write('</A>')
         
         self._write('\n%s</OL>' % baseIndent)
               
   def generateIndex(self, words):

      level = 1
      headerRx = re.compile(r'\d+')
      curList = []
      stack = [curList]

      # generate the headers as a recursive list
      for block in words:
         if isinstance(block, TextBlock) and headerRx.match(block.type):
            headerLevel = int(block.type)
            
            # for a greater header level, insert a new list
            while headerLevel > level:
               parent = curList
               curList = []
               stack.append(curList)
               parent.append(curList)
               level += 1
            
            # for a lesser header level, pop to that level
            while headerLevel < level:
               stack.pop()
               level -= 1
               curList = stack[-1]

            curList.append(block)
      
      # now emit them
      self.__emitHeaders(stack[0], 1)

   def formatAll(self, text):
      """
         Formats /text/ (an NML @TextBlock) as a complete HTML document.
      """
      self.out.write('<HTML>')
 
      # see if we there's a title, write it if there is
      header = getHeader(text)
      if header:
	 self.out.write('<HEAD><TITLE>')
	 self.out.write(encode(header))
	 self.out.write('</TITLE></HEAD>\n')
	
      # generate an index
      self.generateIndex(text.words)

      self.out.write('<BODY>')
      self.format(text)
      self.close()
      self.out.write('</BODY></HTML>')
