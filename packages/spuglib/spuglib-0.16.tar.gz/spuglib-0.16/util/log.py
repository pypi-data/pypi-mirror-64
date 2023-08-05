#==============================================================================
#
#  $Id$
#
"""
   Simple logger interface that will grow to suit my needs.
"""
#
#  Copyright (C) 2006 Michael A. Muller
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
#==============================================================================

import sys, os, syslog, traceback

EMERG = 0
ALERT = 1
CRIT = 2
ERR = 3
WARN = WARNING = 4
NOTICE = 5
INFO = 6
DEBUG = 7

class LogWriter:
   """
      Interface for classes wishing to implement a "logging destination" - a
      place to write to.
   """

   def debug(self, msg, *args, **kwargs):
      """
	 Logs a debug message.  Must be implemented by derived classes.
      """
      raise NotImplementedError()

   def info(self, msg, *args, **kwargs):
      """
	 Logs a info message.  Must be implemented by derived classes.
      """
      raise NotImplementedError()

   def notice(self, msg, *args, **kwargs):
      """
	 Logs a notice message.  Must be implemented by derived classes.
      """
      raise NotImplementedError()

   def warn(self, msg, *args, **kwargs):
      """
         Logs a warning message.  Must be implemented by derived classes.
      """
      raise NotImplementedError()

   def error(self, msg, *args, **kwargs):
      """
	 Logs an error message.  Must be implemented by derived classes.
      """
      raise NotImplementedError()
   
   def _format(self, msg, args, kwargs):
      # loggers _must not throw exceptions_
      try:
         if args:
            return msg % args
         elif kwargs:
            return msg % kwargs
         else:
            return msg
      except:
         
         try:
            self.error('Unable to format log message %s, '
                        'args = %s, kwargs = %s' % 
                        (repr(msg), repr(args), repr(kwargs))
                       )
            return '%s(%s, %s)' % (msg, args, kwargs)
         except:
            self.error('Unable to format or even stringify log message.')
            return 'Unformattable log message'                              

class StreamLogWriter(LogWriter):
   """
      Implements a @LogWriter on top of a standard python stream (aka file
      interface).
   """

   def __init__(self, out):
      self.__out = out

   def __write(self, msg):
      try:
         self.__out.write(msg + '\n')
         self.__out.flush()
      except:
         try:
            # fall back to syslog
            _getSyslogLogger().error('Failed to write log message: %s' %
                                    traceback.format_exc()
                                    )
            _getSyslogLogger().info(msg)
         except:
            # finally, just give up
            pass

   def debug(self, msg, *args, **kwargs):
      self.__write('DEBUG: %s' % self._format(msg, args, kwargs))

   def info(self, msg, *args, **kwargs):
      self.__write('INFO: %s' % self._format(msg, args, kwargs))

   def notice(self, msg, *args, **kwargs):
      self.__write('NOTICE: %s' % self._format(msg, args, kwargs))

   def warn(self, msg, *args, **kwargs):
      self.__write('WARN: %s' % self._format(msg, args, kwargs))

   def error(self, msg, *args, **kwargs):
      self.__write('ERROR: %s' % self._format(msg, args, kwargs))

   def critical(self, msg, *args, **kwargs):
      self.__write('CRITICAL: %s' % self._format(msg, args, kwargs))

class SyslogLogger(LogWriter):
   """
      Implements @LogWriter on top of syslog.
   """

   def __init__(self, ident = 'syslog', logopt = 0, 
		facility = syslog.LOG_USER
		):
      syslog.openlog(ident, logopt, facility)

   def debug(self, msg, *args, **kwargs):
      syslog.syslog(syslog.LOG_DEBUG, self._format(msg, args, kwargs))

   def info(self, msg, *args, **kwargs):
      syslog.syslog(syslog.LOG_INFO, self._format(msg, args, kwargs))

   def notice(self, msg, *args, **kwargs):
      syslog.syslog(syslog.LOG_NOTICE, self._format(msg, args, kwargs))

   def warn(self, msg, *args, **kwargs):
      syslog.syslog(syslog.LOG_WARNING, self._format(msg, args, kwargs))

   def error(self, msg, *args, **kwargs):
      syslog.syslog(syslog.LOG_ERR, self._format(msg, args, kwargs))

   def critical(self, msg, *args, **kwargs):
      syslog.syslog(syslog.LOG_CRIT, self._format(msg, args, kwargs))

# demand-create the syslog logger (needed if logging fails)
_syslogLogger = None
def _getSyslogLogger():
   global _syslogLogger
   if _syslogLogger is None:
      _syslogLogger = SyslogLogger()
   return _syslogLogger

# default is to write to stderr
_logger = StreamLogWriter(sys.stderr)

def setLogWriter(logger):
   """
      Sets the default, application-wide log writer.

      parms:
         logger::
            [@LogWriter]
   """
   global _logger
   _logger = logger

_logLevel = INFO
def _setLogLevel():
   global _logLevel
   level = os.environ.get('SPUG_LOG_LEVEL')
   if level == 'DEBUG':
      _logLevel = DEBUG
   elif level == 'INFO':
      _logLevel = INFO
   elif level == 'NOTICE':
      _logLevel = NOTICE
   elif level == 'WARN':
      _logLevel = WARN
   elif level == 'WARNING':
      _logLevel = WARNING
   elif level == 'ERR':
      _logLevel = ERR
   elif level == 'CRIT':
      _logLevel = CRIT
   elif level == 'ALERT':
      _logLevel = ALERT
   elif level == 'EMERG':
      _logLevel = ALERT

def debug(msg, *args, **kwargs):
   global _logLevel
   if _logLevel >= DEBUG:
      _logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
   global _logLevel
   if _logLevel >= INFO:
      _logger.info(msg, *args, **kwargs)

def notice(msg, *args, **kwargs):
   global _logLevel
   if _logLevel >= INFO:
      _logger.notice(msg, *args, **kwargs)

def warn(msg, *args, **kwargs):
   global _logLevel
   if _logLevel >= WARN:
      _logger.warn(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
   global _logLevel
   if _logLevel >= ERR:
      _logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
   global _logLevel
   if _logLevel >= CRIT:
      _logger.critical(msg, *args, **kwargs)

# set the log level from the environment
_setLogLevel()
