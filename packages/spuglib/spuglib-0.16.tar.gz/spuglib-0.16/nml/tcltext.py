#==============================================================================
#
#  $Id: tcltext.py 895 2005-11-29 00:14:34Z mike $
#
"""
   Contains the TCLTextFormatter: an NML formatter that formats a TextBlock
   onto a Tkinter Text control.
"""
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
#  $Log: tcltext.py,v $
#  Revision 1.5  2000/02/18 01:30:00  mike
#  Fixed broken references.
#
#  Revision 1.4  2000/02/13 22:08:52  mike
#  Doc fixes.
#
#  Revision 1.3  1998/11/03 01:38:31  mike
#  Added image support.
#  
#  Revision 1.2  1998/06/14 00:41:32  mike
#  first usable version.
#
#  Revision 1.1  1998/06/11 01:35:40  mike
#  Initial revision
#
#
#==============================================================================


from StdFormatter import *
from types import *
from Tkinter import *

# XXX debug
import sys

# place where we store images that are placed in a text control so that they
# don't go out of scope.
_images = {}

class TCLTextFormatter(StdFormatter):
   "Class for formatting a TextBlock onto a TCL text control."
   
   bold = 1
   underline = 2
   italic = 4
   tele = 8

   stdFont = '-*-helvetica-medium-r-*-*-*-120-*'
   boldFont = '-*-helvetica-bold-r-*-*-*-120-*'
   italicFont = '-*-helvetica-medium-o-*-*-*-120-*'
   teleFont = '-*-courier-medium-r-*-*-*-120-*'

   def __init__(self, textctl):
      StdFormatter.__init__(self)
      self.textctl = textctl
      self.states = {}
      self.stateStack = [0]
      self.lines = 0
      self.indent = 0
      self.tabSize = 2

   def _addState(self, attr, range):
      """
         Adds a pair of text positions to the state.  Range is a tuple
         containing two `row/column` tuples for the beginning and end of a
         range.
      """
      try:
         self.states[attr].append(range)
      except KeyError:
         self.states[attr] = [range]

   def _pushState(self, attr):
      """
         Pushes the current state and creates a new current state consisting of
         the current state merged with /attr/.
      """
      self.stateStack.insert(0, self.stateStack[0] | attr)
   
   def _popState(self):
      "Restores the previous state."
      del self.stateStack[0]

   def _pos(self):
      "Returns the current text position as a `row/column` tuple."
      return self.lines + 1, len(self.buf)

   def _makeLine(self, line):
      """
         Overrides @spug.nml.StdFormatter.StdFormatter._commit() to implement 
         indentation.
      """
      return (self.indent * self.tabSize) * ' ' + line

   def _commit(self, data):
      """
         Provides the necessary override of
	 @spug.nml.StdFormatter.StdFormatter._commit().  Counts the number
	 of newlines (to maintain the current line number)
      """
      newlinePos = string.find(data, '\n')
      if 0 <= newlinePos < len(data) - 1:
         lines = string.split(data, '\n')
         self.lines = self.lines + len(lines)
         for line in lines:
            self.textctl.insert('end', line)
            self.textctl.insert('end', '\n')
      elif newlinePos >= 0:
         self.textctl.insert('end', data)
         self.lines = self.lines + 1
      else:
         pass
#        raise Exception('data committed without newline: "' + data + '"')

   def formatDoc(self, text):
      "Formats an entire document."
      for x in text.words:
         self.format(x)

   def formatUL(self, text):
      "Formats an unordered list."
      
      if not self._curIsEmpty():
         self._write('\n')

      for x in text.words:
         self._write('\n-' + (self.indent * self.tabSize - 1) * ' ')
         self.indent = self.indent + 1
         self.format(x)
         self.indent = self.indent - 1
   
   def formatDL(self, text):
      "Formats a definition list."
      self.indent = self.indent + 1
      for x in text.words:
         if x is not text.words[-1]:
            self._write('\n')
         self.format(x)
      self.indent = self.indent - 1
      self._write('\n')
   
   def formatDI(self, text):
      "Formats a definition item."
      self.format(text.words[0])
      self.indent = self.indent + 1
      self._write(':\n')
      self.format(text.words[1])
      self.indent = self.indent - 1    

   def formatText(self, text):
      "Formats plain old text."
   
      # we'll use this to indicate that the last element was a word,
      # which must be followed by whitespace if the next element is another
      # word in the block
      needSpace = 0
      
      # write leading space if we need it
      if not text.tightLeft:
         self._writeSpace()
      
      # write all of the words and subblocks
      for cur in text.words:
         if needSpace:
            self._writeSpace()
         if type(cur) is StringType:
            needSpace = 1
            self._write(cur)
         else:
            needSpace = 0
            self.format(cur)
      
      # write trailing space if we need it
      if not text.tightRight:
         self._writeSpace()

   def formatTextAttr(self, text, attr):
      "Formats text with a special attribute /attr/."
      start = self._pos()
      self._pushState(attr)
      self.formatText(text)
      self._addState(self.stateStack[0], (start, self._pos()))
      self._popState()

   def format(self, text):
      "Formats the given text block into the text control."
      if text.type == 'doc':
         self.formatDoc(text)
      elif text.type == 'para':
         self.formatText(text)
         if not self._curIsEmpty():
            self._write('\n\n')
         else:
            self._write('\n')
      elif text.type == 'unorderedList':
         self.formatUL(text)
      elif text.type == 'definitionList':
         self.formatDL(text)
      elif text.type == 'definitionItem':
         self.formatDI(text)
      elif text.type == 'bold':
         self.formatTextAttr(text, self.bold)
      elif text.type == 'italic':
         self.formatTextAttr(text, self.italic)
      elif text.type == 'underline':
         self.formatTextAttr(text, self.underline)
      elif text.type == 'text' or text.type == 'literal':
         self.formatText(text)
      elif text.type == 'prelit' or text.type == 'pre' or text.type == 'tele':
         self.formatTextAttr(text, self.tele)
      elif text.type == 'ref':
         # XXX bogus.  need real references.
         self.formatTextAttr(text, self.underline)
      elif text.type == 'img':
         name = text.words[0]
         if _images.has_key(name):
            image = _images[name]
         else:
            image = PhotoImage(file = name)
            _images[name] = image
         container = Canvas(self.textctl, width = image.width(), 
                            height = image.height()
                            )
         self.textctl.window_create('end', window = container)
         container.create_image(0, 0, image = image, anchor = N + W)
      elif text.type == 'n':
         self._write('\n')
      elif len(text.type) == 1 and text.type in string.digits:
         self._write('\n\n')
         self.formatTextAttr(text, self.underline | self.bold)
      else:
         print "Unsupported type: " + text.type

   def configTag(self, state):
      stateName = repr(state)
      if state == self.bold:
         self.textctl.tag_config(stateName, font = self.boldFont)
      elif state == self.italic:
         self.textctl.tag_config(stateName, font = self.italicFont)
      elif state == self.underline:
         self.textctl.tag_config(stateName, underline = 1)
      elif state == self.tele:
         self.textctl.tag_config(stateName, font = self.teleFont)
      elif state == self.bold | self.underline:
         self.textctl.tag_config(stateName, font = self.boldFont,
                                 underline = 1)       
      else:
         print "Unknown state: " + repr(stateName)

   def formatAll(self, text):
      self.textctl.config(font = self.stdFont)
      self.close()
      self.format(text)
      for state, ranges in self.states.items():
         for r in ranges:
            self.textctl.tag_add(repr(state), 
                                 str(r[0][0]) + '.' + str(r[0][1]), 
                                 str(r[1][0]) + '.' + str(r[1][1]), 
                                 )
         self.configTag(state)
      
      
if __name__ == '__main__':
   from parse import DocParser
   from Tkinter import Text
   src = open(sys.argv[1])
   parser = DocParser(src)
   text = Text()
   text.pack()
   TCLTextFormatter(text).formatAll(parser.parseDoc())
   text.mainloop()
