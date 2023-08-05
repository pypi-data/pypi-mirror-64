#==============================================================================
#
#  $Id: ModalWindow.py 617 2000-04-02 18:43:43Z mike $
#
"""
   Module for the ModalWindow class.
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
#  $Log: ModalWindow.py,v $
#  Revision 1.2  2000/04/02 18:43:43  mike
#  Added show() method to allow a launcher to automatically redraw after
#  processing a modal window.
#
#  Revision 1.1  2000/03/28 01:36:38  mike
#  Modal top-level window base class.
#
#
#==============================================================================

from Toplevel import Toplevel
from MainLoop import MainLoop

class ModalWindow(Toplevel, MainLoop):

   def __init__(self, x0, y0, width, height):
      Toplevel.__init__(self, self.newwin(height, width, y0, x0), x0, y0,
                        width,
                        height
                        )
      MainLoop.__init__(self)
   
   def show(self, parent):
      """
         Shows the modal window.  Redraws the parent when done.
      """
      self.mainloop()
      parent.touchwin()
      parent.refresh()
