#==============================================================================
#
#  $Id: WinStream.py 561 2000-02-13 22:35:04Z mike $
#
"""
   A text window that implements the "file" interface.  Useful for systems
   that don't support writing to the terminal from a GUI program.
"""
#
#  Copyright (C) 1998 Michael A. Muller
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
#  $Log: WinStream.py,v $
#  Revision 1.2  2000/02/13 22:35:04  mike
#  Doc fixes
#
#  Revision 1.1  1998/10/23 01:01:37  mike
#  Initial revision
#
#
#==============================================================================

from tk import *

class WinStream(Frame):
   
   def __init__(self, parent = None):
      if not parent:
         parent = Toplevel()
      self.top = parent
      Frame.__init__(self, parent)
      self.text = Text(self)
      self.text.pack()
      self.pack()
   
   def write(self, stuff):
      self.text.insert('end', stuff)
   
