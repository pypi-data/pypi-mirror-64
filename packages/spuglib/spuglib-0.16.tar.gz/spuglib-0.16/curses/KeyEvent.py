

from Event import Event

class KeyEvent(Event):
   """
      Public Variables:
      /code/::
         Key code.
   """
   
   def __init__(self, keyCode):
      Event.__init__
      self.code = keyCode
   
   def asChar(self):
      """
         Returns the character value of the key-code.  Will raise a
         ValueError if the key-code is for a non-character value.
      """
      return ord(self.code)
   
   def asString(self):
      """
         Returns the key represented as a symbolic string value.  If the
         key represents a control character (i.e. an ascii code <= 26)
         it will be of the form "Ctrl-/letter/"
      """
   
   def isSpecial(self):
      """
         Returns true if the event is for a "special" (non-ascii character)
         key.
      """
      return self.code > 255
