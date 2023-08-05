#==============================================================================
#
#  $Id: block.py 891 2005-11-27 23:12:47Z mike $
#
#  Contains the definition of a TextBlock and BlockType.  These structures
#  define NML objects.
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
#  $Log: block.py,v $
#  Revision 1.9  2005/03/06 17:30:22  mike
#  Added support for extracting and displaying a title (obtained from the first
#  header in the document)
#
#  Revision 1.8  2002/04/28 19:09:28  mike
#  Added support for tables.
#
#  Revision 1.7  2000/02/13 22:08:52  mike
#  Doc fixes.
#
#  Revision 1.6  1999/05/23 17:55:34  mike
#  Fixed comments and added a warning message if block formatting constructs
#  are discovered in a text formatting entry.
#
#  Revision 1.5  1999/02/03 01:48:50  mike
#  Fixed tabs and comments, added support for comment and reference types.
#
#  Revision 1.4  1998/11/03 00:43:48  mike
#  Purely cosmetic
#
#  Revision 1.3  1998/08/14 15:26:59  mike
#  Added documentation for "exec" block types.
#
#  Revision 1.2  1998/06/14 00:45:06  mike
#  Just added a comment for the 'n' (linebreak/newline) type.
#
#  Revision 1.1  1998/06/11 01:34:05  mike
#  Initial revision
#
#
#==============================================================================

import re, string
from types import *
from spug.io.LineReader import *

class BlockType:
   """
      Contains information about block types.
   """

   def __init__(self, name, tag, terminator):
      """
         Constructs a block type given the following parameters:
         /name/::
               Name of the type
         /tag/::
               Regular expression used to indicate the start of the block.
         /terminator/::
               Regular expression used to terminate the block.
      """
      self.name = name
      self.tag = tag
      self.terminator = terminator

   def getName(self, pattern):
      return self.name
   
   def getTerminator(self, pattern):
      return self.terminator

class AnyBlockType(BlockType):
   """
      Contains information about the generalized block format: \\name( ... )
      Generalized blocks can use parens, square, curly, or angle brackets
      or single or double quotes as delimiters.
   """
   
   expr = r'\\([\w\.]+)([\[\{\(<"' "'])";
   
   template = re.compile(expr)
   
   def __init__(self, tag):
      BlockType.__init__(self, '', tag, '')
   
   def getName(self, pattern):
      return self.template.match(pattern).group(1)
   
   def getTerminator(self, pattern):
      initiator = self.template.match(pattern).group(2)
      return \
         {
         '[': ']',
         '{': '}',
         '(': ')',
         '<': '>',
         '"': '"',
         "'": "'",
         }[initiator]

class TextBlock:
   """
      Represents a block of text with a particular style.
      
      These are the standard types of text blocks:
      *doc*::
            Document type.  A structural type which can contain other structural
            types.
      *para*::
            Paragragh type.  A structural type which can not contain other
            structural types.
      *unorderedList*::
            Unordered list.  A structural type in which each of the words are 
            of type *doc*.
      *definitionList*::
            Definition list.  A structural type in which each of the words are
            of type *definitionItem*.
      *definitionItem*::
            An item in a definition list.  A structural type that always contains 
            exactly two words: a *text* item and a *doc* item.
      *table*::
            A table object.  Contents should only be *row* objects.
      *row*::
            A table row.  Should only be embedded in a *table*, and contents 
            should ony be *column* objects.
      *col*::
            A table column.  Should only be embedded in a *row* objects.
      *text*::
            A block of text that can contain only non-structural types.
      *underline*::
            Underlined text.
      *bold*::
            Boldfaced text.
      *italic*::
            Italic text.
      *ref*::
            Reference to a text location.  In this case, the first word is a
            reference, the remainder is the anchor text.
      *img*::
            The first word of the text is the name of an image file.  The remainder
            of the text is ignored.
      *exec*::
            Executes its contents as a shell command.  In the event of an error, 
            raises a parsing error.  Output from the command is treated as NML
            source which is parsed in context.
      *n*::
            Force a newline at this point in the enclosing text.  All of the
            words are ignored.
      *X*::
            The enclosed text is a cross reference (XXX this is very weak
            at this time - only can be used to reference other parts of the
            same document).
      *C*::
            The enclosed text is a comment, and should not be visible when
            the document is rendered.
            
      There are a variety of special types of text blocks:
      *literal*::
            backquoted type - everything in it is literal except the backslash.
      *prelit*::
            `preformatted/literal` type.  Everything in it is literal and the
            raw format (extraneous whitespace) of the original should
            be preserved.  This type only has one word.
      *pre*::
            Preformatted.  Raw format of the original should be preserved.
      *date*::
	    The block contents is the document date.
      *title*::
	    The block contents is the document title.
      /namespace.type/::
	    Block types that are specific to a particularly renderer can use
	    a block type of this form to force them to be ignored by other
	    renderers.
   """
   
   def __init__(self, src, typeName, tightLeft = 0):
      """
         Constructs a text block.
         /src/::
               either a tuple (filename, line number) or a LineReader.  Any other
               type is ignored.
         /typeName/::
               Type name of the block.
         /tightLeft/::
               If specified, indicates whether the block binds tightly (without
               whitespace) to the information to the left of it.
      """
   
      if isinstance(src, LineReader):
         self.src = src.name, src.lineNumber()
      elif type(src) == TupleType:
         self.src = src
      else:
         self.src = '<unknown>', -1
         
      self.words = []
      self.type = typeName
      
      self.tightLeft = tightLeft
      self.tightRight = 0
      
      # *literal*, *prelit* and *C* types are both literal.
      self.literal = self.type == 'literal' or self.type == 'prelit' or \
         self.type == 'C'
      
      # *pre*, *prelit* and *C* types are both preformatted.
      self.preformatted = self.type == 'pre' or self.type == 'prelit' or \
         self.type == 'C'

      # exec types are very special
      self.isExec = self.type == 'exec'

      self.blanklineTerminated = self.type == 'para'
   
   def addWords(self, words):
      """
         adds the given sequence of /words/ to the receiver.
      """
      self.words = self.words + words

   def addChild(self, child):
      """
         Adds a child text block to the receiver.
      """
      self.words.append(child)

   def consume(self, str):
      """
         Consumes a string in a manner appropriate to the text block.
      """
      if self.preformatted:

         # was there a last word?
         if self.words:
            lastWord = self.words[-1]
         else:
            lastWord = None         

         # if the last word was also a string, just append this word
         # to the last word         
         if lastWord and type(lastWord) == StringType:
            self.words[-1] = lastWord + str
         
         else:
            # otherwise, just append
            self.words.append(str)
      else:
         self.addWords(string.split(str))
         
   def find(self, blockType):
      """
	 Finds the first block with type /blockType/ in all of the child
	 blocks.  Returns *None* if the block type is not found.

	 parms:
	    blockType::
	       [string]
      """
      for child in self.words:
	 if isinstance(child, TextBlock):
	    if child.type == blockType:
	       return child
	    else:
	       result = child.find(blockType)
	       if result is not None:
		  return result
      else:
	 return None

   def debug(self, soFar = ''):
      """
         Prints /self/ in a form useful to der programmer.  Returns the last
         line as a string.
      """
      if len(soFar) > 76:
         print soFar
         soFar = ''
      soFar = soFar + ' \\' + self.type + '('
      
      for x in self.words:
         if type(x) is StringType:
            if len(soFar) + len(x) + 1 > 79:
               print soFar
               soFar = ''
            soFar = soFar + ' ' + x
         else:
            soFar = x.debug(soFar)

      if len(soFar) > 78:
         print soFar
         soFar = ''
      
      soFar = soFar + ')'

      return soFar

   def __str__(self):
      """
         Returns the block in a minimal string format - basically this is raw
         content with spaces between words.
      """
      return string.join(map(str, self.words))

def getHeader(block):
   """
      A utility function which finds the first header in the text and returns
      it as a string.  This is useful for extracting the title from a
      document.

      Returns *None* if no header was found.

      parms:
	 block::
	    [@TextBlock]
   """
   for child in block.words:
      if isinstance(child, TextBlock):
	 if child.type.isdigit():
	    return str(child)
	 else:
	    header = getHeader(child)
	    if header is not None:
	       return header
   else:
      return None
