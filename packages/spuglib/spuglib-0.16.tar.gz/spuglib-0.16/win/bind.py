#==============================================================================
#
#  $Id: bind.py 561 2000-02-13 22:35:04Z mike $
#
"""
   Mix-in classes to make event binding easier.
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
#  $Log: bind.py,v $
#  Revision 1.2  2000/02/13 22:35:04  mike
#  Doc fixes
#
#  Revision 1.1  1998/10/23 01:02:17  mike
#  Initial revision
#
#
#==============================================================================


class KeyBinder:
   """
      KeyBinder is a mix-in that facilitates binding keys to windows.  Derived
      classes should use the @bindKey() method to bind a key sequence
      (without enclosing angle brackets) to a callable object which accepts
      no parameters.
   """
   
   def _keyEvent(self, evt):
      "Event handler method.  Called when any key event is "
      if not self.map.has_key(evt.keysym):
         raise Exception("key " + evt.keysym + " not in binder map!")
      self.map[evt.keysym]()
   
   def __init__(self, top = None):
      """
         Constructs a keybinder.  /top/ should be the toplevel window that 
         events should be bound to (it can also be a non-toplevel window for
         local binding).  If /top/ is not specified, attempts to determine the
         toplevel window from /self/.
      """
      
      if top is None:
         top = self.winfo_toplevel()
      
      self.top = top
      self.map = {}
   
   def bindKey(self, keySequence, action):
      """
         Binds the /keySequence/ to the /action/.  It is not necessary to
         enclose the sequence in angle brackets.
      """
      self.map[keySequence] = action
      self.top.bind('<' + keySequence + '>', self._keyEvent)
