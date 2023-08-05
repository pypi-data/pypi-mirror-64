#==============================================================================
#
#  $Id: StdError.py 800 2003-03-31 23:03:12Z mike $
#
"""
   Standard error classes and utilities.
"""
#
#  Copyright (C) 1998 Michael A. Muller
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#  $Log: StdError.py,v $
#  Revision 1.5  2003/03/31 23:03:12  mike
#  Replaced use of exc_tracback (unsupported in python 2.2) with exc_info()[2]
#  (from cregan).
#
#  Revision 1.4  2000/02/13 20:12:20  mike
#  Converted comments to docstrings.
#
#  Revision 1.3  1998/10/27 18:17:29  mike
#  Created errorText() method, which pretty much does what exlocstr
#  should have
#
#  Revision 1.2  1998/10/23 00:50:26  mike
#  Added header
#
#
#==============================================================================

from spug.io.LineReader import LineReader
import string, traceback

class ImplementedBySubclassError(Exception):
   """

      This should be raised by a functions that exist in base classes that
      should be overriden by a subclass.
      
      XXX this class is obsolete - I didn't understand that *NotImplemented*
      is used for this.
   """

   def __init__(self, txt = ''):
      Exception.__init__(self, txt)


class BadParmError(Exception):
   """
      This should be raised by a function when a parameter value is not what
      it expected.
      
      XXX obsolete - didn't know about ValueError.
   """

   pass

class AdditionalText:
   """
      Mix-in for exception classes that allow text to be added at several levels
      of exception handling.
   """
   
   def __init__(self, text = None):
      if text:
         self.text = [ text ]
      else:
         self.text = []
   
   def addText(self, newText):
      "Adds /newText/ to the exception text list."
      self.text.append(newText)
   
   def getText(self):
      """
         Returns the complete exception text as a single string, with individual
         exception items seperated by newlines.
      """
      return string.join(self.text, '\n')

class FileParseError(Exception):
   """
      Raised when a parse error is encountered while reading a text file.
      If the file is a LineReader, source location information is available.
   """

   def __init__(self, file, text, lineNum = None):
      """
         Constructs a FileFormatError from a file object and a message text
         string. 
         
         If a line number is explicitly provided or a LineReader
         object is used for /file/, the line number of the error is made
         available.
      """
      Exception.__init__(self, text)
      self.file = file
      if lineNum:
         self.lineNum = lineNum
      if isinstance(file, LineReader):
         self.lineNum = file.lineNumber()
      else:
         self.lineNum = None
   
   def getLineNum(self):
      """
         Returns the line number of the source file in which the error
	 occurred. Returns *None* if the file object was not a lineReader.
      """
      return self.lineNum
   
   def getSourceName(self):
      "Returns the name of the source file."
      return self.file.name
   
   def __str__(self):
      "Creates a string containing source information"
      return self.file.name + ':' + str(self.lineNum) + ':' + self[0]

def exlocstr(exinfo = None):
   """
      Creates a stack trace from the given exception info (should be the
      returned from `sys.exc_info()`, the value of the current exception info
      is used if none is supplied).
         
      Returns the stack trace represented as a multi-line string.
      
      Deprecated.  Use errorText() instead.
   """
   import sys
   if not exinfo:
      exinfo = sys.exc_info()
   loc = ''
   tb = exinfo[2] 
   while tb: 
      loc = loc + '  File "' + tb.tb_frame.f_code.co_filename + '", line ' + \
         str(tb.tb_frame.f_lineno) + ', in ' + \
         tb.tb_frame.f_code.co_name + '\n'
      tb = tb.tb_next 
   return loc

def errorText(ex):
   """
      Returns the complete error text for the exception, just as the python
      interpreter would have formatted it, as a multi line string.
      
      This must be called from an exception handler.
      
      This function isn't really very different from 
      `traceback.format_exception()` - except that it can be used in 1.5.1
      and I'm not sure if `format_exception` can.
   """
   import sys
   info = traceback.extract_tb(sys.exc_info()[2])
   retval = 'Traceback (innermost last):\n'
   for file, line, func, src in info:
      retval = retval + '  File "' + file + '", line ' + str(line) + ', in ' + \
         func + '\n'
      
      # add the source line if there is one
      if src:
         retval = retval + '    ' + src + '\n'
   
   if ex:
      retval = retval + ex.__class__.__name__ + ': ' + str(ex)
   return retval
