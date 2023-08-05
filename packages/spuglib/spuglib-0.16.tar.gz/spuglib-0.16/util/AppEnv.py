#==============================================================================
#
#  $Id: AppEnv.py 552 2000-02-13 00:16:33Z mike $
#
"""
   Application environment object: provides a uniform method of storing
   application parameters.
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
#  $Log: AppEnv.py,v $
#  Revision 1.4  2000/02/13 00:16:33  mike
#  Converted comments to docstrings.
#
#  Revision 1.3  1998/11/06 21:38:13  mike
#  Added a hack which may or may not fix the problem with saving options files
#  in windows.
#
#  Revision 1.2  1998/10/22 23:39:01  mike
#  Removed references to the application path (which didn't work on windows).
#
#  Revision 1.1  1998/08/01 18:15:42  mike
#  Initial revision
#
#
#==============================================================================

import imp, os, sys, string, re

class AppEnv:
   """
      Application environment class.  This holds information about the
      application environment loaded from an application preference file
      of the name ./application-name/ which is searched for in the following
      locations:
      
      -   The users home directory (as defined by the *HOME* environment
          variable).
      -   Each of the non-empty directories in the sys.path variable (doesn't
          look in the current directory).
      
      This class implements the dictionary interface for variable access.
   """
   
   identRx = re.compile('[A-Za-z_][A-Za-z_0-9]*')
   
   def _findEnvFile(self):
      fname = os.sep + self.fileName
      try:
         home = os.environ['HOME']
      except:
         home = None
      globalDict = {}
      self.vars = {}
      if home and os.path.exists(home + fname):
         self.varFile = home + fname
      else:
         for cur in sys.path:
            if cur and os.path.exists(cur + fname):
               self.varFile = cur + fname
               break
         else:
            self.varFile = None
            return
      execfile(self.varFile, globalDict, self.vars)
   
   def __init__(self, appName):
      """
         Constructs an AppEnv instance.  /appName/ should be a string application
         name, /mainModule/ should be the location of the main module.
      """
      self.appName = appName
      if os.name == 'nt' or os.name == 'dos':
         self.fileName = self.appName
      else:
         self.fileName = '.' + self.appName
      self._findEnvFile()

   def writeTo(self, file):
      """
         Writes the file representation of the environment to the given /file/.
      """
      for key, val in self.vars.items():
         file.write(key + ' = ' + `val` + '\n')

   def save(self):
      """
         Saves the environment file.  If the file was not already loaded or
         specified through the @setPath() method, the file will be written
         to the home directory or (if it does not exist) the first non-empty
         directory in sys.path.
      """
      if not self.varFile:
         path = None
         try:
            path = os.environ['HOME']
         except:
            for cur in sys.path:
               if cur and os.path.exists(cur) and os.path.isdir(cur):
                  path = cur
                  break
         if not path:
            raise AppEnvError("Couldn't find a place to save to.")
         self.varFile = path + os.sep + self.fileName
      f = open(self.varFile, 'w')
      f.write('# Application defaults for ' + self.appName + 
               '.  DO NOT EDIT\n\n'
              )
      self.writeTo(f)

   def setPath(self, path):
      """
         Sets the variable file path.  The variable file will be constructed from
         /path/ and the application name.
      """
      self.varFile = path + os.sep + self.fileName

   def loaded(self):
      """
         Returns true (1) if the variable file was loaded, false (0) if not.
      """
      return self.varFile and 1 or 0

   def get(self, key, default):
      """
         Gets the application environment variable identified by /key/.  If
         this value is not currently among the application variables, returns
         /default/.
      """   
      return self.vars.get(key, default)
   
   def getStrict(self, key):
      """

         Gets the application environment variable identified by /key/.  If
	 this variable is not defined, or is defined as an empty or all
	 whitespace string, raises a KeyError.

         If the value is defined, all whitespace will be stripped from the end
         end beginning of it.
      """
      val = string.strip(self.vars[key])
      if not val:
         raise KeyError(key)
      return val
   
   def has_key(self, key):
      return self.vars.has_key(key)

   def __getitem__(self, item):
      return self.vars[item]
   
   def __setitem__(self, item, val):
      match = self.identRx.match(item)
      if not match or match.group() != item:
         raise ValueError('"' + item + '" is not a legal identifier.')
      if repr(val)[0] == '<':
         raise ValueError('"' + repr(val) + 
                           '" can not be represented in an environment file.'
                          )
      self.vars[item] = val
   