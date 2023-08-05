#==============================================================================
#
#  $Id: ComLine.py 766 2001-11-27 01:38:57Z mike $
#
"""
   Command line parsing utility.
   
   Synopsis:
   
   {{
      from spug.util.ComLine import helpOption, ArgType, ComLine
      
      # define the command line options
      clopts = \\
         [
         # standard help option (-h or --help)
         helpOption(),
         
         # option -f, --file, or --file-to-use which accepts a single
         # parameter
         ArgType('file', 'f', ['file', 'file-to-use'], parm = 1, 
                 parmHelp = 'file-name',
                 help = 'Specifies the file to be used.'
                 ),
         
         # a verbosity option
         ArgType('verbose', 'v', ['verbose'], help = 'be verbose'),
         ]
      
      # we define the help prefix, options will be automatically printed
      # if help is requested.
      cl = ComLine(clopts, helpPrefix = '''
      widget - defines various widgets
      Usage:
         widget [options] widget-name ...
      ''')
      
      # "others" gives us the list of non-option arguments.  Check to 
      # see if it is empty, show usage blurb if it is.
      if not cl.others():
         cl.help()
      
      # get file option (None if none was supplied).
      file = cl['file']
      
      # get verbosity (1 or None)
      verbose = cl['verbose']
   }}
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
#  $Log: ComLine.py,v $
#  Revision 1.9  2001/11/27 01:38:57  mike
#  Fixes for Python 2.1
#
#  Revision 1.8  2000/02/13 21:27:52  mike
#  Doc fixes, converted CRLF's.
#
#  Revision 1.7  1999/03/19 02:12:47  mike
#  Added stuff to make the help option really easy.
#
#  Revision 1.6  1998/12/03 12:58:02  mike
#  Fixes to option NML help.
#
#  Revision 1.5  1998/12/02 21:23:06  mike
#  Expanded documentation features.
#
#  Revision 1.4  1998/10/15 17:57:28  mike
#  Forgot to import sys on last change.
#
#  Revision 1.3  1998/10/15 17:51:50  mike
#  Fixed the help command (needed to exit if force flag set).
#
#  Revision 1.2  1998/10/15 14:09:12  mike
#  Added the "help" function to the module.  This allows programs that only
#  use the -h command line option to do so very easily.s
#
#  Revision 1.1  1998/08/04 20:46:36  mike
#  Initial revision
#
#
#==============================================================================

from types import IntType, StringType

_escapeString = None

class Error(Exception):
   pass

class UnknownOptionError(Error):
   """
      Raised when an unknown command line option is encountered.
   """
   pass

class DuplicateOptionError(Error):
   """
      Raised when a non-multiple command line option is used more than once.
   """
   pass

class UsageError(Error):
   """
      Raised when something is wrong with the option's argument.
   """
   pass

class ArgType:
   """
      An instance of *ArgType* defines that characteristics of a single command
      line option.  All parameters to @__init__() are available as public
      variables.
   """
   
   def __init__(self, name, shortOptions, longOptions = [], parm = 0,
                valid = None, mult = 0, help = "", helpCmd = 0,
                parmHelp = 'parm'
                ):
      """
         Constructs ArgType.
         Parameters:
         /name/::
             Name of the option.
         /shortOptions/::
             A string containing the single character command line options.
         /longOptions/::
             A list of strings containing the long (full word) command line
             options.
         /parm/::
             If this is true, the argument accepts a parameter.
         /valid/::
             If used, should be passed a function which accepts the value of the
             argument and returns true if the argument is valid (falls within
             the constraints defined by the parameter).  Only appropriate in
             conjunction with /parm/
         /mult/::
             If this is true, the argument may be used more than once on the
             command line and its value will be returned as a list of all of
             the values that have been defined for it.
         /help/::
             If set, this contains a help message that will be printed out along
             with the option when help is displayed using @ComLine.help()
         /helpCmd/::
             If this is true, the use of this option automatically triggers the
             @ComLine.help() function.
         /parmHelp/::
             This is the string that will be printed in the option's help message
             in to describe the parameter for the option.  For example, if a value
             of "file-name" is used for a "-c" option, the option help will look
             like this:
         
             {{
                -c <file-name>
                   Does something with the given file.
             }}
      """
      self.name = name
      self.shortOptions = shortOptions
      self.longOptions = longOptions
      self.parm = parm
      self.valid = valid
      self.mult = mult
      self.help = help
      self.helpCmd = helpCmd
      self.parmHelp = parmHelp

class ComLine:
   """
      Instances of this class parse and manage command line options.
      The public variable /args/ is an array containing the unprocessed 
      command line arguments (those that did not begin with '-').
   """
   
   def _addArgType(self, v):
      self.types[v.name] = v
      
      # add the arg type to each of the single character option names
      # associated with it
      for opt in v.shortOptions:
         if self.shortOptions.has_key(opt):
            raise Error("Short option " + opt + " is used by both " +
                        v.name + " and " + self.shortOptions[opt].name
                        )
         self.shortOptions[opt] = v
   
      # now add it to each of the long option names.
      for opt in v.longOptions:
         if self.longOptions.has_key(opt):
            raise Error("Long option " + opt + " is used by both " +
                        v.name + " and " + self.longOptions[opt].name
                        )
         self.longOptions[opt] = v
      
      # now set it to None in the "vals" dictionary
      self.vals[v.name] = None
   
   def _processOption(self, typeInfo, args):
      optName = typeInfo.name
      
      if typeInfo.helpCmd:
         self.help()
         import sys
         sys.exit(0)

      if not typeInfo.mult and self.vals[optName] is not None:
         raise DuplicateOptionError(optName)

      # if this has a parameter, get the parameter, raising an error if
      # it wasn't found.
      
      if typeInfo.parm and not args:
         raise UsageError('"%s" option requires a parameter' % optName)
         
      elif typeInfo.parm:
      
         parm = args[0]
         del args[0]
      
         # if there is a validation function, use it
         if typeInfo.valid:
            if not typeInfo.valid(parm):
               raise InvalidParmError(optName, parm)
      
         # if this is a multiple option, add the argument info to the list
         # of values for the option, otherwise set the option to the value.
         if typeInfo.mult:
            if not self.vals[optName]:
               self.vals[optName] = [parm]
            else:
               self.vals[optName].append(parm)
         else:
            self.vals[optName] = parm

         self.args.append((parm, typeInfo))

         return 1
      
      else:
         
         self.args.append((1, typeInfo))
         self.vals[optName] = 1
         return 0
   
   def _processExtended(self, args):
      arg = args[0][2:]
      del args[0]
      try:
         typeInfo = self.longOptions[arg]
      except KeyError, ex:
         raise UnknownOptionError(ex)
      self._processOption(typeInfo, args)
   
   def _processShort(self, args):
      arg = args[0][1:]
      while arg:
      
         # break off the first character of the current argument
         curOpt = arg[0]
         args[0] = arg = arg[1:]
         
         # if it was the last character of the argument, remove the argument
         if arg == '':
            del args[0]
            arg = None
         
         try:
            typeInfo = self.shortOptions[curOpt]
         except KeyError, ex:
            raise UnknownOptionError(ex)
         if self._processOption(typeInfo, args):
            arg = None

      # if the first argument was consumed but not deleted, remove it now
      if arg == '':
         del args[0]

   def __init__(self, arginfo, argv = None, helpPrefix = None):
      """
         Constructs a ComLine object from /arginfo/ (a list of @ArgType instances)
         and /argv/ (list of command line arguments).  If argv is not supplied,
         sys.argv is used.
      """
   
      if not argv:
         import sys
         argv = sys.argv

      self.helpPrefix = helpPrefix

      self.argTypes = arginfo
      self.types = {}
      self.shortOptions = {}
      self.longOptions = {}
      
      self.args = []
      self.vals = {}
      
      for v in arginfo:
         self._addArgType(v)
      
      self.programName = argv[0]
      
      # make a copy of the rest of the args
      args = argv[1:]
      while args:
         arg = args[0]
      
         if arg[0:2] == '--':
            self._processExtended(args)
         elif arg[0] == '-':
            self._processShort(args)
         else:
            self.args.append((arg, None))
            del args[0]       

   def help(self):
      """
         Prints out a nicely formatted help message containing a description of
         each of the options.  If /helpPrefix/ was supplied during construction,
         prints this first.  Otherwise, just prints the program name first.
      """
      import sys
      if self.helpPrefix is not None:
         print self.helpPrefix
      else:
         print self.programName + ':'
      print "Options:"
      for cur in self.argTypes:
         for opt in cur.shortOptions:
            sys.stdout.write('-' + opt + ' ')
            if cur.parm:
               sys.stdout.write('<%s> ' % cur.parmHelp)
         for opt in cur.longOptions:
            sys.stdout.write('--' + opt + ' ')
            if cur.parm:
               sys.stdout.write('<%s> ' % cur.parmHelp)
         if cur.help:
            sys.stdout.write('\n   ')
            sys.stdout.write(cur.help)
            if cur.help[-1] != '\n':
               sys.stdout.write('\n')
   
   def optionsHelpToNML(self, cleanHelpText = 0):
      """
         Returns a string representing the options help formatted in NML.
         
         If /cleanHelpText/ is true, escapes the special NML characters 
         in the help text.
      """
      global _escapeString
      
      # this allows us to defer the import of escape string so that this
      # module is not neccessarily dependent on NML
      if cleanHelpText and _escapeString is None:
         from spug.nml.parse import escapeString
         _escapeString = escapeString
      
      nmlStr = ''
      for cur in self.argTypes:
         first = 1
         for opt in cur.shortOptions:
            if first:
               nmlStr = nmlStr + '*-' + opt + '*'
               first = 0
            else:
               nmlStr = nmlStr + ', *-' + opt + '*'
            if cur.parm:
               nmlStr = nmlStr + ' /%s/' % cur.parmHelp
         for opt in cur.longOptions:
            if first:
               nmlStr = nmlStr + '*--' + opt + '*'
               first = 0
            else:
               nmlStr = nmlStr + ', *--' + opt + '*'
            if cur.parm:
               nmlStr = nmlStr + ' /%s/' % cur.parmHelp
         if cur.help:
            if cleanHelpText:
               nmlStr = nmlStr + '::\n   ' + _escapeString(cur.help)
            else:
               nmlStr = nmlStr + '::\n   ' + cur.help
            if cur.help[-1] != '\n':
               nmlStr = nmlStr + '\n'
      return nmlStr

   def others(self):
      """
         Constructs and returns a list of all non-option parameters.
      """
      otherList = []
      for val, type in self.args:
         if type is None:
            otherList.append(val)
      return otherList
   
   def __getitem__(self, key):
      """
         Attempts to make the command line accessible as both an array and a
         dictionary.  If /key/ is an integer, returns a tuple containing either
         the indexed argument and *None* (if it is a non-option argument) or
         the value of the option and the @ArgType object for the option (if it
         is a command line option).
         
         If /key/ is a string, it should be the name of a command line option and
         the value of that option will be returned.  This will return *None* if
         the option is a legitimate option but was not specified on the command
         line.
         
         If the value specified by the key does not exist, raises either an
         *IndexError* or a *KeyError* depending on the mode of addressing used.
      """
      if type(key) is IntType:
         return self.args[key]
      elif type(key) is StringType:
         return self.vals[key]

def helpOption():
   """
      Clients may use this function to easily create the officially sanctioned
      help function.
   """
   return ArgType("help", 'h', ['help'], helpCmd = 1, 
                   help = "shows this help message."
                   )

def help(helpText, force = 0):
   """
      Import this function when you just need to provide the "help" command
      line option.  For example:
      
      {{
          from spug.util.ComLine import help
          help('''
          foo - program to do foo
          Options:
          '''
          )
      }}
      
      If you pass in a true value for /force/, it will force the help message
      to be printed no matter what the command line options are.
   """
   opts = [ helpOption() ]
   cl = ComLine(opts, helpPrefix = helpText)
   if force:
      import sys
      cl.help()
      sys.exit()

if __name__ == '__main__':

   import sys

   def validator(arg):
      try:
         int(arg)
      except ValueError:
         return 0
      return 1
   
   opts = \
      [
      ArgType('typea', 'aA', ['aaa', 'AAA'], help = 'simple option'),
      ArgType('typeb', 'bB', ['bbb', 'BBB'], 1, 
              help = 'option with parameter'
              ),
      ArgType('typec', 'cC', ['ccc', 'CCC'], 1, validator,
              help = 'option with integer parameter'
              ),
      ArgType('typed', 'dD', ['ddd', 'DDD'], 1, None, 1,
              help = 'multi-option with parameter'
              ),
      ArgType('nml-doc', 'n', ['nml-doc'], parm = 1, help = "nml docs",
              parmHelp = 'bogus'),
      ArgType('help', 'h?', ['help'], help = 'this help message', helpCmd = 1),
      ]
   
   cl = ComLine(opts, helpPrefix = "Program to test command line options\n")
   print "args:", cl.args
   print "vals:"
   for k, v in cl.vals.items():
      print k, v
   
   print "arg[0] =", cl[0]
   print "arg['typeb'] =", cl['typeb']
   print "other: ", cl.others()
   if cl['nml-doc']:
      print cl.optionsHelpToNML()


