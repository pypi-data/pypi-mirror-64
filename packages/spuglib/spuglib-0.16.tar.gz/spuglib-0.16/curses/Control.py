#==============================================================================
#
#  $Id: Control.py 613 2000-03-30 01:52:07Z mike $
#
"""
   Module for the @Control class.
"""
#
#  Copyright (C) 1998 Michael A. Muller
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#  $Log: Control.py,v $
#  Revision 1.4  2000/03/30 01:52:07  mike
#  Replaced addstr() calls with safer write() and writeAt(); added leaveok()
#  in the appropriate places to only enable cursors in entryfields.
#
#  Revision 1.3  2000/03/28 01:35:34  mike
#  Constructor now passes coordinates to base class.
#
#  Revision 1.2  2000/03/24 02:18:12  mike
#  Controls now automatically add themselves to their parents.
#
#  Revision 1.1.1.1  2000/03/17 00:46:04  mike
#  Curses wrapper classes.
#
#
#==============================================================================

from Window import Window

class Control(Window):
   """
      A control is a non-toplevel (see @Toplevel.Toplevel) window that
      performs some particular function.
   """

   def __init__(self, parent, x0, y0, width, height):
      absY, absX = parent.getbegyx()
      Window.__init__(self, 
                      parent.subwin(height, width, absY + y0, 
                                    absX + x0
                                    ),
                      x0,
                      y0,
                      width,
                      height
                      )
      parent.addChild(self)
   
   def getMinimumSize(self):
      """
         Returns a width, height tuple describing the minimum size required
         for the control.  Must be implemented by subclass.
      """
      raise NotImplementedError()
   
         
