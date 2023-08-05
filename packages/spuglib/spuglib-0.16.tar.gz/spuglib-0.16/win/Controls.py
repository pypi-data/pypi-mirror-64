#==============================================================================
#
#  $Id: Controls.py 1332 2008-11-25 15:37:51Z mmuller $
#
"""
   Simple compound Tkinter controls.
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
#  $Log: Controls.py,v $
#  Revision 1.3  2000/02/13 22:35:04  mike
#  Doc fixes
#
#  Revision 1.2  1999/06/04 20:20:24  mike
#  Fixed comments and changed the order of scrolling list construction and
#  gridding in an attempt to fix the bizarre windows trap.
#
#  Revision 1.1  1998/10/23 00:59:10  mike
#  Initial revision
#
#
#==============================================================================

from spug.win.tk import *


class Choice(Menubutton):
   """
      A java-style choice control: a drop down list.
   """

   class Option:
      """
         Nested class for choices
      """
      def __init__(self, menu, text):
         self.menu = menu
         self.text = text
      
      def selected(self):
         self.menu.configure(text = self.text)

   def __init__(self, 
                parent, 
                contents = [], 
                default = None
                ):
      """
         Constructor.  Contents
      """

      # if no default choice was given, and there is stuff in the list,
      # use the first element of the list as the default.
      if default is None and contents:
         default = contents[0]

      Menubutton.__init__(self, parent, text = default)
      self.dropdown = Menu(self, tearoff = 0)
      self.configure(menu = self.dropdown)
      for cur in contents:
         self.addChoice(cur)
   
   def addChoice(self, choice):
      """
         Adds a new choice to the list (/choice/ is a string).
      """
      self.dropdown.add_command(label = choice, 
                                command = \
                                 self.Option(self, choice).selected
                                )
   
   def setSelection(self, selection):
      """
         Sets the selection to that given.  Does not verify that /selection/
         is a valid choice.
      """
      self.configure(text = selection)
   
   def get(self):
      """
         Gets the currently active selection.
      """
      return self.cget('text')
      

class ScrollingList(Frame):
   """
      A List with associated scrollbars.
   """

   def __init__(self, parent, **kw):
      """
         Constructs a new ScrollingList.
      """
      
      self.list = None
      Frame.__init__(self, parent)
      self.list = Listbox(self, **kw)
      self.list.grid(sticky = N + W + S + E, row = 0, column = 0)
      self.sb = Scrollbar(self, command = self.scrolled)
      self.sb.grid(sticky = N + E + S, row = 0, column = 1)    
      self.hsb = Scrollbar(self, command = self.list.xview,
                           orient = 'horizontal')
      self.hsb.grid(sticky = W + S + E, row = 1, column = 0)
      self.list.config(yscrollcommand = self.sb.set,
                       xscrollcommand = self.hsb.set)

      self.rowconfigure(0, weight = 1)
      self.columnconfigure(0, weight = 1)

   def scrolled(self, *args):
      """
         Command called when the list is scrolled.
      """
      
      self.list.yview(*args)

   def syncScrollbar(self):
      """
         Syncs the scrollbar to the current view of the list.
      """
      pass
      
   def append(self, item):
      """
         Adds a new item to the end of the list.
      """
      self.list.insert('end', item)
   
   def insert(self, index, item):
      """
         Adds a new item at the given index within the list.
      """
      self.list.insert(index, item)

   def fillList(self, items):
      """
         Sets the contents of the list from a list of /items/.  Anything
         that was originally in the list is removed.
      """
      self.list.delete(0, self.list.size() - 1)
      for cur in items:
         self.append(cur)

   def curselection(self):
      """
         Returns a list of all selected item indeces (as integers).
      """
      return map(int, self.list.curselection())

   def firstSelectionIndex(self):
      """
         Returns the index of the first selected item, returns *None* if there
         is no item selected.
      """
      sel = self.curselection()
      if sel:
         return sel[0]
      else:
         return None

   def firstSelection(self):
      """
         Returns the text of the first selected item.  Returns *None* if there
         are no selected items.
      """
      sel = self.curselection()
      if sel:
         return self.list.get(sel[0])
      else:
         return None
   
   def deleteAll(self):
      """
         Deletes the entire list.
      """
      size = self.list.size()
      if size:
         self.list.delete(0, size - 1)
   
   def config(self, **opts):
      """
         provides special configuration processing.  Mostly passes
	 configuration options to the list.
      """
      return self.list.config(**opts)

   def bind(self, sequence, action):
      """
         Overrides Widget.bind to bind events to the listbox instead of the 
         frame.
      """
      return self.list.bind(sequence, action)

   def size(self):
      """
         Overrides Frame.size() to delegate this to the list.
      """
      return self.list.size()

   def __nonzero__(self):
      """
         Keeps this from being delegated by __getattr__.
      """
      return 1

   def __getattr__(self, attr):
      """
         Delegates all other attributes to the list.
      """
      if self.list:
         return getattr(self.list, attr)
      else:
         raise AttributeError(attr)

class ScrollingText(Frame):
   """
      A text control with scrollbars.  Wrap mode is always 'none' for one
      of these because there is a horizontal scrollbar.
   """
   
   def __init__(self, parent = None, **kw):
      self.text = None
      if parent:
         Frame.__init__(self, parent)
      else:
         Frame.__init__(self)
      self.text = Text(self, **kw)
      
      self.vsb = Scrollbar(self, command = self.text.yview)
      
      self.hsb = Scrollbar(self, command = self.text.xview,
                           orient = 'horizontal'
                           )
      
      self.text.config(yscrollcommand = self.vsb.set,
                       xscrollcommand = self.hsb.set,
                       wrap = 'none'
                       )
                       
      self.text.grid(sticky = N+S+E+W)
      self.vsb.grid(row = 0, column = 1, sticky = N+S)
      self.hsb.grid(sticky = W+E)
      self.rowconfigure(0, weight = 1)
      self.columnconfigure(0, weight = 1)
   
   def __getattr__(self, attr):
      if self.text:
         return getattr(self.text, attr)
      else:
         raise AttributeError(attr)

class FullControl(Frame):
   """
      A full control is a control with a label attached to it.
   """

   def __init__(self, parent, label, ctl = None, orientation = LEFT):
      """
         Constructor
      """
   
      Frame.__init__(self, parent)
      
      self.label = Label(self, text = label)
      self.label.pack(side = orientation)
      if ctl:
         self.addCtl(ctl)
   
   def addCtl(self, ctl):
      """
         Used to add a control after construction.
      """
      self.ctl = ctl
      self.ctl.pack(expand = 1)

class FullEntry(FullControl):
   """
      A FullEntry is a combination of a label and an entry field.
   """

   def __init__(self, parent, label, width = 20):
      """
         Constructor.
      """
      
      FullControl.__init__(self, parent, label)
      self.addCtl(Entry(self, width = width))

   def get(self):
      """
         Returns the entries text
      """
      return self.ctl.get()

   def set(self, val):
      """
         Set the text in the entryfield
      """
      cur = self.ctl.get()
      if cur:
         self.ctl.delete(0, len(cur))
      self.ctl.insert(0, val)

class FullChoice(FullControl):
   """
      A full choice is a combination of a label and a menu.
   """


   def __init__(self, 
                parent, 
                label, 
                contents = [], 
                default = None
                ):
      """
         Constructor.
      """

      FullControl.__init__(self, parent, label)
      self.addCtl(Choice(self, contents, default))
   
   def addChoice(self, choice):
      """
         Adds the given choice to the menu.  /choice/ must be a string.
      """
      self.ctl.addChoice(choice)
   
   def setSelection(self, selection):
      """
         Sets the current selection of the menu button.  /selection/ must be
         a string.  No verification is performed to insure that it is a valid
         choice.
      """
      self.ctl.setSelection(selection)
   
   def get(self):
      """
         Returns the current selection in the menu.
      """
      return self.ctl.get()


