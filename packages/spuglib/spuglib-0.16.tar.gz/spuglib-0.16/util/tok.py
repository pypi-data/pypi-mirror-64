#!/usr/local/bin/python
#==============================================================================
#
#  $Id: tok.py 842 2004-05-04 01:54:45Z mike $
#
"""
   Simple tokenizer framework.
   
   At this time, all of the functionality of the @CTokenizer is
   implemented in @Tokenizer.  Eventually, the *CTokenizer* personality
   should be broken out into the correct class.
   
   Synopsis:
   
   {{

      from spug.util.tok import CTokenizer
      
      # create a new tokenizer to parse standard input
      toker = CTokenizer(sys.stdin)
      
      while 1:
      
         # get the next token
         tok = toker.nextToken()
         
         # check for end-of-stream
         if tok.isType(Token.end):
            break
         
         # print out the token type and the value
         print toker.tokTypes[tok.type - 1].name + ': ' + tok.val
   }}
   
   Run "#python tok.py#" to see the action of the above code.
      
""" #"
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
#  $Log: tok.py,v $
#  Revision 1.4  2004/05/04 01:54:45  mike
#  Misc small fixes, added a TokenStream class to avoid having to do that with
#  every new client.
#
#  Revision 1.3  2000/02/13 21:58:52  mike
#  Doc fixes.
#
#  Revision 1.2  2000/02/13 00:09:08  mike
#  Converted comments to docstrings.
#
#  Revision 1.1  1998/10/22 23:46:26  mike
#  Initial revision
#
#
#==============================================================================

import re

class Token:
   """
      Tokens represent pieces of text.  Each token has:
      /val/:: 
         source text of the token.  Its "value".
      /type/:: 
         a numeric value indicating the tokens type
      /srcName/:: 
         Name of the source stream that it came from
      /lineNum/:: 
         Line number from which it came.
         
      #Token.end# is a class variable set to zero. It is used to indicate
      that the end of the stream has been read.  *Do not use 0 as a token 
      Id.*
   """

   # special token for end of stream
   end = 0

   def __init__(self, type, val, srcInfo):
      """
         Constructor for Token.  Type is one of the types listed above, val is
         the value of the token (its text), srcName is the name of the source
         file that the token was tokenized from, and /lineNum/ is the line number
         in the source file.
         /srcInfo/ is a tuple indicating the source file name and the line
         number.
      """
      
      self.type = type
      self.val = val
      self.srcName = srcInfo[0]
      self.lineNum = srcInfo[1]

   def isType(self, type):
      """
         Returns true if the token is of the indicated type.
      """
      return self.type == type

   def equals(self, type, val):
      """
         Returns true if the token is of the indicated type and has the
         indicated value.
      """
      return self.type == type and self.val == val
   
class TokenInfo:
   """
      TokenInfo holds information about token types.  Each has a 
      /name/, a /regex/ (regular expression describing how the token is
      represented) and an /id/.
   """

   def __init__(self, name, regex, create, continued):
      """
         Make one.  Public variables:
         /name/::
            the name of the token type
         /regex/::
            the regular expression that describes the tokens source form
         /create/::
             a function that should expect a token source string
         /continued/::
            an optional regular expression.  If it is present, it
	       indicates that the token may be continued over multiple lines
	       (if /regex/ matches to the end of the current line) and it
	       represents the kind of expression which will terminate the
	       multi line token beginning with /regex/.  All lines between
	       the line that begins the token and the portion of a line
	       which ends the token are considered to be part of the token.
      """

      self.name = name
      self.regex = regex
      self.create = create
      self.continued = continued

class TokenizerError(Exception):
   "A Tokenizer error"
   
   def __init__(self, toker, text):

      Exception.__init__(self, 
                         toker.src.name + ":" + `toker.lineNum` + ": " + text
                         )    
      self.toker = toker

class Tokenizer:
   """
      A Tokenizer is used to extract tokens from a source stream.  Tokens
      are of the form normally accepted by C-like languages.

      XXX This class really needs to become generic, with its C personality
      moved to CTokenizer
   """

   # Descriptions of each of the token types.  In a more generalized
   # model, these will exist in a subclass, with Tokenizer providing only
   # the basic functionality required to process the token types.

   id = 1
   int = 2
   str = 3
   chr = 4
   cmt = 5
   ws = 6
   sym = 7
   
   identifier = \
      TokenInfo("identifier", 
                re.compile(r'[A-Za-z_][A-Za-z_0-9]*'),
                lambda src, loc: Token(Tokenizer.id, src, loc),
                None
                )
      
   integer = \
      TokenInfo("integer", 
                re.compile(r'(0x[0-9a-fA-F]+)|([0-9]+)'),
                lambda src, loc: Token(Tokenizer.int, src, loc),
                None
                )
      
   string = \
      TokenInfo("string", 
                re.compile(r'"([^\\]|(\\.))*?"'),
                lambda src, loc: Token(Tokenizer.str, src, loc),
                None
                )
   
   character = \
      TokenInfo("character",
                re.compile(r" ' [^\\] | (\\.) ' ", re.X),
                lambda src, loc: Token(Tokenizer.chr, src, loc),
                None
                )
   
   # comments can consist of either // to end of line or /* */
   comment = \
      TokenInfo("comment", 
                re.compile(r' ( /\* .*?  \*/ ) |'
                            r'( // .* $ )', 
                           re.X
                           ),
                lambda src, loc: Token(Tokenizer.cmt, src, loc),
                None
                )

   # long comments are simply comments that extend past the end of the
   # line.
   longComment = \
      TokenInfo("longComment",
                re.compile(r' /\* .* \n$ ', re.X),
                lambda src, loc: Token(Tokenizer.cmt, src, loc),
                re.compile(r' .* \*/ ', re.X)
                )         
   
   whitespace = \
      TokenInfo("whitespace", 
                re.compile(r'[ \n\r\t]+'),
                lambda src, loc: Token(Tokenizer.ws, src, loc),
                None
                )

   symbol = \
      TokenInfo("symbol",
                re.compile(r'[~!#%^&\*\(\)\-\+\=\|\}\{\]\[:;<>\?,\./\\]'),
                lambda src, loc: Token(Tokenizer.sym, src, loc),
                None
                )

   tokTypes = [ identifier, integer, string, comment, longComment, whitespace,
                symbol
                ]
   
   def __init__(self, src):
      """
         Constructor.  Creates a new Tokenizer given a source file and
         (optionally) a set of flags.
      """

      self.src = src
      self.lineNum = 0
      self.preparsed = [ ]
      self.buffer = ""
   
   def nextPreparsed(self):
      """
         Return the next token in the preparsed list (the list of tokens that
         has already been parsed and were put back).
      """
      
      next = self.preparsed[0]
      del self.preparsed[0]
      return next
   
   def fillBuffer(self):
      """
         Make sure that the buffer has data in it.
      """
      
      if not self.buffer:
         self.buffer = self.src.readline()
         self.lineNum = self.lineNum + 1

   def breakOff(self, toksrc):
      """
         "breaks off" the regular expression match specified by toksrc from the
         buffer, and returns it.
      """
   
      self.buffer = self.buffer[toksrc.end():]
      return toksrc.group()

   def __takeIt(self, tokType, toksrc):
      """
         Takes the next token off of the front of the buffer and returns it.
	 If the token type continues onto the next line, continue it.
      """
      
      # get the stuff
      stuff = self.breakOff(toksrc)
      
      # if the token continues onto the next line and the regular
      # expression matches rest of the current line, continue refilling
      # the buffer until we obtain an expression that matches the
      # "continued" expression.
      if tokType.continued and not len(self.buffer):
         
#         print "continued is regex: ",  \
#            isinstance(tokType.continued, re.RegexObject)
         
         self.fillBuffer()
         
         # keep getting until we either find the terminator or run out
         # of source code
         while self.buffer:
         
            # quit if we find the end
            toksrc = tokType.continued.match(self.buffer)
            if toksrc:
               return stuff + self.breakOff(toksrc)
            
            # if not, take whatcha got and gimme more
            stuff = stuff + self.buffer
            self.buffer = None
            self.fillBuffer()
            
         else:
            raise TokenizerError(self, tokType.name + " never terminated.")
         
         return stuff
      else:
         return stuff

   def parseNextToken(self):
      """
         Parses the next token directly off of the stream.  Clients should
         generally avoid using this.  Use nextToken() instead, since that will
         use the preparsed queue if tokens have been put back.
      """
      
      # make sure that the buffer has data
      self.fillBuffer();
      
      # if the buffer is still empty, this is the end of the stream
      if not self.buffer:
         return Token(Token.end, '', (self.src.name, self.lineNum))
      
      # check each of the regular expressions against the contents of the
      # buffer
      for x in self.tokTypes:
      
         # see if this expression matches
         toksrc = x.regex.match(self.buffer) 
         if toksrc:
            
            # break the token off of the front of the stream
            toksrc = self.__takeIt(x, toksrc)
            
            # construct a new instance of x
            return x.create(toksrc, (self.src.name, self.lineNum))
            
      else:
         raise TokenizerError(self, "Unknown token.");
   
   def nextToken(self):
      """
         Returns the next token, either from the preparsed cache, or from the
         stream.
      """
      
      if self.preparsed:
         return self.nextPreparsed()
      else:
         return self.parseNextToken()

   def putBack(self, tok):
      """
         Puts the given token back on the list.  Puts it first on the list,
         so immediately after calling, /tok/ will be the next token
         return from @nextToken().
      """
      self.preparsed.insert(0, tok) 

class CTokenizer(Tokenizer):
   "Tokenizer for C-like languages."
   pass

class TokenStream:
   """
      This class can be used as a wrapper for any object that provides
      the file readline() method - it delegates that and also provides
      a "name" variable, required by the tokenizer.
   """
   
   def __init__(self, src, name):
      self.src = src
      self.name = name
   
   def readline(self):
      return self.src.readline()

if __name__ == '__main__':
   import sys  
   toker = Tokenizer(sys.stdin)
   
   while 1:
   
      tok = toker.nextToken()
      if tok.isType(Token.end):
         break
      
      print toker.tokTypes[tok.type - 1].name + ': ' + tok.val
