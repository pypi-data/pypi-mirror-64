#==============================================================================
#
#  $Id: SimpleTextViewer.py 618 2000-04-02 18:44:15Z mike $
#
"""
   Module for SimpleTextViewer class.
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
#  $Log: SimpleTextViewer.py,v $
#  Revision 1.3  2000/04/02 18:44:15  mike
#  Added setText().  Fixed cursor disabling.
#
#  Revision 1.2  2000/03/30 01:52:07  mike
#  Replaced addstr() calls with safer write() and writeAt(); added leaveok()
#  in the appropriate places to only enable cursors in entryfields.
#
#  Revision 1.1  2000/03/28 01:37:01  mike
#  Simple scrolling text viewer control.
#
#
#==============================================================================

import string, re
from KeyEvent import KeyEvent
from Control import Control

class SimpleTextViewer(Control):
   """
      As the name implies, this is a class that is used to view a large
      string.
   """

   # regex to match control characters
   __ctrlRx = re.compile('[' + string.join(map(lambda x: '\\%03o' % x, 
                                               range(0, 32) + range(128, 256)
                                               ),
                                           ''
                                           ) + 
                          ']'
                         )

   def paint(self):
      offset = 0
      for line in self.__lines[self.__top:self.__top + self.__rows]:
         if len(line) > self.__cols:
            self.writeAt(0, offset, line[:self.__cols - 1])
            self.write('\\', self.A_REVERSE)
         else:
            self.writeAt(0, offset, line)
            self.clrtoeol()
         offset = offset + 1
      self.clrtobot()
      self.leaveok(1)
      self.refresh()

   def __fixLines(self):
      """
         "fixes" the lines list by truncating any lines wider than
         the viewer and wrapping them around to the next line.
      """
      i = 0
      while i < len(self.__lines):
         line = self.__lines[i]
         while len(line) > self.__cols:
            # replace the line with a special "continuation line", which
            # is actually 1 character longer than the number of columns
            # so that we can distinguish it from a line which merely occupies
            # the entire space
            self.__lines[i] = line[:self.__cols - 1] + ' +'
            
            # insert the remainder of the line into the next slot: we'll 
            # consider his truncation next time through this loop
            i = i + 1
            line = line[self.__cols - 1:]
            self.__lines.insert(i, line)
         
         i = i  + 1

   def __ctrlRxSub(self, m):
      """
         Substitutes a matching control character with the appropriate
         string ('^X' except for tabs).
      """
      ch = ord(m.group())
      if ch == 9:
         # return enough space to take us to the next tabstop
         return ' ' * (8 - m.start() % 8)
      elif ch > 127:
         return '\\%03o' % ch
      else:
         return '^%c' % chr(ch + 64)

   def __fixCtrls(self, line):
      """
         Returns a new line with all control characters replaced with '^X'
         type sequences.
      """
      self.__ctrlRxSub
      return self.__ctrlRx.sub(self.__ctrlRxSub, 
                               line
                               )

   def setText(self, text):
      """
         Sets the text in the viewer to /text/ (a string).
      """
      self.__lines = map(self.__fixCtrls, string.split(text, '\n'))
               
   def __init__(self, parent, x0, y0, width, height, text):
      Control.__init__(self, parent, x0, y0, width, height)
      self.setText(text)
      self.__top = 0
      self.__rows = height
      self.__cols = width
      self.__fixLines()
      self.paint()

   def lineUp(self):
      "Move the view up a single line."
      
      # make sure we aren't already at the top
      if self.__top == 0:
         self.error()
         return
      
      self.__top = self.__top - 1
      self.paint()
   
   def lineDown(self):
      "Move the view down a single line."
      
      # make sure that this is meaningful
      if self.__top + self.__rows >= len(self.__lines):
         self.error()
         return
      
      self.__top = self.__top + 1
      self.paint()

   def pageDown(self):
      "Move the view to the next page."
      
      # make sure that we are not already at the end
      if self.__top + self.__rows >= len(self.__lines):
         self.error()
         return
      
      self.__top = self.__top + self.__rows
      self.paint()

   def pageUp(self):
      "Move the view to the previous page."
      
      # make sure that we can do this
      if self.__top == 0:
         self.error()
         return
      
      # try to go back a full page if we can, if not, go back to 0
      if self.__top < self.__rows:
         self.__top = 0
      else:
         self.__top = self.__top - self.__rows
      
      self.paint()

   def processEvent(self, evt):
      if isinstance(evt, KeyEvent):
         if evt.code == self.KEY_UP:
            self.lineUp()
         elif evt.code == self.KEY_DOWN:
            self.lineDown() 
         elif evt.code == self.KEY_PPAGE:
            self.pageUp()
         elif evt.code == self.KEY_NPAGE:
            self.pageDown()
         else:
            return 0
         
         return 1
      else:
         return 0   

