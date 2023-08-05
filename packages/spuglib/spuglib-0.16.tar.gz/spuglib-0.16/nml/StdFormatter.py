#==============================================================================
#
#  $Id: StdFormatter.py 874 2005-11-10 23:14:21Z mike $
#
"""
   Standard formatter class file.
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
#  $Log: StdFormatter.py,v $
#  Revision 1.4  2000/02/13 22:08:52  mike
#  Doc fixes.
#
#  Revision 1.3  1998/11/03 00:42:28  mike
#  Fixed project references.
#  
#  Revision 1.2  1998/06/14 00:46:44  mike
#  Added the _curIsEmpty() method and formatting to insure that a period
#  is followed by two spaces.
#
#  Revision 1.1  1998/06/11 01:23:23  mike
#  Initial revision
#
#
#==============================================================================

import string, re
from spug.util.StdError import ImplementedBySubclassError

class StdFormatter:
   "Contains utilities useful to all formatters."

   wsrx = re.compile(r'\s+')

   def __init__(self):
      self.buf = ''
      self.maxLineWidth = 80

      # this is true if the buffer begins at the start of the line
      self.__atLineStart = True

   def _flush(self, pos):
      "Flushes up to and including position /pos/ in the buffer."
      self.__atLineStart = self.buf[:pos] == '\n'
      pos = pos + 1
      self._commit(self.buf[:pos])
      self.buf = self._makeLine(self.buf[pos:])

   def _write(self, str):
      """
         Used by the formatting functions to write information to the
         buffered output stream.  The output will be buffered unless it
         contains a newline, in which case the buffer will be committed up
         to the last newline.
      """
      self.buf = self.buf + str

      # if the buffer now contains a newline, flush up to the newline
      lastNewline = string.rfind(self.buf, '\n')
      if lastNewline >= 0:
         self._flush(lastNewline)

   def _reduce(self):
      """
         Called when the receiver's buffer exceeds the maximum line length.
         Flushes the receiver up to the point of the last whitespace region
         under the maximum line length.

         If the buffer has no whitspace zone below the maximum line space,
         flushes up to the first white space.
      """

      # find the first whitespace
      nextWS = self.wsrx.search(self.buf)
      
      # if the first whitespace is beyond the maximum line width, truncate
      # at the first whitespace
      if not nextWS:
         self._commit(self.buf)
         self.buf = self._makeLine('')
         return
      elif self._tooLong(self.buf[:nextWS.start()]):
         # write and truncate the first part of the buffer
         self._commit(self.buf[:nextWS.start()] + '\n')
         self.buf = self._makeLine(self.buf[nextWS.end():])
         return
         
      while 1:
         lastWS = nextWS
         nextWS = self.wsrx.search(self.buf, lastWS.end())
         if not nextWS or self._tooLong(self.buf[:nextWS.start()]):
            # write and truncate the first part of the buffer
            self._commit(self.buf[:lastWS.start()] + '\n')
            self.buf = self._makeLine(self.buf[lastWS.end():])
            return

   def _writeSpace(self):
      """
         Used to indicate that white space is needed between the previous
         written object and the next one.  This function will add the
         appropriate amount of whitespace (possibly none) depending on the
         state of the buffer.
   
         If the buffer exceeds the maximum line width (/maxLineWidth/), part of
         it will be committed using @_reduce().
      """
      # if there is a non-whitespace character at the end of the string,
      # add whitespace to it.
      if self.buf and self.buf[-1:] not in string.whitespace:
         # use a double space if the line ended with a period
         if self.buf[-1] == '.':
            self.buf = self.buf + '  '
         else:
            self.buf = self.buf + ' '

      # if we have exceeded our boundaries, flush part of the buffer.
      if self._tooLong(self.buf):
         self._reduce()    


   def _tooLong(self, line):
      """
         Returns true if the given line is too long to fit on the
         rendering destination.
   
         By default, this compares the length of the line to *maxLineWidth*.
         derived classes should override this to implement layout rules that
         take into account things like font size.
      """
      return len(line) > self.maxLineWidth

   def  _makeLine(self, line):
      "Derived classes may overload this to implement their own indentation."
      return line

   def _commit(self, data):
      """
         Must be implemented by subclass.  Writes the raw data to the final
         consumer.
      """
      raise ImplementedBySubclassError()

   def _atLineStart(self):
      """
	 Returns true if we are currently at the beginning of a line (if the
	 last thing written was a newline or nothing has been written)
      """
      return self.__atLineStart and not self.buf or self.buf[-1:] == '\n'

   def _startLine(self):
      """
	 Writes a newline if we are not already at the beginning of a line.
      """
      if not self._atLineStart():
	 self._write('\n')

   def _curIsEmpty(self):
      """
         Returns true if the current line is empty (consists entirely of
         whitespace).
      """
      return string.strip(self.buf) == ''

   def close(self):
      """
         Closes the formatting of the block, committing the contents of the
         buffer.
      """
      self._commit(self.buf)
