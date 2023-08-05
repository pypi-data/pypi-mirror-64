#==============================================================================
#
#  $Id: StdWin.py 684 2000-05-18 00:09:20Z mike $
#
"""
   A set of standardized complete windows.
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
#  $Log: StdWin.py,v $
#  Revision 1.5  2000/05/18 00:09:20  mike
#  Doc fix.
#
#  Revision 1.4  2000/02/13 22:35:04  mike
#  Doc fixes
#
#  Revision 1.3  1999/05/23 17:41:35  mike
#  Fixed message box focus issues.
#
#  Revision 1.2  1999/04/08 01:01:35  mike
#
#  First cut at phunkyvw; on StdWin fixed docs and cleaned-up functionality.
#
#  Revision 1.1  1998/10/23 00:59:51  mike
#  Initial revision
#
#
#==============================================================================

from spug.win.Controls import *
from spug.win.bind import KeyBinder

class ListView(Frame, KeyBinder):
   """
      A list view provides a boiler-plate list viewer.  It is a ScrollingList
      object with a set of buttons at the bottom.  Derived classes may define
      their own buttons for the view.
      
      A ListView is arranged on a grid which leaves the 0th row unoccupied, so
      that derived classes can add a menu (or whatever they want, for that
      matter) to the top.
   """

   def quitPressed(self):
      """
         Obsolete form of @_quit().  Do not use.
      """
      self.parent.destroy()
   
   def _quit(self):
      """
         Called when the quit button is pressed.  Derived classes should
         override this if they want to intercept "Quit" processing.
      """
      self.quitPressed()

   def fillList(self, data):
      """
         Fills the list with /data/, which should be a list of strings.
         The listbox's current contents are destroyed.
      """
      self.list.fillList(data)

   def _setFixedFont(self):
      try:
         self.list.config(font = "-bitstream-courier-medium-r-*-*-*-*-*")
      except:
         pass

   def getTop(self):
      """
         Returns the lists Toplevel.
      """
      return self.parent

   def __init__(self, data = None, width = 40, height = 20, fixedFont = 0,
                selectMode = BROWSE):
      """
         Constructs a ListView.  If data is provided, it is a list of strings
         with which to populate the listbox.  /fixedFont/ is used to indicate
         that the listbox is to be fixed font.
         
         /selectMode/ indicates the Tk mode of selection.  Modes of selection
         are as follows:
             *SINGLE*::
                One item may be selected.
             *BROWSE*::
                Like single, but you can move the mouse with the button down.
             *MULTIPLE*::
                Select and unselect as many items as you want with a 
                mouse-click.
             *EXTENDED*::
                Select as many items as you want by sweeping them with the 
                mouse.  Control-button-1 sweep to select a non-adjacent set.
      """
      self.parent = Toplevel()
      Frame.__init__(self, self.parent)
      KeyBinder.__init__(self, self.parent)

      self.list = ScrollingList(self, width = width, height = height)
      if fixedFont:
         self._setFixedFont()
      self.list.config(selectmode = selectMode)
      self.list.grid(row = 1, sticky = N + S + E + W)
      
      if data:
         self.fillList(data)
      
      self.bpnl = Frame(self)
      self.quit = Button(self.bpnl, text = 'Quit', command = self._quit)
      self.quit.pack(side = LEFT)
      self.bpnl.grid(row = 2, sticky = W)
      self.columnconfigure(0, weight = 1)
      self.rowconfigure(1, weight = 1)
      self.pack(expand = 1, fill = 'both')      
      
   def addButton(self, name, cmd):
      """
         Adds a new button to the button panel at the bottom with the given
         name and command.  Returns the new button.
      """
      btn = Button(self.bpnl, text = name, command = cmd)
      btn.pack(side = LEFT)
      return btn

class MessageBox(Frame, KeyBinder):
   """
      Provides a generic message box with reasonable defaults.  Text is
      displayed in a label with a wraplength of 40.  The set of buttons is
      configurable.
   """
   
   class BoxButton(Button):
      """
         BoxButton may only be used by MessageBox.  It is the kind of button that
         must be used by a message box to trigger the events properly.
      """
      
      def __init__(self, parent, owner, name, index, state = 'normal'):
         Button.__init__(self, parent, text = name, command = self.pressed,
                         state = state
                         )
         self.owner = owner
         self.index = index
      
      def pressed(self):
         self.owner.buttonPressed(self.index)
   
   def __init__(self, txt, buttons = ['OK'], default = 0):
      """
         Creates a message box with the given message.  Buttons can specify a
         list or tuple of the names of the buttons.  The index of the name
         will be the value returned by the @show() method.  /default/ indicates
         the index of the default pushbutton.
      """
      self.parent = Toplevel()
      Frame.__init__(self, self.parent)
      KeyBinder.__init__(self)
      self.text = Label(self, text = txt) #, wraplength = 40)
      self.text.pack(side = TOP)
      self.bpnl = Frame(self)
      i = 0
      for b in buttons:
         if default == i:
            newButton = self.BoxButton(self.bpnl, self, b, i, 
                                       state = 'active'
                                       )
            self.bindKey('Return', newButton.pressed)
            newButton.focus()
         else:
            newButton = self.BoxButton(self.bpnl, self, b, i)
         newButton.pack(side = LEFT)
         i = i + 1
      self.bpnl.pack(side = TOP)
      self.pack()
      self.tkraise()
   
   def buttonPressed(self, index):
      """
         Function called when a box button is pressed.
      """
      self.index = index
      self.parent.destroy()

   def show(self):
      """
         Displays the message box modally.  Returns the button that was pressed.
      """
      self.wait_window(self)
      return self.index

class EntryBox(Frame):
   """
      Window to get a single line of input from the user.  Contains an optional
      label, an entryfield, and OK and Cancel buttons.
   """

   def okPressed(self):
      self.text = self.entry.get()
      self.parent.destroy()

   def cancelPressed(self):
      self.parent.destroy()

   def __init__(self, width = 30, labelText = None, initText = None):
      """
         Constructs an EntryBox with an entry field of the given /width/.
         
         If /labelText/ is provided, a label is constructed at the top of the
         window with the given text.  
      """
      self.parent = Toplevel()
      Frame.__init__(self, self.parent)
      if labelText:
         self.label = Label(self, text = labelText)
         self.label.pack(side = TOP)
      self.entry = Entry(self, text = initText or '')
      self.entry.pack()
      
      self.buttonPnl = Frame(self)
      self.okBtn = Button(self.buttonPnl, 
                          text = 'OK', 
                          command = self.okPressed, 
                          state = 'active'
                          )
      self.okBtn.pack(side = LEFT)
      self.cancelBtn = Button(self.buttonPnl,
                              text = 'Cancel',
                              command = self.cancelPressed
                              )
      self.cancelBtn.pack(side = LEFT)
      self.buttonPnl.pack(side = TOP, anchor = W)
      self.pack()
      
      self.text = None
      self.parent.title('Please enter a response')

   def show(self):
      """
         Displays the window and returns the text that is received from the 
         user.  If the *cancel* button is pressed, returns None.
      """
      self.wait_window(self)
      return self.text

