#==============================================================================
#
#  $Id: parse.py 848 2004-10-02 01:08:06Z mike $
#
#  Contains DocParser which parses an NML TextBlock out of a stream.
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
#  $Log: parse.py,v $
#  Revision 1.10  2004/10/02 01:08:06  mike
#  Fixed exception.
#
#  Revision 1.9  2001/11/28 01:41:41  mike
#  Fixes for 2.1
#
#  Revision 1.8  2000/02/13 22:08:52  mike
#  Doc fixes.
#
#  Revision 1.7  1999/05/23 17:55:34  mike
#  Fixed comments and added a warning message if block formatting constructs
#  are discovered in a text formatting entry.
#
#  Revision 1.6  1999/05/10 22:27:52  mike
#  Definition terms can now safely contain embedded double-colons.
#
#  Revision 1.5  1998/12/02 20:48:06  mike
#  Added special syntax for level 1, 2, and 3 headers.
#
#  Revision 1.4  1998/11/03 01:37:35  mike
#  Improved error processing, fixed problem with block terminators.
#
#  Revision 1.3  1998/08/14 15:26:32  mike
#  Added support for parsing "exec" blocks.
#
#  Revision 1.2  1998/06/14 00:40:39  mike
#  Changed name of 'code' type to 'tele'.
#
#  Revision 1.1  1998/06/11 01:27:27  mike
#  Initial revision
#
#
#==============================================================================


import string, re, os
from UserList import UserList
from spug.io.LineReader import LineReader
from types import *
from block import *

special = re.compile(r'(\\.)|_|\*|#|/')

# get the regex object type in 1.5.X or 2.X
if hasattr(re, 'RegexObject'):
   RegexObject = re.RegexObject
else:
   RegexObject = type(special)

class DocParseError(Exception):
   """
      DocParseError is thrown when an error occurs while parsing a document.
      
      XXX should be derived from @StdError.FileParseError
   """
   def __init__(self, txt, src = None, blk = None):
      """
         Constructs a *DocParseError*.
         /txt/::
             exception text
         /src/::
             Source file.  Used to provide error location information.
         /blk/::
             Block that the exception was thrown during the parsing of (used
             to provide a block start location.
      """

      Exception.__init__(self, txt)
      
      if src:
         if isinstance(src, LineReader):
            self.src = src.name, src.lineNumber()
         elif type(src) == TupleType:
            self.src = src
         elif isinstance(src, FileType):
            self.src = src.name, -1
         else:
            self.src = '<unknown>', -1
      else:
         self.src = '<unknown>', -1
      
      if blk:
         self.block = blk
      else:
         self.block = None

   def __str__(self):
      """
         Formats the receiver as a string.  The string form of a block is the
         members of the block seperated by whitespace.  No leading or trailing
         whitespace is appended, all nested blocks are recursively converted to
         strings.
      """
      str = ''
      if self.src:
         str = str + "%s:%d: " % self.src
      
      if self.block:
      
         # we need to include the filename in the string if it is not the
         # same as the filename of the execption's source location.  
         # If it is the same, we can omit it.
         if self.block.src[0] == self.src[0]:
            str = str + \
                  'parsing %s block from line %d ' % \
                  (self.block.type, self.block.src[1])
         else:
            str = str + 'parsing %s block from %s:%d ' % \
                  ((self.block.type,) + self.block.src)

      return str + self[0]


def _DocParser_makeSpecial(types):
   """
      Builds and returns the regular expression that defines all start tag
      character sequences.
   """
   special = ''
   for x in types.values():
      special = special + x.tag + '|'
   
   special = special + r'(\\.)'
   return re.compile(special)

class DocParser:
   """
      A Document parser us used to parse a TextBlock out of a stream.
   """

   types = \
      {
      '/': BlockType('italic', '/', '/'),
      '*': BlockType('bold', r'\*', '*'),
      '_': BlockType('underline', '_', '_'),
      '#': BlockType('tele', '#', '#'),
      '`': BlockType('literal', '`', '`'),
      '\\': AnyBlockType(AnyBlockType.expr),
      }

   wsrx = re.compile(r'\s+')
   definitionrx = re.compile(r'.*[^\\]::\s*$')
   unorderedrx = re.compile(r'\s*-\s+')
   prelitStartrx = re.compile(r'\s*\{\{\s*$')
   prelitEndrx = re.compile(r'\s*\}\}\s*$')
   preStartrx = re.compile(r'\s*\[\[\s*$')
   preEndrx = re.compile(r'\s*\]\]\s*$')
   blockTerminatorrx = re.compile(r'(.*[^\\]::\s*|\s*-\s+.*)$')
   underlinerx = re.compile(r'\s*(={3,}|-{3,}|\'{3,})\s*$')
   definitiontokrx = re.compile(r'.*(::\s*\n)')
   
   special = _DocParser_makeSpecial(types)

   # characters that are terminators that have special meaning in regular
   # expressions.
   rxspecial = (')', ']', '}')

   def __init__(self, src):
      """
         Constructs a DocParser from the given source stream.
      """
      self.buffer = ''
      self.nextLine = None
      self.src = src
      self.tabSize = 8
      self.debugMode = 0
      self.terminatorRxSet = {}

   def _debug(self, loc, blk):
      """
         If in debug mode, prints a loc followed by blk.debug() (blk is expected
         to be a text block).
      """
      if self.debugMode:
         print loc, blk.debug()

   def _warn(self, msg, block):
      """
         Warns the user of things that could be manifestations of errors.
      """
      if isinstance(self.src, LineReader):
         lineInfo = 'line %d: ' % self.src.lineNumber()
      else:
         lineInfo = ''
      
      print 'Warning: %swhile parsing %s block from line %d: %s' % \
         (lineInfo, block.type, block.src[1], msg)

   def _pullLine(self):
      """
         Pulls a line from the source stream, takes it from the /nextLine/
         variable if it is not *None*.
      """
      if self.nextLine:
         line = self.nextLine
         self.nextLine = None
      else:
         line = self.src.readline()
      return line

   def _getCurLine(self):
      """
         Returns the current line of the buffer, returns None if the source
         stream has terminated.
      """
      if not self.buffer:
         self.buffer = self._pullLine()
         
      return self.buffer
   
   def _getNextLine(self):
      """
         Returns the next line of the stream (following the current line).
      """
      if self.nextLine is None:
         self.nextLine = self.src.readline()
      return self.nextLine
   
   def _getNextFullLine(self):
      """
         Like getCurLine(), but keeps reading lines until it encounters
         a line devoid of whitespace or the until end of the file.
      """
      if not self.buffer:
         
         self.buffer = self._pullLine()
         if not self.buffer:
            return None
      
      # match all whitepsace
      ws = self.wsrx.match(self.buffer)
      
      while ws and ws.group() == self.buffer:
         self.buffer = self._pullLine()
         ws = self.wsrx.match(self.buffer)
      
      return self.buffer

   def _harvestBuffer(self, rx = None, replacement = None):
      """
         'Harvests' the entire buffer or up till the regular expression
         if one is supplied.
         
         If no regular expression is given, returns the entire buffer
         and replaces it with an empty string.
         
         If a regular expression is provided, returns up to the beginning
         of the regular expression and truncates up to the end of the regular
         expression.  In this mode of operation, the buffer is never left empty,
         because the parser expects it to contain the remainder of the current
         line.  If /replacement/ is provided, it is appended to the end of the
         value to be returned.
      """
      if rx:
         crop = self.buffer[:rx.start()]
         if replacement:
            crop = crop + replacement
         self.buffer = self.buffer[rx.end():]
         if not self.buffer:
            self.buffer = '\n'
      else:
         crop = self.buffer
         self.buffer = ''
      return crop

   def _setCurLine(self, newCur):
      """
         Sets the current line to /newCur/.  *Deprecated*.  Use 
         @_harvestBuffer()
      """
      self.buffer = newCur

   def _searchForTerminator(self, target, terminator):
      """
         Searches the string /target/ for the first occurrence of the
         string /terminator/.  Returns a match object or *None*.
      """
      rx = self.terminatorRxSet.get(terminator)
      if not rx:
         rx = re.compile(re.escape(terminator))
         self.terminatorRxSet[terminator] = rx
      return rx.search(target)

   def _searchSpecial(self, target, startPos, terminator = None):
      """
         Returns a match object for the next special character sequence or
         terminator (as supplied), whichever comes first.
         
         Returns *None* if neither is available.
      """
   
      # first search for special characters, if there are any obvious
      # reasons not to care about searching for the terminator after this,
      # return it
      specialMatch = self.special.search(target, startPos)
      if not terminator or specialMatch and specialMatch.group() == terminator:
         return specialMatch
      
      # search for instances of the terminator.  If we find one, create a
      # bogus match object for it.
      termMatch = self._searchForTerminator(target, terminator)
      
      # return the first matching expression
      if specialMatch and termMatch:
         if specialMatch.start() < termMatch.start():
            return specialMatch
         else:
            return termMatch
      elif specialMatch:
         return specialMatch
      else:
         return termMatch

   def _parseLiteral(self, txt, term):
      """
         Parses a literal text block.  Literal blocks have no special
         character sequences except for the terminator and escape characters.
      """
      
      lastMatch = 0
      
      # if the terminator is a special character in a regular expression,
      # insulate it with a backslash
      if term in self.rxspecial:
         term = '\\' + term
      
      # create a special regular expression that will match a terminator
      # or escape sequence
      termrx = re.compile(r'(\\.)|' + term)
      
      # assume that we don't have a full line for starters
      fullLine = 0
      
      while 1:
      
         # get the next line and make sure that we got one.
         line = self._getCurLine()
         if not line:
            raise DocParseError('Premature end of file', self.src, txt)

         # search for the first instance of an escape sequence or the
         # terminator
         special = termrx.search(line, lastMatch)
         
         # if an escape sequence was found, remove the backslash
         if special and special.group()[0] == '\\':
            line = line[:special.start()] + line[special.start() + 1:]
            self._setCurLine(line)
            lastMatch = special.end() - 1
         
         # if the terminator was found, we're done
         elif special:
            txt.consume(line[:special.start()])
            
            # truncate up to and including the terminator, if this leaves
            # us with an empty line, tack on a newline.
            line = line[special.end():]
            if not line:
               line = '\n'
            
            self._setCurLine(line)
            return txt
         
         # otherwise, add all of the words in the line to the block
         else:
         
            # warn the user of embedded block terminators
            if fullLine and (self.wsrx.match(line) or 
                             self.blockTerminatorrx.match(line)):
               self._warn("Unexpected block terminator.", txt)
       
            txt.consume(line)
            self._setCurLine('')
            fullLine = 1
            lastMatch = 0

   def _parsePreformattedLiteral(self, txt, lineTerm, term = None):
      """
         Preformatted literals are basically just blocks of text that are
         interred by the block as a single string.  The only characters
         that are special are the terminator and the necessary escape characters
         (`\<terminator> and \\\\`).
         
         For a line terminated preformatted literal, /lineTerm/ must contain
         a regular expression that matches the entire contents of the line,
         excluding trailing and leading whitespace.
      """
   
      if not lineTerm:
      
         # prepare the terminator for use in a regular expression
         if term in self.rxspecial:
            term = '\\' + term
         
         # construct a regular expression for the terminator and two
         # escape sequences
         termrx = re.compile(r'(\\\\)|(\\' + term + ')|(' + term + ')')
      
      # last position that we searched on
      lastPos = 0
      
      while 1:
         line = self._getCurLine()
         
         if not line:
            raise DocParseError("Unexpected end of file.", self.src, txt)
         
         # if this is line terminated, check whether the line matches
         # the line terminator
         if lineTerm and lineTerm.match(line):
            # discard the contents of the buffer
            self._harvestBuffer()
            return txt
            
         elif lineTerm:
         
            # want to move on at this point because the rest of the body
            # of the loop deals with non-line-terminated blocks
            txt.consume(self._harvestBuffer())
            continue

         # check to see if the line has any special stuff in it
         special = termrx.search(line, lastPos)
         if special:
         
            # if this is a terminator, end this now.
            if special.group(3):
               # just stick everything into it and go
               txt.consume(self._harvestBuffer(special))
               return txt
            else:
               txt.consume(self._harvestBuffer(special))
               txt.consume(special.group()[1])
               lastPos = 0
         else:
            # no special characters: just consume it
            txt.consume(self._harvestBuffer())
            lastPos = 0
      

   def _parsePreformatted(self, type, term):
      pass

   def _parseExec(self, txt, term):
      """
         Parses and executes an "exec" block, reading the output of
         the executed command and then parsing it as an NML document.
      """
      tmp = TextBlock(self.src, 'literal', 0)
      self._parseLiteral(tmp, term)
      newSrc = os.popen(str(tmp))
      tmpParser = DocParser(newSrc)
      tmpParser.parseAnything(txt, 0)
      return txt

   def _parseText(self, type, term, tightLeft = 0, indent = 0):
      """
         Parses the next text block.
         /type/::
             the block type.
         /term/::
             the terminator string.  If this value is *None*, the text block
             returns on an empty (all whitepsace) line or a line matching
             one of the kinds of line that starts a new block.
         /tightLeft/::
             If true, the text block binds tightly (with no interspersed
             whitespace) to the text to the left of it.
         /indent/::
             If this is not zero, it represent the level of indentation that the 
             text block must maintain.  If a line is encountered that is
             below that level of indentation, block processing is terminated.
      """

      txt = TextBlock(self.src, type, tightLeft)

      if txt.preformatted and txt.literal:
         return self._parsePreformattedLiteral(txt, None, term)
      elif txt.isExec:
         return self._parseExec(txt, term)
      elif txt.literal:
         return self._parseLiteral(txt, term)

      lastMatch = 0      
      checkSpecialTerm = 1
      
      while 1:
         # get the next line of the buffer
         line = self._getCurLine()
         
         # make sure that there was one
         if not line and term:
            raise DocParseError('Premature end of file', self.src, txt)
         elif not line:
            return txt
         
         # if we are checking indentation, and the next line has
         # lower indentation than the current level, return
         if checkSpecialTerm and indent and indent > self._levelOfIndent(line):
            return txt
         
         # if there's no terminator, we need to check for all of the
         # conditions that constitute a new block - empty line and
         # special format header lines
         if checkSpecialTerm and not term:
            ws = self.wsrx.match(line)
            if ws and ws.group() == line or self.blockTerminatorrx.match(line):
               return txt              
         
         # if the terminator is a regular expression, we need to check to
         # see if the regular expression matches the current line
         elif checkSpecialTerm and isinstance(term, RegexObject):
            if term.match(line):
               return txt

         # if we are not parsing a block formatter and we encounter
         # a block terminator, issue a warning (this probably means that
         # an end terminator is missing)
         if checkSpecialTerm and term and txt.words and \
            (not string.strip(line) or self.blockTerminatorrx.match(line)):
            self._warn("Block terminator encountered.", txt)
         
         # if the terminator is a regular expression search for special 
         # characters excluding the termination sequence.  Otherwise,
         # search for the termination sequence as well
         if isinstance(term, RegexObject):
            match = self._searchSpecial(line, lastMatch)
         else:
            match = self._searchSpecial(line, lastMatch, term)
         
         # first of all, if we matched a backslash expression, remove the
         # backslash from the line and set the lastMatch pointer to the
         # location after the backslash
         if match and match.group()[0] == '\\' and len(match.group()) == 2:
            self._setCurLine(line[:match.start()] + line[match.end() - 1:])
            lastMatch = match.end() - 1
            
            # since we don't have a complete line, turn off checking for
            # special termination conditions
            checkSpecialTerm = 0
            
         elif match:
         
            matchVal = match.group()

            # add the words before the special character to the document
            txt.consume(self._harvestBuffer(match))
            
            # reset the lastMatch pointer (since we`are done with it)
            lastMatch = 0
         
            # if the special character is the terminating character for
            # the current text block, return now
            if matchVal == term:          
               return txt

            # get the child information
            childType = self.types[matchVal[0]]

            # parse a new text block ending with the matching terminator
            childBlock = self._parseText(childType.getName(matchVal), 
                                         childType.getTerminator(matchVal)
                                         )
            
            self._debug("Child: ", childBlock)

            # if the last character before where we start is a whitespace
            # character, mark the fact that we need whitespace before the
            # textblock.
            loc = match.start() - 1
            if loc >= 0 and line[loc] not in string.whitespace:
               childBlock.tightLeft = 1
            else:
               childBlock.tightLeft = 0

            # add the new child to the list of children for the block
            txt.addChild(childBlock)
            
            # if there is whitepsace immediately after the child block, the
            # child block binds tightly to the right
            line = self._getCurLine()
            if line and line[0] not in string.whitespace:
               childBlock.tightRight = 1
            
            # if we care about indentation or structure, we need to indicate
            # that we do not currently have a complete line so that
            # checking for structural termination conditions is turned off
            checkSpecialTerm = 0
         
         else:
            # add the entire line to the text block, reset everything to
            # indicate that we`ve consumed it.
            txt.consume(self._harvestBuffer())
            lastMatch = 0
            
            # turn on checking for special termination conditions (since we've
            # got a complete line)
            checkSpecialTerm = 1

   def _levelOfIndent(self, line):
      """
         Computes the level of indentation for the given /line/.
      """
   
      if not line:
         return 0
   
      # convert tabs to spaces
      str = string.expandtabs(line, self.tabSize)
      
      # build a match for the leading whitespace
      ws = self.wsrx.match(str)
      if not ws:
         return 0
      else:
         return ws.end()

   def _parseDefinitionList(self, indent):
      """
         Parses a definition list block.
      """

      # create a new definition list
      dl = TextBlock(self.src, 'definitionList')

      # trick to get the string that the line actually terminates with
      line = self._getNextFullLine()
      term = self.definitiontokrx.match(line).group(1)

      # get the item being defined, which should be a text block
      item = self._parseText('text', term)
      
      self._debug("Defined: ", item)
      
      while 1:
         # get the next line, if the indentation is less than the current leve
         line = self._getNextFullLine()
         lineIndent = self._levelOfIndent(line)
         if lineIndent < indent:
            raise DocParseError("Greater indentation expected following "
                                 "definition term.",
                                self.src,
                                item
                                )
         
         definition = TextBlock(self.src, 'doc')
         self.parseAnything(definition, lineIndent)
         self._debug("Definition: ", definition)
         
         # create a new definition item block containing the item and its
         # definition
         block = TextBlock(self.src, 'definitionItem')
         block.addChild(item)
         block.addChild(definition)
         
         # add the item to the definition list
         dl.addChild(block)
         
         # get the next line
         line = self._getNextFullLine()
         lineIndent = self._levelOfIndent(line)
         
         # if the next line is not a definition, we're done.
         if not line or lineIndent < indent or \
               not self.definitionrx.match(line):
            return dl

         # get the line terminator
         term = self.definitiontokrx.match(line).group(1)
         
         # reset item to the next definition.
         item = self._parseText('text', term)
         
         self._debug("Defined: ", item)

   def _parseUnorderedList(self, indent):
      """
         Parses an unordered list.
      """
   
      # quick little procedure to replace the hyphen
      def replaceHyphen(self, line):
         pos = string.find(line, '-')
         line = line[:pos] + ' ' + line[pos + 1:]
         self._setCurLine(line)
         return line
   
      ol = TextBlock(self.src, 'unorderedList')
   
      # replace the leading hyphen in the current line with a space
      line = self._getCurLine()
      line = replaceHyphen(self, line)
      
      # get the current indentation
      lineIndent = self._levelOfIndent(line)
      
      while 1:
         # create a new doc block for the item
         item = TextBlock(self.src, 'doc')
         self.parseAnything(item, lineIndent)
         
         # add the new item to the list
         ol.addChild(item)
         
         # get the next line with stuff in it
         line = self._getNextFullLine()
         if not line:
            return ol
         
         # if its indentation is less than that of the unordered list itself,
         # quit now
         lineIndent = self._levelOfIndent(line)
         if lineIndent < indent:
            return ol

         # if it is something other than an unordered list element, quit now
         if not self.unorderedrx.match(line):
            return ol

         # go through the replacement game again
         line = replaceHyphen(self, line)
         
         # get the current indentation
         lineIndent = self._levelOfIndent(line)    

   def _parsePara(self, indent):
      """
         Create, parse and return the next paragraph.
      """
      tmp = self._parseText('para', None, indent = indent)
      self._debug("Para: ", tmp)
      return tmp

   def parseAnything(self, block, indent):
      """
         Not entirely sure where this fits in: parses meta-level structures,
         recognizes special sequences for unordered lists and definition lists
         and paragraphs.
      """
   
      while 1:
         line = self._getNextFullLine()
         
         # if this is the end of the file, we're done
         if not line:
            return
         
         # if this line is indented less than the current level of indent,
         # return.
         if self._levelOfIndent(line) < indent:
            return
         
         # if this is a definition, parse a definition list
         if self.definitionrx.match(line):
            tmp = self._parseDefinitionList(indent)
            self._debug("Definition list: ", tmp)
            block.addChild(tmp)
            
         # if this is an unordered list item, parse an unordered list
         elif self.unorderedrx.match(line):
            tmp = self._parseUnorderedList(indent)
            self._debug('Unordered list: ', tmp)
            block.addChild(tmp)
         
         # if this is a preformatted literal block start, parse one
         elif self.prelitStartrx.match(line):
            self._harvestBuffer()
            tmp = TextBlock(self.src, 'prelit')
            self._parsePreformattedLiteral(tmp, self.prelitEndrx)
            self._debug('Preformatted literal: ', tmp)
            block.addChild(tmp)
         
         # if this is preformatted, parse a preformatted block
         elif self.preStartrx.match(line):
            self._harvestBuffer()
            tmp = self._parseText('pre', self.preEndrx, 
                                  self._levelOfIndent(line)
                                  )
            self._harvestBuffer()
            self._debug('preformatted: ', tmp)
            block.addChild(tmp)

         # if this is a line of text followed by an "underline line",
         # treat it as a header
         elif line and self.underlinerx.match(self._getNextLine()):
            underline = string.strip(self._getNextLine())[0]
            if underline == '=':
               header = '1'
            elif underline == '-':
               header = '2'
            elif underline == "'":
               header = '3'
            tmp  = self._parseText(header, self.underlinerx, 
                                   self._levelOfIndent(line)
                                   )                                   
            self._harvestBuffer()
            self._debug('header: ', tmp)
            block.addChild(tmp)
         
         # if this is just an ordinary line, parse it as a paragraph
         elif line:
            block.addChild(self._parsePara(indent))

   def parseDoc(self):
      """
         Parse (and return) the entire document from the stream.
      """
      doc = TextBlock(self.src, 'doc') 
      self.parseAnything(doc, 0)
      return doc

_specialChars = string.join(DocParser.types.keys(), '|')
_specialChars = string.replace(_specialChars, '\\', '\\\\')
_specialChars = string.replace(_specialChars, '*', '\\*')

_specialChars = re.compile(_specialChars)

def escapeString(str):
   """
      This function is used to take a string that contains literal text
      and escape all special NML characters in it.  Block level formatting
      sequences are not considered.
   """
   return _specialChars.sub(lambda match: '\\' + match.group(), str)
