
from App import App
from KeyEvent import KeyEvent
from Entryfield import Entryfield
from Label import Label
from Listbox import Listbox
from SimpleTextViewer import SimpleTextViewer
from Control import Control

class MyApp(App):
   
   def processEvent(self, evt):
      if not App.processEvent(self, evt) and isinstance(evt, KeyEvent):
         if evt.code == ord('q') or evt.code == 27:
            self.terminate()
         elif evt.code == 10:
            list.append(e0.getText())
            list.paint()
            e0.setText('')
         

class MyCtl(Control):
   
   def __init__(self, parent, x0, y0):
      Control.__init__(self, parent, x0, y0, 4, 1)
      self.__last = 0
   
   def paint(self):
      self.move(0, 0)
      self.write(str(self.__last))
      self.refresh()
   
   def processEvent(self, evt):
      if isinstance(evt, KeyEvent):
         self.__last = evt.code
         self.paint()

   
   

a = None

text = '''This is a really lengthy text entry, much too big to fit into the
wimpy space that I have allocated for it.  However, it will be a suitable
illustration of the new truncation features of the text viewer.
'''

try:
   a = MyApp()
   m = MyCtl(a, 1, 1)
   l0 = Label(a, 10, 10, "Name:")
   e0 = Entryfield(a, 20, 10)
   l0 = Label(a, 10, 12, "Rank:")
   e1 = Entryfield(a, 20, 12)
   list = Listbox(a, 10, 13, 10, 10, [])
   textViewer = SimpleTextViewer(a, 22, 13, 16, 5, text)
   a.mainloop()
except:
   if a: del a
   import sys
   import traceback
   traceback.print_exc(sys.exc_info())


