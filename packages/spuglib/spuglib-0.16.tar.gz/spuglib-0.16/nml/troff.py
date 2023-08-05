#==============================================================================
#
#  $Id$
#
#  Formatter to write an NML TextBlock to TROFF.
#
#  Copyright (C) 2005 Michael A. Muller
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
#==============================================================================

import re, string
from types import *
from StdFormatter import StdFormatter
from block import getHeader

class TroffFormatter(StdFormatter):
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

   BLOCK_START = 0
   AFTER_BLOCK = 1
   AFTER_PARA = 2
   INLINE = 3
   COMMENT = 4

   # escape all backslashes
   __specialRx = re.compile(r'\\|\n')
   def __specialSub(self, match):
      val = match.group()
      if val == '\n':
	 if self.__state == self.COMMENT:
	    return '\n.\\"'
	 else:
	    return '\n'
      else:
	 return '\\' + match.group()
 
   def __init__(self, out):
      """
         Constructs an HTML formatted from an output stream.
      """
      StdFormatter.__init__(self)
      self.out = out
      self.__state = self.BLOCK_START

      # stack of the inline modifiers
      self.__lastInline = []

      # true if we are currently preserving whitespace
      self.__literal = True

   def __writeTitle(self, block):
      for word in block.words:
	 self._write(str(word).upper())
	 self._writeSpace()

      self._write('\n')

   def __writeInline(self, macro, block):
      """
	 Formats inline phrases: underline, italic...
      """
      if block.tightLeft or block.tightRight or self.__literal:

	 # if there was a prior font modifier, close it off first
	 if self.__lastInline:
	    self._write('\\fP')

	 # need a paren in front of two character font names
	 if len(macro) == 2:
	    macro = '(' + macro

	 self.__lastInline.append(macro)
	 
	 self._write('\\f%s' % macro)
	 self._writeWords(block.words)
	 self._write('\\fP')

	 # pop the modifier, if there was another restore it
	 assert self.__lastInline.pop() == macro
	 if self.__lastInline:
	    self._write('\\f%s' % self.__lastInline[-1])
      else:
	 self._write('\n.%s ' % macro)
	 # XXX doesn't deal with embedded newlines
	 self._writeWords(block.words)
	 self._write('\n')
      self.__state = self.INLINE

   def format(self, block):
      """
         Formats the block as its HTML equivalent.
      """
      if not block.tightLeft:
         self._writeSpace()

      if block.type == '1':
	 self._startLine()
	 self._write('.SH ')
	 self.__writeTitle(block)
	 self.__state = self.BLOCK_START
	 self._startLine()
      elif block.type == '2':
	 self._startLine()
	 self._write('.SS ')
	 self.__writeTitle(block)
	 self.__state = self.BLOCK_START
	 self._startLine()
      elif block.type in string.digits:
	 self._startLine()
	 self._write('.SS ')
	 self._writeWords(block.words)
	 self.__state = self.BLOCK_START
	 self._startLine()
      elif block.type == 'para':
	 if self.__state == self.AFTER_PARA:
	    self._startLine()
	    self._write('.sp 1\n')
	 self._writeWords(block.words)
	 self._write('\n')
	 self.__state = self.AFTER_PARA
      elif block.type == 'italic':
	 self.__writeInline('I', block)
      elif block.type == 'bold':
	 self.__writeInline('B', block)
      elif block.type == 'underline':
	 # troff interprets italics as underline :-/
	 self.__writeInline('I', block)
      elif block.type == 'tele':
	 self.__writeInline('CW', block)
      elif block.type == 'unorderedList':
	 self._startLine()
	 if self.__state == self.INLINE:
	    self._write('.br\n')
	 self._write('.in +4\n')
	 for word in block.words:
	    self._startLine()
	    self._write('.ti -4\n')
	    self._write('\\(bu   ')
	    self.__state = self.BLOCK_START
	    self.format(word)
	    self._startLine()
	    self._write('.br\n')
	 self._write('.in -4\n')
	 self.__state = self.AFTER_BLOCK
      elif block.type == 'prelit':
	 self._write('\n.nf\n')
	 self.__literal = True
	 for word in block.words:
	    self._write(self._fix(word))
	 self.__literal = False
	 self._write('\n.fi\n')
	 self.__state = self.AFTER_BLOCK
      elif block.type == 'pre':
	 self._write('\n.nf\n')
	 self.__literal = True
	 self._writeWords(block.words)
	 self.__literal = False
	 self._write('\n.fi\n')
	 self.__state = self.AFTER_BLOCK
      elif block.type == 'definitionItem':
	 self._startLine()
	 if self.__state == self.INLINE:
	    self._write('.br\n')
	 self.__state = self.AFTER_BLOCK
	 self.format(block.words[0])
	 self._startLine()
	 self._write('.in +4\n')
	 self.__state == self.BLOCK_START
	 self.format(block.words[1])
	 self._startLine()
	 self._write('.in -4\n')
	 self.__state = self.AFTER_BLOCK
      elif block.type == 'X':
	 for word in block.words:
	    self._write(word.upper())
	    self._writeSpace()
      elif block.type == 'C':
	 # start a new line, go into comment mode and write everything
	 self._startLine()
	 state = self.__state
	 self.__state = self.COMMENT
	 self._write('.\\"')
	 self._writeWords(block.words)

	 # start a fresh line and restore the old state
	 self._startLine()
	 self.__state = state
      elif block.type in ('doc', 'definitionList', 'text', 'literal',
			  'text'):
	 self._writeWords(block.words)
      else:
	 # do nothing
	 pass
	 #print 'doing nothing for %s' % block.type

      # add whitespace to the right if so specified
      if not block.tightRight:
         self._writeSpace()

      return

   def _fix(self, text):
      return self.__specialRx.sub(self.__specialSub, text)

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
      # XXX I'm pretty sure I should be putting the "expandtabs()" into
      # _makeLine() instead of here... problem is, that doesn't work - it
      # doesn't look like _makeLine() actually gets called for every single
      # line.  It looks like _commit(), does, though.
      self.out.write(data.expandtabs())

   def formatAll(self, text):
      """
         Formats /text/ (an NML @TextBlock) as a complete HTML document.
      """
      self.format(text)
      self.close()
