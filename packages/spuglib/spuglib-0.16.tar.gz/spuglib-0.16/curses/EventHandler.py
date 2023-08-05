#==============================================================================
#
#  $Id: EventHandler.py 826 2003-08-02 19:20:45Z mike $
#
"""
   EventHandler interface.
"""
#
#  Copyright (C) 2000 Michael A. Muller
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
#==============================================================================


class EventHandler:
   """
      Interface for event handlers.  All derived classes must implement
      the @processEvent() method.
   """
   
   def processEvent(self, event):
      """
         This method is called whenever an event is sent.
         
         Must be implemented by derived classes.
      """
      raise NotImplementedError()
