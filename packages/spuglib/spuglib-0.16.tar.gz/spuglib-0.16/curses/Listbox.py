#==============================================================================
#
#  $Id: Listbox.py 852 2005-01-15 21:38:08Z mike $
#
"""
   Module for the Listbox class.
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
#  $Log: Listbox.py,v $
#  Revision 1.7  2005/01/15 21:38:08  mike
#  Fixed check for home/Ctrl-A.
#
#  Revision 1.6  2002/12/02 00:47:56  mike
#  Fixed bugs causing display problems.
#
#  Revision 1.5  2000/07/16 17:45:06  mike
#  Added _selectionChanged() method so that derived classes can intercept all
#  events causing the selection to change.
#
#  Revision 1.4  2000/04/04 01:12:17  mike
#  Added paintSelection()
#
#  Revision 1.3  2000/04/02 18:42:32  mike
#  Added setSelection(), delete(), setItems() and getItems()
#  Fixed cursor disabling and range check.
#
#  Revision 1.2  2000/03/30 01:52:07  mike
#  Replaced addstr() calls with safer write() and writeAt(); added leaveok()
#  in the appropriate places to only enable cursors in entryfields.
#
#  Revision 1.1  2000/03/24 02:10:19  mike
#  Simple listbox control.
#
#
#==============================================================================

import string
from types import IntType
from KeyEvent import KeyEvent
from Control import Control

class Listbox(Control):

   """
      Used to represent a standard listbox.
   """

   def __drawLine(self, offset, item):
      if offset + self.__top == self.__cur:
         if self.__gotFocus:
            attr = self.A_REVERSE
         else:
            attr = self.A_UNDERLINE
      else:
         attr = self.A_NORMAL
      
      # convert to a string and truncate to the width of the box
      strItem = self._itemAsString(item)[:self.__cols]
      
      # now pad to the width of the box
      strItem = string.ljust(strItem, self.__cols)
      
      self.writeAt(0, offset, strItem, attr)
      self.leaveok(1)
      self.refresh()

   def __drawFrom(self, pos):
      """
         Draws from the position /pos/ down to the bottom of the box.
      """
      offset = 0
      for item in self.__items[self.__top:self.__top + self.__rows]:
         self.__drawLine(offset, item)
         offset = offset + 1
      
      # clear the rest of the window
      while offset < self.__rows:
         self.hline(offset, 0, 32, self.__cols)
         offset = offset + 1
      
      self.refresh()

   def _itemAsString(self, item):
      """
         Returns /item/ represented as a string. Since the default form of
         this control deals with a list of strings, the base class version
         of this method just returns the item.  Derived classes should
         override it if they use the control to manage something other than
         strings.
      """
      return item

   def _selectionChanged(self, selectionIndex, item):
      """
         Called when the selection changes.  Derived classes may override
         this to be notified of a selection change.  Base class version does
         nothing.  /selectionIndex/ is the index of the new selection (or
         -1 if nothing is now selected), /item/ is the selected item (*None*
         if nothing is now selected).
      """
      pass

   def paint(self):
      self.__drawFrom(self.__top)
   
   def paintSelection(self):
      """
         Repaints only the selected entry.
      """
      self.__drawLine(self.__cur - self.__top, self.__items[self.__cur])
      
   def selectionDown(self):
      "Moves the selection bar down one line"
      
      # make sure that we haven't gone off the edge
      if self.__cur >= len(self.__items) - 1:
         self.error()
         return
      
      # increment the selection cursor
      self.__cur = self.__cur + 1

      # call the notification method
      selection = self.__items[self.__cur]
      self._selectionChanged(self.__cur, selection)    
      
      # if we've gone over the bottom edge, need to scroll
      if self.__cur - self.__top == self.__rows:
         self.__top = self.__top + 1
         self.paint()
         return
      
      # repaint the old selection
      pos = self.__cur - self.__top - 1
      self.__drawLine(pos, self.__items[self.__cur - 1])
      
      # repaint the new selection
      pos = self.__cur - self.__top
      self.__drawLine(pos, selection)     
      

   def selectionUp(self):
      "moves the selection bar up one line"
      
      # make sure that we aren't already at the top
      if self.__cur == 0:
         self.error()
         return
      
      # decrement the selection cursor
      self.__cur = self.__cur - 1
      
      # call the notification method
      selection = self.__items[self.__cur]
      self._selectionChanged(self.__cur, selection)
      
      # if we've gone over the top, need to scroll
      if self.__cur < self.__top:
         self.__top = self.__top - 1
         self.paint()
         return
      
      # repaint the old selection
      pos = self.__cur - self.__top + 1
      self.__drawLine(pos, self.__items[self.__cur + 1])
      
      # repaint the new selection
      pos = self.__cur - self.__top
      self.__drawLine(pos, selection)

   def pageDown(self):
      "moves the view down to the next page."
      
      itemCount = len(self.__items)
      
      # make sure that there is a next page to move down to
      if self.__top + self.__rows >= itemCount:
         self.error()
         return
      
      # increment the topline to the next page
      self.__top = self.__top + self.__rows
      
      # if the cursor can't move down a full page, move it to the end
      if self.__cur + self.__rows >= itemCount:
         self.__cur = itemCount - 1
      else:
         self.__cur = self.__cur + self.__rows
      
      # do notification
      self._selectionChanged(self.__cur, self.__items[self.__cur])
      
      # finally, redraw
      self.paint()

   def pageUp(self):
      "moves the view up to the previous page"
      
      if self.__top == 0:
         self.error()
         return
      
      # if we are too close to the top, just go to the top.  Otherwise, 
      # go back exactly one page
      if self.__top < self.__rows:
         self.__top = 0
      else:
         self.__top = self.__top - self.__rows
      
      # same idea with the cursor: go back one page if we can afford to
      if self.__cur < self.__rows:
         self.__cur = 0
      else:
         self.__cur = self.__cur - self.__rows
      
      # do notification
      self._selectionChanged(self.__cur, self.__items[self.__cur])
      
      # redraw the page
      self.paint()

   def topOfList(self):
      "returns to the top of the list"
      oldPos = self.__cur
      self.__top = 0
      self.__cur = 0
      if oldPos:
         self._selectionChanged(self.__cur, self.__items[self.__cur])
      self.paint()
   
   def bottomOfList(self):
      """
         Brings the selection cursor to the last item at the bottom of the
         list and displays the last page.
      """
      itemCount = len(self.__items)
      
      # if this is not already the last page, compute the last page.
      if self.__top + self.__rows < itemCount:
         self.__top = itemCount - self.__rows
      
      # cursor to the end
      if self.__cur != itemCount - 1:
         self.__cur = itemCount - 1
         self._selectionChanged(self.__cur, self.__items[self.__cur])
      
      # redraw
      self.paint()
   
   def __processKey(self, key):
      if key == self.KEY_DOWN:
         self.selectionDown()
      elif key == self.KEY_UP:
         self.selectionUp()
      elif key == self.KEY_NPAGE:
         self.pageDown()
      elif key == self.KEY_PPAGE:
         self.pageUp()
      elif key in (self.KEY_HOME, 1):
         self.topOfList()
      elif key in (self.KEY_END, 5):
         self.bottomOfList()
      else:
         return 0
      
      return 1
   
   def processEvent(self, evt):
      if isinstance(evt, KeyEvent):
         return self.__processKey(evt.code)
      else:
         return 0

   def __drawSelection(self):
      if self.__items:
         self.__drawLine(self.__cur - self.__top, self.__items[self.__cur])
      else:
         self.move(0, 0)

   def takeFocus(self):
      self.__gotFocus = 1
      self.__drawSelection()
   
   def releaseFocus(self):
      self.__gotFocus = 0
      self.__drawSelection()
      self.refresh()

   def setSelection(self, selection):
      """
         Sets the cursor to the given selection.  Raises a *ValueError* if
         the index is out of range, or is not in the list of items.
         
         parms:
            selection::
               [int or any] if an int, it is the index of the selection.
               For anything other than an int, it is the selection object.
      """
      oldPos = self.__cur
      if type(selection) is IntType:
         if selection >= len(self.__items) or selection < 0:
            raise ValueError('Selection index out of range')
         self.__cur = selection
      else:
         index = self.__items.index(selection)
         self.__cur = index

      # call notification method
      if oldPos != self.__cur:
         self._selectionChanged(self.__cur, self.__items[self.__cur])      
      
      self.__moveToView()
   
   def __moveToView(self):
      """
         Changes the view of the list so that the cursor is included, 
         repainting if a change was made.
      """
      if self.__cur < self.__top:
         self.__top = self.__cur
      
      # is the selection greater than the last displayed row?
      elif self.__cur >= self.__top + self.__rows:
         # adjust position so that the selection is at the last row
         self.__top = self.__cur - self.__rows + 1
         
         # fix negative number that can occur when there are fewer items than
         # rows
         if self.__top < 0:
            self.__top = 0
      else:
         return
      self.paint()
   
   def __init__(self, parent, x0, y0, width, height, items):
      Control.__init__(self, parent, x0, y0, width, height)
      self.__rows = height
      self.__cols = width
      self.__items = items
      self.__cur = 0
      self.__top = 0
      self.__gotFocus = 1
      self.paint()   

   def selection(self):
      """
         Returns the current selection.  Returns *None* if the listbox is
         empty.
      """
      if self.__items:
         return self.__items[self.__cur]
      else:
         return None


   def selectionIndex(self):
      """
         Returns the index of the current selection.  Returns -1 if the
         listbox is empty.
      """
      if not self.__items:
         return -1
      else:
         return self.__cur

   def __itemAdded(self, index, item):
      # if there were no entries, we need to set the cursor.
      if self.__cur == -1:
         self.__cur = 0
      
      # if the new item is cursored, change the selection
      if self.__cur == index:
         self._selectionChanged(self.__cur, item)
   
   def append(self, item):
      """
         Adds a new item to the end of the list.
      """
      self.__items.append(item)
      
      # if the item is in range, paint it.
      pos = len(self.__items) - 1
      if self.__top <= pos < self.__top + self.__rows:
         self.__drawLine(pos, item)
      self.__itemAdded(pos, item)

   def insert(self, index, item):
      """
         Inserts an item at /index/th position in the list.
      """
      self.__items.insert(index, item)
      
      # adjust the index if it is out of range
      if index >= len(self.__items):
         index = len(self.__items) - 1
      
      # if the item is in range, we need to redraw the rest of the list.
      if self.__top <= index < self.__top + self.__rows:
         self.__drawFrom(index)

      self.__itemAdded(index, item)

   def delete(self, index):
      """
         Deletes the item at the given index.  If the index is out of
         range, raises a *KeyError*.
      """
      # remove the item from the list (let the exception fly, if any)
      del self.__items[index]
      
      # if the item is in range, we need to redraw the rest of the list.
      if self.__top <= index < self.__top + self.__rows:
         self.__drawFrom(index)
      
      # if it was the cursor, and it was the list item on the list, decrement
      # the cursor
      if self.__cur == index and index == len(self.__items):
         self.__cur = self.__cur - 1
      
      # notify the selection method
      if self.__cur == -1:
         self._selectionChanged(-1, None)
      else:
         self._selectionChanged(self.__cur, self.__items[self.__cur])
   
   def setItems(self, items):
      """
         Resets the internal items list.
      """
      self.__items = items
      self.__top = 0
      self.__cur = 0
      self.paint()      
   
   def getItems(self):
      """
         Returns the list of all items in the listbox.  This is the internal
         list, and the caller should not modify it.  Use @setItems(), or the
         @append(), @insert(), and @delete() methods instead.
      """
      return self.__items