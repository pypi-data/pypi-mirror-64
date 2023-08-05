#==============================================================================
#
#  $Id: shell.py 556 2000-02-13 21:58:52Z mike $
#
"""
   Utilities to make it easy to do in python what you can easily do in 
   bash.
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
#  $Log: shell.py,v $
#  Revision 1.2  2000/02/13 21:58:52  mike
#  Doc fixes.
#
#  Revision 1.1  1999/02/03 01:55:30  mike
#  Initial revision
#
#
#==============================================================================

import os
from os import mkdir
import string, re, time

def mtime(file): 
   "Returns the modification time of the file"
   return os.stat(file)[8] 
      
def atime(file): 
   "Returns the last access time of the file" 
   return os.stat(file)[7] 
            
def ctime(file): 
   "Returns the creation time of the file" 
   return os.stat(file)[9]
   
def nt(file0, file1): 
   """ 
      Returns true if /file0/ is newer than /file1/, returns false
      if either file doesn't exist or file1 is newer or has the same mtime.
   """ 
   if not os.path.exists(file0): 
      return 0 
   elif not os.path.exists(file1): 
      return 0
   else:
      return mtime(file0) > mtime(file1)

def ot(file0, file1): 
   """ 
      Returns true if /file0/ is older than /file1/, returns false
      if either file doesn't exist or file1 is newer or has the same mtime.
   """ 
   if not os.path.exists(file0): 
      return 0 
   elif not os.path.exists(file1): 
      return 0
   else:
      return mtime(file0) < mtime(file1)

                                       
def xl(str, pat):
   """
      Deletes the leading substring that matches the pattern /pat/.
      /pat/ can contain shell wildcards "`*`" and "?".
      
      XXX at this time, pattern matching has a problem with other regular
      expression metacharacters.  They will be used as the would in
      a regular expression.
   """
   pat = string.replace(pat, '.', '\\.')
   pat = string.replace(pat, '*', '.*')
   pat = string.replace(pat, '?', '.')
   m = re.match('^' + pat, str)
   if m:
      return str[m.end():]
   else:
      return str
 

def xt(str, pat):
   """
      Deletes the trailing substring that matches the pattern /pat/.
      /pat/ can contain shell wildcards "`*`" and "?".
      
      XXX at this time, pattern matching has a problem with other regular
      expression metacharacters.  They will be used as the would in
      a regular expression.
   """
   pat = string.replace(pat, '.', '\\.')
   pat = string.replace(pat, '*', '.*')
   pat = string.replace(pat, '?', '.')
   m = re.search(pat + '$', str)
   if m:
      return str[:m.start()]
   else:
      return str
   
def fmttime(fstr, timeval):
   """
      Formats a unix /timeval/ (seconds since the epoch) as a string
      according to the rules defined by the format string /fstr/.
      
      /fstr/ follows the same formatting conventions as strftime.  Time
      zone is always assumed to be the local timezone.
   """
   return time.strftime(fstr, time.localtime(timeval))
