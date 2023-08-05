
from Curses import Curses, CursesError
from EventHandler import EventHandler

class Window(Curses, EventHandler):

   """
      Protected Variables:
      /_xpos/::
         Window x position relative to parent.
      /_ypos/::
         Window y position relative to parent.
      /_width/::
         Window width.
      /_height/::
         Window height.
   """

   def __init__(self, win, x0, y0, width, height):
      Curses.__init__(self)
      self.__win = win
      
      self._xpos = x0
      self._ypos = y0
      self._width = width
      self._height = height

      # get keys as logical values instead of raw key sequences - for all
      # windows.
      self.keypad(1)

   def canTakeFocus(self):
      """
         Derived classes should override this method and return false if
         they cannot accept the focus (in other words, if they are static).
         
         Base class version returns true.
      """
      return 1

   def takeFocus(self):
      """
         Called when focus is transferred to the window.  Base class
         version does nothing, may be implemented by subclass.
      """
      pass
   
   def releaseFocus(self):
      """
         Called when focus is transferred from the window.  Base class
         version does nothing, may be implemented by subclass.
      """
      pass

   # --- high level interface ---

   def write(self, data, attr = None):
      """
         Use this instead of @addstr(): adds a string without issuing an
         exception if the cursor is out of range afterwards.
      """
      try:
         if attr is None:
            self.addstr(data)
         else:
            self.addstr(data, attr)
      except CursesError, ex:
         pass

   def writeAt(self, x, y, data, attr = None):
      """
         Use this instead of @addstr(): adds a string at a position without 
         issuing an exception if the cursor is out of range afterwards.
      """
      try:
         if attr is None:
            self.addstr(y, x, data)
         else:
            self.addstr(y, x, data, attr)
      except CursesError, ex:
         pass

   def getSize(self):
      """
         Returns external width and height as a tuple.
      """
      return self._width, self._height

   def getPos(self):
      """
         Returns x and y coordinates relative to the parent window as a tuple.
      """
      y,x = self.getbegyx()
      return x, y

   def error(self):
      """
         Notifies the user of a key-entry type error with a beep.
      """
      self.beep()
      self.refresh()

   # --- low level (curses) interface ---

   def addstr(self, *parms):
      """
         Adds a string to the display.  Parm list should be one of:
         
         -  x, y, string, attribute
         -  string, attribute
         -  string
      """
      apply(self.__win.addstr, parms)

   def subwin(self, lines, cols, orgy, orgx):
      return self.__win.subwin(lines, cols, orgy, orgx)

   def refresh(self):
      self.__win.refresh()

   def move(self, row, col):
      self.__win.move(row, col)
   
   def keypad(self, val):
      """
         Turns "keypad" functionality on or off.  "val" should be 1 or 0.
      """
      self.__win.keypad(val)

   def getch(self):
      """
         Gets a character and returns it.
      """
      return self.__win.getch()

   def hline(self, ypos, xpos, chr, numCols):
      """
         Draws a horizontal line of the character /chr/ (an integer)
         starting at (xpos, ypos) and extending /numCols/ columns.
      """
      self.__win.hline(ypos, xpos, chr, numCols)
      
  
   def clrtoeol(self):
      """
         Clear from the current position to the end of the line.
      """
      self.__win.clrtoeol()
   
   def clrtobot(self):
      """
         Clear from the current position to the bottom of the window.
      """
      self.__win.clrtobot()

   def getmaxyx(self):
      """
         Returns a tuple consisting of the height and width of the window.
      """
      return self.__win.getmaxyx()

   def getyx(self):
      """
         Returns a tuple consisting of the (absolute?) y and x positions of the 
         cursor for the window.
      """
      return self.__win.getyx()

   def getbegyx(self):
      """
         Returns a tuple consisting of the absolute y and x positions of the
         window.
      """
      return self.__win.getbegyx()

   def leaveok(self, arg):
      self.__win.leaveok(arg)

   def touchwin(self):
      self.__win.touchwin()

   def box(self, *parms):
      apply(self.__win.box, parms)