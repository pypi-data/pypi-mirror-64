#==============================================================================
#
#  $Id: Label.py 1029 2006-03-26 16:50:14Z mike $
#
"""
   Module for the @Label class.
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
#  $Log: Label.py,v $
#  Revision 1.3  2000/03/30 01:52:07  mike
#  Replaced addstr() calls with safer write() and writeAt(); added leaveok()
#  in the appropriate places to only enable cursors in entryfields.
#
#  Revision 1.2  2000/03/24 02:12:19  mike
#  Added module docs.
#
#
#==============================================================================

from Control import Control

class Label(Control):
   """
      A label is a static text area with an unchangeable value.
   """

   def paint(self):
      self.move(0, 0)
      self.write(self.__text)
      self.leaveok(0)
      self.refresh()

   def __init__(self, parent, x0, y0, text):
      Control.__init__(self, parent, x0, y0, len(text), 1)
      self.__text = text
      self.paint()

   def getMinimumSize(self):
      return len(self.__text), 1

   def canTakeFocus(self):
      return 0
   
   def releaseFocus(self):
      pass

   def setText(self, text):
      self.__text = text
      self.paint()

   def getText(self):
      return self.__text
