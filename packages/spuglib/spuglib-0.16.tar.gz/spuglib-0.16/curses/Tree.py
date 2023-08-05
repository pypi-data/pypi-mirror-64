
from Control import Control

class TreeModel:
   """
      Abstract base class for tree objects.
      
      Public-vars:
         expanded::
            [boolean] set to true if the tree object is currently expanded
            (i.e. all children are visible).
   """
   
   def __init__(self, expanded = 0):
      self.expanded = expanded
   
   def hasChildren(self):
      """
         Returns true if the object has any children.
         
         Must be implemented by derived classes.
      """
      raise NotImplementedError()
   
   def getChildren(self):
      """
         Returns a list of all child nodes (list<@TreeModel>).
      """
      raise NotImplementedError()
   
   def __iter__(self):
      """
         Creates a depth-first iterator for the model object.
      """
      return TreeModelIter(self)
   
   def __str__(self):
      """
         Returns a one-line string representation of the object for use
         as its identifier line.
      """
      raise NotImplementedError()

   def expandAll(self):
      """
         Expands the node and all children.
      """
      self.expanded = 1
      for child in self:
         child.expanded = 1
   
   def contractAll(self):
      """
         "Contracts" (unexpands) the node and all children.
      """
      self.expanded = 0
      for child in self:
         child.expanded = 0

class TreeModelIter:
   
   """
      Public-vars:
         iterateAll::
            [boolean] if true, iterate all children.  If false, iterate only
            expanded children.
   """
   
   def __init__(self, model):
      self.stack = [(model, 0)]
      self.cur = model
      self.iterateAll = 1
   
   def next(self):
      if self.cur.hasChildren() and (self.iterateAll or self.cur.expanded):
         firstChild = self.cur.getChildren()[0]
         self.stack.append((firstChild, 0))
         self.cur = firstChild
         return self.cur
      else:
         while 1:
            lastChild, index = self.stack.pop()
            if self.stack:
               self.cur, parIndex = self.stack[-1]
               peers = self.cur.getChildren()
               index += 1
               if index < len(peers):
                  self.cur = peers[index]
                  self.stack.append((self.cur, index))
                  return peers[index]
            else:
               raise StopIteration()

   def __iter__(self):
      """
         Returns the iterator.  Makes it easy to use the iterator in a for
         loop.
      """
      return self

   def copy(self):
      dup = TreeModelIter(self)
      dup.stack = self.stack[:]
      dup.cur = self.cur
      dup.iterateAll = self.iterateAll
      return dup

   def depth(self):
      """
         Returns the current depth of the iterator (levels of nesting).
      """
      return len(self.stack)

   def __cmp__(self, other):
      """
         Compares two iterators: iterators are equal if they reference
         the same node.
      """
      return self.cur is not other.cur

class DefaultTreeModel(TreeModel):
   """
      Simple tree object, allows you to add children and associated
      nodes with a "parcel" which is used for the description string.
   
      Public-vars:
         parcel::
            [any] object that the tree object is displaying.
   """
   
   def __init__(self, parcel = None, children = None, expanded = True):
      if children is None:
         children = []
      TreeModel.__init__(self, expanded)
      self.__parcel = parcel
      self.__children = children
   
   def __get_parcel(self):
      return self.__parcel
   
   def __set_parcel(self, parcel):
      self.__parcel = parcel
      self.dispatchEvent(TreeNodeChangeEvent(parcel))
   
   parcel = property(__get_parcel, __set_parcel)
   
   def addChild(self, child):
      """
         parms:
            child::
               [@TreeModel]
      """
      self.__children.append(child)
   
   def hasChildren(self):
      return bool(self.__children)
   
   def getChildren(self):
      return self.__children
   
   def __str__(self):
      return str(self.__parcel)

class Tree(Control):
   
   def __init__(self, parent, x0, y0, width, height, indent = 3, roots = []):
      Control.__init__(self, parent, x0, y0, width, height)
      self.__indent = 3
      self.__root = DefaultTreeModel(children = roots)
      self.__root.expandAll()
      self.__top = iter(self.__root)
      self.__top.iterateAll = 0
      self.__active = iter(self.__root)
      self.__active.next()
      self.paint()
   
   def __drawFrom(self, pos):
      cur = self.__top.copy()
      i = 0
      while i < pos:
         i += 1
         cur.next()
      for i in cur:
         if pos >= self._height:
            break
         self.writeAt(0, pos, self.__indent * ' ' * cur.depth())
         if cur == self.__active:
            attr = self.A_REVERSE
         else:
            attr = 0
         self.write(`i.parcel`, attr)
         pos += 1
      
      # clear any space at the bottom
      self.clrtobot()
      
      self.refresh()
   
   def paint(self):
      self.__drawFrom(0)

   def processEvent(self, evt):
      if isinstance(evt, KeyEvent):
         if evt.code == ord('u'):
            self.beep()
            return 1
         if evt.code == self.KEY_UP:
            self.__active.prev()
            self.paint()
            return 1
         elif evt.code == self.KEY_DOWN:
            self.__active.next()
            self.paint()
            return 1
      return 0

if __name__ == '__main__':
   print 'creating tree base...',
   tree = DefaultTreeModel('root')
   print 'ok'
   
   print 'adding children...',
   tree.addChild(DefaultTreeModel(1))
   tree.addChild(DefaultTreeModel(2))
   node = DefaultTreeModel(3)
   tree.addChild(node)
   node.addChild(DefaultTreeModel(4))
   tree.addChild(DefaultTreeModel(5))
   print 'ok'

   print 'doing child iteration...',   
   list = []
   for child in tree:
      list.append(child.parcel)
   if list == [1, 2, 3, 4, 5]:
      print 'ok'
   else:
      print 'failed'

   print 'iterator copy...',
   cur = iter(tree)
   while 1:
      child = cur.next()
      if child.parcel == 3:
         cur = cur.copy()
         break
   list = []
   for val in cur:
      list.append(val.parcel)
   if list == [4, 5]:
      print 'ok'
   else:
      print 'failed'

   print 'iterator depth...',
   cur = iter(tree)
   for val in cur:
      if val.parcel == 3 and cur.depth() == 2:
         print 'ok'
         break
   else:
      print 'failed'

   import sys
   if len(sys.argv) > 1 and sys.argv[1] == 'g':
      from App import App
      from KeyEvent import KeyEvent
      class MyApp(App):
         def processEvent(self, evt):
            if App.processEvent(self, evt):
               return 1
            if isinstance(evt, KeyEvent) and evt.code == ord('q'):
               self.terminate()

      try:      
         app = MyApp()
         tv = Tree(app, 1, 1, 20, 20, roots = [tree])
         app.mainloop()
      except Exception, ex:
         import traceback
         type, val, tb = sys.exc_info()
         del app
         errorText = '\n'.join(traceback.format_exception(type, val, tb))
         print errorText
         open('error.txt', 'w').write(errorText)

               