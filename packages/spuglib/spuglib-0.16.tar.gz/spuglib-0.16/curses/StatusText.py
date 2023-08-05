#==============================================================================
#
#  $Id: StatusText.py 761 2001-05-04 00:20:41Z mike $
#
"""
   Module for the StatusText class.
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
#  $Log: StatusText.py,v $
#  Revision 1.3  2001/05/04 00:20:41  mike
#  Added required __init__.py file.  Did something with StatusText.
#
#  Revision 1.2  2000/03/30 01:52:07  mike
#  Replaced addstr() calls with safer write() and writeAt(); added leaveok()
#  in the appropriate places to only enable cursors in entryfields.
#
#  Revision 1.1  2000/03/28 01:38:48  mike
#  Status text control: a changeable label.
#
#
#==============================================================================

from Control import Control

class StatusText(Control):
   """
      This is a text control, similar to a label except that the text can
      be changed, making it suitable for displaying status information.
   """
   
   def paint(self):
      self.writeAt(0, 0, self.__text[:self._width])
      self.clrtoeol()
      self.leaveok(1)
      self.refresh()
   
   def __init__(self, parent, x0, y0, width, height, text):
      Control.__init__(self, parent, x0, y0, width, height)
      self.__text = text
      self.paint()
   
   def setText(self, text):
      "Sets the controls text"
      self.__text = text
      self.paint()
   
   def getText(self):
      "Returns the control's text"
      return self.__text
   
   def canTakeFocus(self):
      """
         Overrides @Window.canTakeFocus() to indicate that focus can not be
         given to this window.
      """
      return 0
   