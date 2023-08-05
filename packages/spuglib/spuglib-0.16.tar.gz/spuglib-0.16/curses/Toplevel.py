#==============================================================================
#
#  $Id: Toplevel.py 1071 2006-12-11 21:37:59Z mike $
#
"""
   Module for the @Toplevel class.
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
#  $Log: Toplevel.py,v $
#  Revision 1.5  2000/04/30 19:39:52  mike
#  Added getFocus() method, which returns the focused child.
#
#  Revision 1.4  2000/04/02 18:45:34  mike
#  Added setFocus() and getChildren() methods.  Allowed the use of the
#  backspace as well as Shift-Tab to move focus backwards.
#
#  Revision 1.3  2000/03/28 01:37:38  mike
#  Passed coordinates to base class.
#
#  Revision 1.2  2000/03/24 02:20:44  mike
#  Header comment and minor fixes.
#
#
#==============================================================================

from KeyEvent import KeyEvent
from Window import Window

class Toplevel(Window):
   """
      Implements a toplevel window.
   """
   
   def __init__(self, cursesWin, x0, y0, width, height):
      Window.__init__(self, cursesWin, x0, y0, width, height)
      self.__focus = None
      self.__children = []

      # extra event handlers
      self.__handlers = []
         

   def focusToNext(self):
      """
         Shifts focus to the next window on the list.
      """
      if self.__focus:
         self.__focus.releaseFocus()
         
         startIndex = i = self.__children.index(self.__focus) + 1
         
         # search for a child control that can accept the focus
         while 1:
            if i == len(self.__children):
               i = 0
            self.__focus = self.__children[i]
            
            # make sure that the control can accept the focus, if not
            # we'll want to try this again.
            if self.__focus.canTakeFocus():
               self.__focus.takeFocus()
               break
            else:
               i = i + 1
               
               # if we've come full circle, give him the focus and
               # be done with it
               if i == startIndex:
                  break

   def focusToPrev(self):
      """
         Shifts focus to the previous window on the list.
      """
      if self.__focus:
         self.__focus.releaseFocus()
         startIndex = i = self.__children.index(self.__focus) - 1
         
         # again, search for the first previous child control that can
         # accept the focus
         while 1:
            self.__focus = self.__children[i]
            
            # make sure that he can accept
            if self.__focus.canTakeFocus():
               self.__focus.takeFocus()
               break
            else:
               i = i - 1
               
               # protect us from an endless loop if nobody can take focus.
               if i == startIndex:
                  break
               
               # don't want to get too far into the negative
               if i < 0:
                  i = len(self.__children) - i
               

   def setFocus(self, child):
      """
         Sets the focus to the given child.  Raises a *ValueError* if
         /child/ is not one of the children.
      """
      if child not in self.__children:
         raise ValueError('Attempt to set focus to a non-child')
         
      if self.__focus:
         self.__focus.releaseFocus()
      self.__focus = child
      child.takeFocus()

   def getFocus(self):
      """
         Returns the child that has the focus, *None* if there is no 
         focus child.
      """
      return self.__focus

   def addChild(self, newChild):
      """
         Adds a new child window, giving it the focus.  User should not
         need to call this, because most windows should call it automatically
         upon construction.
      """
      # remove the focus from the current child
      if self.__focus:
         self.__focus.releaseFocus()
      
      self.__children.append(newChild)
      self.__focus = newChild      

   def getChildren(self):
      """
         Returns the internal list of children.  Callers should not modify
         this.
      """
      return self.__children

   def getEvent(self):
      """
         Returns the next event received from the window.
      """
      if self.__focus:
         ch = self.__focus.getch()
      else:
         ch = self.getch()
         
      # create the event
      return self.makeEvent(ch)
      
   def addEventHandler(self, handler):
      self.__handlers.append(handler)

   def processEvent(self, evt):
      if self.__focus:
         processed = self.__focus.processEvent(evt)
      else:
         processed = 0
      
      if not processed:
	 # try to let the handlers process it
	 for handler in self.__handlers:
	    if handler.processEvent(evt):
	       return 1

         if isinstance(evt, KeyEvent):
            if evt.code == 9:
               self.focusToNext()
               return 1
            elif evt.code in (self.KEY_STAB, self.KEY_BACKSPACE):
               self.focusToPrev()
               return 1
               
      return processed

               
   

      
   
