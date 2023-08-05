

class Observable:
   """
      Manages a list of observers and sends events to them.
   """
   
   def __init__(self):
      self.__observers = []
   
   def addObserver(self, eventHandler):
      """
         Adds a new observer to the set.
         
         parms:
            eventHandler::
               [@spug.curses.EventHandler.EventHandler]
      """
      self.__observers.append(eventHandler)
   
   def sendEvent(self, event):
      """
         Sends an event to all observers.
         
         parms:
            event::
               [@spug.curses.Event.Event]
      """
      for obs in self.__observers:
         obs.sendEvent(event)
   