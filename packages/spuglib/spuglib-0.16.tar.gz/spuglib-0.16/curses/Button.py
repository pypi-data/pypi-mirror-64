
from Control import Control
from KeyEvent import KeyEvent

class Button(Control):
   """
      Textual "pushbutton".
   """
   
   def paint(self):
      if self.__hasFocus:
         self.writeAt(0, 0, '[' + self.__text + ']', self.A_REVERSE)
      else:
         self.writeAt(0, 0, '[' + self.__text + ']')
      self.leaveok(1)
      self.refresh()
   
   def __init__(self, parent, x, y, text, onClick):
      Control.__init__(self, parent, x, y, len(text) + 2, 1)
      self.__text = text
      self.__hasFocus = 1
      self.__onClick = [ onClick ]
      self.paint()
   
   def releaseFocus(self):
      self.__hasFocus = 0
      self.paint()
   
   def takeFocus(self):
      self.__hasFocus = 1
      self.paint()

   def processEvent(self, evt):
      if isinstance(evt, KeyEvent):
         if evt.code == 10 or evt.code == 32:
            self.__onClick[0]()
      