#==============================================================================
#
#  $Id: App.py 1070 2006-12-11 21:36:09Z mike $
#
"""
   Module for App class.
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
#  $Log: App.py,v $
#  Revision 1.5  2000/05/19 00:02:29  mike
#  Added code to do a better job of switching from curses mode to full screen
#  apps.
#
#  Revision 1.4  2000/03/28 01:34:22  mike
#  Moved main loop functionality into MainLoop.
#
#  Revision 1.3  2000/03/24 02:17:11  mike
#  Moved keypad(1) all the way up to Window.
#
#  Revision 1.2  2000/03/24 02:12:19  mike
#  Added module docs.
#
#  Revision 1.1.1.1  2000/03/17 00:46:04  mike
#  Curses wrapper classes.
#
#
#==============================================================================

from MouseEvent import MouseEvent, makeMouseEvent
from KeyEvent import KeyEvent
from Toplevel import Toplevel
from MainLoop import MainLoop

import sys
from terminfo import getTermInfo

_app = None

class App(Toplevel, MainLoop):
   """
      This is the cornerstone class for a spug.curses application: it 
      wraps the *stdscr* window and manages the main message loop.
      
      Users may derive an application window of their own from this one,
      but only one instance may be created.  This instance is available
      globally through the @current() function.
   """
   
   def __init__(self):
   
      # there can be only one
      global _app
      if _app:
         raise Exception('Attempt to recreate App singleton')
      else:
         _app = self
   
      stdscr = self.initscr()
      height, width = stdscr.getmaxyx()
      Toplevel.__init__(self, stdscr, 0, 0, width, height)
      MainLoop.__init__(self)
      
      # don't want to see keypresses as they are entered
      self.noecho()
      
      # handle mouse events
      self.mousemask(0xFFFFFFFF)
      
      # if we need term info, we'll store it here
      self.__terminfo = None

      # turn on colors
      self.startColor()

      # turn off the cursor
      self.cursSet(0)

   def __del__(self):
      if _app is self or _app is None:
         self.endwin()
      else:
         print 'whoa!  _app is not self!'

   def beforeNestedApp(self):
      """

         This method and @afterNestedApp() attempt to perform all of the
	 voodoo necessary to run a nested application which takes control
	 over the terminal. I make no claim that this is the correct way to
	 do it: only that it seems to work on the few terminals that I use.
      
         Call this before running applications that use the terminal.
         
      """

      # try to bring back the mouse
      self.leaveok(1)
      self.move(0, 0)
      self.refresh()
      
      # get the terminal info
      if not self.__terminfo:
         self.__terminfo = getTermInfo()

      # try to "pop" the screen
      if self.__terminfo.has_key('exit_ca_mode'):
         sys.stdout.write(self.__terminfo['exit_ca_mode'])
      sys.stdout.flush()
      
   def afterNestedApp(self, child):
      """
         This method (hopefully) restores the terminal screen to a sane 
         state after running an application that takes control
         of the terminal.  Call it after running such a program.
         
         You _must first call_ @beforeNestedApp(), as it sets the `__terminfo`
         variable that is used by this function.
         
         parms:
            child::
               [@spug.curses.Window.Window or None] if specified,
               this is a child window that is in the foreground, overlaying
               the application window.
      """

      # reenter the cup
      if self.__terminfo.has_key('enter_ca_mode'):
         sys.stdout.write(self.__terminfo['enter_ca_mode'])

      # try to enable special graphics characters
      if self.__terminfo.has_key('ena_acs'):
         sys.stdout.write(self.__terminfo['ena_acs'])

      sys.stdout.flush()
      
      # restore the input state
      self.raw()
      self.keypad(1)
      
      # restore the mouse state
      self.leaveok(0)
      
      # repaint everything
      self.touchwin()
      self.refresh()
      
      # repaint the child (and restore his mouse state) if there was a child
      if child:
         child.leaveok(0)
         child.touchwin()
         child.refresh()
         
def current():
   """
      Returns the App singleton, creating it if it does not exist.
   """
   global _app
   if not _app:
      _app = App()
   return _app
