
from Event import Event

def makeMouseEvent():
   """
      Creates a new @MouseEvent from the information obtained from
      curses getmouse function.
   """
   curses.getmouse(evt)
   return MouseEvent(evt.x, evt.y, evt.bstate)

class MouseEvent(Event):
   """
      Represents mouse events.
      
      Public Variables:
      /x/::
         Mouse x position.
      /y/::
         Mouse y position.
      /state/::
         Mouse button state, indicates event rather than current state.
   """
         
   def __init__(self, name, x, y, state):
      Event.__init__(self, name)
      self.x = x
      self.y = y
      self.state = state
      