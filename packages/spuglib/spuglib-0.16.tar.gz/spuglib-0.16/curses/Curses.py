
# import NCurses if we can, otherwise import plain old curses
#try:
#   from ncurses import curses, _curses
#   _useNCurses = 1
#except ImportError:
#   import curses
#   _useNCurses = 0
import curses
_useNCurses = 0

from KeyEvent import KeyEvent
from MouseEvent import MouseEvent

# preserve this exception in a more palatable form
CursesError = curses.error

class Curses:

   def __init__(self):
      # we save this in the instance because the global variable has an
      # annoying tendency to go away before we can use it to do "endwin()"
      self.__curses = curses
   
   def initscr(self):
      """
         Initializes the curses session and returns the main window.
      """
      return curses.initscr()
      
   def endwin(self):
      """
         Ends the curses session.
      """
      self.__curses.endwin()

   def startColor(self):
      """
	 Enable colored characters.
      """
      curses.start_color()

   def cursSet(self, visibility):
      """
	 Sets cursor visibility.

	 parms:
	    visibiity::
	       [int] 0 = invisible, 1 = visible, 2 = very visible
      """
      curses.curs_set(visibility)

   def newwin(self, height, width, y0, x0):
      """
         Creates a new toplevel window and returns it.
      """
      return curses.newwin(height, width, y0, x0)
   
   def noecho(self):
      return curses.noecho()
   
   def mousemask(self, newMask):
      "Sets the new mask, returns the old mask"
      if _useNCurses:
         mmask = _curses.ptrcreate('long', 0, 1)
         curses.mousemask(newMask, mmask)

   def beep(self):
      curses.beep()

   def makeEvent(self, ch):
      """
         Makes the appropriate event instance for the character /ch/ (an 
         integer) and returns it.
      """
      # is it a mouse event?
      if _useNCurses and ch == curses.KEY_MOUSE:
         evt = makeMouseEvent()
      else:
         evt = KeyEvent(ch)
      return evt

   def raw(self):
      curses.raw()
   
   def noraw(self):
      curses.noraw()

   def initPair(index, foreground, background):
      """
	 Generates a color pair attribute and binds it to an index.
      """
      return curses.init_pair(index, foreground, background)
   initPair = staticmethod(initPair)

   def colorPair(index):
      """
	 Returns an attribute (suitable for use with any of the functions
	 accepting text attributes) for the given color pair index bound with
	 @make_pair()
      """
      return curses.color_pair(index)
   colorPair = staticmethod(colorPair)


for _attrib in dir(curses):
   if _attrib[:3] == 'KEY' or _attrib[0] == 'A' or _attrib[:5] == 'COLOR':
      setattr(Curses, _attrib, getattr(curses, _attrib))
