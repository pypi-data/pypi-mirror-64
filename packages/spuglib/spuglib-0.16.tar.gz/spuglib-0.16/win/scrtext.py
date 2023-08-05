#==============================================================================
#
#  $Id: scrtext.py 561 2000-02-13 22:35:04Z mike $
#
"""
   Scrolling text control.
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
#  $Log: scrtext.py,v $
#  Revision 1.2  2000/02/13 22:35:04  mike
#  Doc fixes
#
#  Revision 1.1  1998/10/23 01:04:03  mike
#  Initial revision
#
#
#==============================================================================

from tk import *

class ScrollingText(Frame):
   "Implements a text control with two scrollbars."

   def __init__(self, parent, **kw):
      """
         Constructs scrolling text with the same parameters used for a normal
         *Text* control.
      """
      Frame.__init__(self, parent)
      self.text = apply(Text, (self,), kw)
      self.text.grid(sticky = N + S + W + E)
      self.vsb = Scrollbar(self, orient = 'vertical', 
                           command = self.text.yview
                           )
      self.vsb.grid(row = 0, column = 1, sticky = N + S)
      self.hsb = Scrollbar(self, orient = 'horizontal',
                           command = self.text.xview
                           )
      self.hsb.grid(row = 1, column = 0, sticky = W + E)
      self.columnconfigure(0, weight = 1)
      self.rowconfigure(0, weight = 1)
      self.text.config(xscrollcommand = self.hsb.set, 
                       yscrollcommand = self.vsb.set
                       )

   def __getattr__(self, attr):
      "Delegates all attributes to the text control."
      return getattr(self.text, attr)
