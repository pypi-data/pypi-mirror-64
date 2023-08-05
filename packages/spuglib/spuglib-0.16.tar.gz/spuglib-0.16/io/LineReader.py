#==============================================================================
#
#  $Id: LineReader.py 1343 2009-01-14 13:15:48Z mmuller $
#
"""
   Class to support tracking line numbers while reading a file.
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
#  $Log: LineReader.py,v $
#  Revision 1.3  2000/05/18 00:05:24  mike
#  Doc fix.
#
#  Revision 1.2  2000/04/05 23:22:17  mike
#  Allowed the specification of the line number upon construction, moved
#  lineNumber() to getLineNumber() preserving old one for compatibility.
#
#  Revision 1.1  1998/11/06 22:20:01  mike
#  Initial revision
#
#
#==============================================================================


class LineReader:

   '''A line reader supports the name attribute and readline() function of a
      file object but none of the others.  Its job is to keep track of line
      numbers in the file object.
      
      Public Variables:
      /name/::
         Name of the file.
   '''

   
   def __init__(self, file, lineNum = 1, name = None):
   
      """
         Constructs a new LineReader from a file object.  If /lineNum/
         is specified, it should be the initial line number.
      """
      
      self.file = file
      self.line = lineNum - 1
      if name:
         self.name = name
      else:
         self.name = file.name
   
   def readline(self):
      
      "Reads and returns the next line from the file."
      
      self.line = self.line + 1
      return self.file.readline()

   def getLineNumber(self):   
      
      """
         Returns the current line number of the file.  This is also
         supported as *lineNumber()* for backwards compatibility.
      """
      
      return self.line

   lineNumber = getLineNumber

   def close(self):
      """
         Closes the LineReader and its associated file.
      """
      self.file.close()
   
