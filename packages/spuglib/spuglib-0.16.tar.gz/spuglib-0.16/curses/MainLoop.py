#==============================================================================
#
#  $Id: MainLoop.py 1057 2006-08-23 23:08:16Z mike $
#
"""
   Module for MainLoop class.
"""
#
#  Copyright (C) 1999 Michael A. Muller
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
#  $Log: MainLoop.py,v $
#  Revision 1.1  2000/03/28 01:36:04  mike
#  Created new class to house common "main loop" functionality.
#
#
#==============================================================================

import weakref
from spug.io.reactor import Reactable, Dispatcher

class CharGetter(Reactable):

   def __init__(self, mainloop):
      self.__mainloop = weakref.proxy(mainloop)

   def wantsToRead(self):
      return True

   def wantsToWrite(self):
      return False

   def handleRead(self, reactor):
      self.__mainloop._processEvent()

   def handleWrite(self, reactor):
      raise Exception("shouldn't be trying to write to a CharGetter")

   def handleError(self, reactor):
      pass

   def handleDisconnect(self, reactor):
      pass

   def fileno(self):
      return 0

class MainLoop:
   """
      Mix-in base class for windows that have a @mainloop() method.
   """

   def __init__(self):
      self.__dispatcher = Dispatcher()
      self.__dispatcher.addReactable(CharGetter(self))
      self.__finished = 0

   def terminate(self):
      """
         Causes the main loop to terminate.
      """
      self.__finished = 1

   def addConnection(self, connection):
      """
         Adds another connection to listen to for input.
      """
      self.__dispatcher.addReactable(connection)

   def getDispatcher(self):
      """
         Provides access to the underlying reactor dispatcher.
      """
      return self.__dispatcher

   def _processEvent(self):
      # get the next character, convert it to an event object, and
      # dispatch its event
      evt = self.getEvent()         
      self.processEvent(evt)

   def mainloop(self):
      """
         Continue processing events until terminated.
      """
      self.__finished = 0
      while not self.__finished:
         self.__dispatcher.processOneEvent()
   
