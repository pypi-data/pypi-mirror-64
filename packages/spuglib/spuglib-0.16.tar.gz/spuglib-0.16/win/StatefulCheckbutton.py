#==============================================================================
#
#  $Id: StatefulCheckbutton.py 503 1999-06-04 20:20:44Z mike $
#
"""
   Contains the StatefulCheckbutton class.
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
#  $Log: StatefulCheckbutton.py,v $
#  Revision 1.1  1999/06/04 20:20:44  mike
#  A checkbutton that tracks its own state.
#
#
#==============================================================================

from tk import Checkbutton

class StatefulCheckbutton(Checkbutton):
   
   """
      A checkbutton that tracks its own state: use @selected() method
      to check its state.
   """
   
   def _command(self):
      """
         Called when the button is toggled.
      """
      self.toggle()
   
   def __init__(self, parent, **kw):
      
      kw['command'] = self._command
      apply(Checkbutton.__init__, (self, parent), kw)
      self.__selected = 0
   
   def select(self):
      """
         Turns the checkbutton "on".
      """
      self.__selected = 1
      Checkbutton.select(self)
   
   def deselect(self):
      """
         Turns the checkbutton "off".
      """
      self.__selected = 0
      Checkbutton.deselect(self)
   
   def toggle(self):
      """
         Toggles the state of the checkbutton.
      """
      if self.__selected:
         self.deselect()
      else:
         self.select()

   def selected(self):
      """
         Returns true if the checkbutton is selected, false if not.
      """
      return self.__selected
