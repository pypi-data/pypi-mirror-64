
import string
from Control import Control
from KeyEvent import KeyEvent

class Entryfield(Control):
   """
      An entryfield for single line text fields.
   """
   
   def paint(self):
      if self.__focused:
         attrib = self.A_REVERSE
      else:
         attrib = self.A_NORMAL

      # compute the endpoint on the slice that we are going to take from the
      # content
      end = self.__offset + self.__width - 2
      
      # compute the content string - the part of the value that we are going
      # to display
      content = self.__value[self.__offset:end]

      # if this is a "secret" field (contents are not displayed), convert
      # the content string to a string of asterisks      
      if self.__secret:
         content = len(content) * '*'
               
      # pad it to fit the width of the control
      content = string.ljust(content, self.__width - 2)

      # draw the entire control      
      self.move(0, 0)
      self.write('[%s]' % content, attrib)
      
      # reset the cursor position
      if self.__focused:
         self.leaveok(0)
         self.move(0, self.__cursor - self.__offset + 1)
      else:
         # if unfocused, don't want to see a cursor here
         self.leaveok(1)
      
      self.refresh()
   
   def __init__(self, parent, x0, y0, width = 16, maxEntry = 16, value = '',
                secret = 0
                ):
      Control.__init__(self, parent, x0, y0, width, 1)
      self.__width = width
      self.__max = maxEntry
      self.__value = value
      self.__offset = 0
      self.__cursor = 0
      self.__focused = 1
      self.__secret = secret
      self.paint()

   def takeFocus(self):
      self.__focused = 1
      self.paint()
   
   def releaseFocus(self):
      self.__focused = 0
      self.paint()

   def getText(self):
      "returns the text of the entryfield"
      return self.__value
   
   def setText(self, text):
      """
         Sets the text of the entryfield, resets cursor and start pos, and
         repaints.
      """
      self.__value = text
      self.__offset = 0
      self.__cursor = 0
      self.paint()
   
   def processEvent(self, evt):
      if isinstance(evt, KeyEvent):
         
         # if it is a printable character we want to insert it into to the
         # contents at the cursor position.
         if evt.code >= 32 and evt.code < 127:
            
            # make sure that there is room to insert
            if len(self.__value) >= self.__max:
               self.error()
               return 1
            
            # insert into the value
            self.__value = self.__value[:self.__cursor] + chr(evt.code) + \
               self.__value[self.__cursor:]
            
            # modify the cursor position
            self.__cursor = self.__cursor + 1
            
            # calculate the cursor position relative to the beginning of the
            # field
            pos = self.__cursor - self.__offset + 1
            
            # if we have just moved out of the field of view, adjust the
            # field of view and repaint everything
            if pos > self.__width - 2:
               self.__offset = self.__offset + 1
               pos = pos + 1
            
            
            # repaint the rest of the field
            self.paint()
            return 1
         
         # now deal with the special chars
         else:
            if evt.code == self.KEY_LEFT:
               if not self.__cursor:
                  self.error()
               else:
                  self.__cursor = self.__cursor - 1
            elif evt.code == self.KEY_RIGHT:
               if self.__cursor == len(self.__value):
                  self.error()
               else:
                  self.__cursor = self.__cursor + 1
            elif evt.code in (self.KEY_BACKSPACE, 8):
               if self.__cursor == 0:
                  self.error()
               else:
                  self.__value = self.__value[:self.__cursor - 1] + \
                     self.__value[self.__cursor:]
                  self.__cursor = self.__cursor - 1
            elif evt.code in (self.KEY_HOME, 1):
               self.__cursor = 0
            elif evt.code in (self.KEY_END, 5):
               self.__cursor = len(self.__value)
            else:
               return 0
            
            # if the cursor is out of view to the left or to the right
            # adjust the offset so that it is on the edge of the view.
            if self.__cursor < self.__offset:
               self.__offset = self.__cursor
            elif self.__cursor >= self.__offset + self.__width - 2:
               self.__offset = self.__cursor - self.__width + 3
            self.paint()
            
            return 1
                  
