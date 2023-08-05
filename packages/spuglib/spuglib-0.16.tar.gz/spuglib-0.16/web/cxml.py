#==============================================================================
#
#  $Id: cxml.py 917 2005-12-14 21:36:24Z mike $
#
"""
   Module for converting CXML documents to XML.
"""
#
#  Copyright (C) 2002 Michael A. Muller
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

import re, string
from types import IntType, StringType
import xmlo

class Token:
   
   def __init__(self, id, val, srcName, lineNum):
      self.id = id
      self.val = val
      self.srcName = srcName
      self.lineNum = lineNum

   def __str__(self):
      return self.val

class Toker:

   # states
   ST_CDATA = 0
   ST_MARKUP = 1
   ST_PI = 2
   ST_COMMENT = 3
   ST_EXPCDATA = 4
   ST_ENTITY = 5

   # tokens
   END = -1   
   CDATA = 0
   TAG = 1
   LPAREN = 2
   RPAREN = 3
   EQUALS = 4
   LCURL = 5
   RCURL = 6
   DQSTRING = 7
   SQSTRING = 8
   WS = 9
   SEMICOLON = 10
   NAME = 11
   COMMA = 12
   PI = 13
   ENDPI = 14
   COMMENT = 15
   ENDCOMMENT = 16
   EXPCDATA = 17
   ENDCDATA = 18
   ENTITYREF = 19
   __cdataToks = \
      [
      (CDATA, r'([^\\\{\}]|\\\\|\\\{|\\\})+', ST_CDATA),
      (TAG, r'\\[^\s\(\{;\?\!\[&]+', ST_MARKUP),
      (RCURL, r'\}', ST_CDATA),
      (PI, r'\\\?', ST_PI),
      (COMMENT, r'\\!--', ST_COMMENT),
      (EXPCDATA, r'\\\[\[', ST_EXPCDATA),
      (ENTITYREF, r'\\&[^;]+;', ST_ENTITY),
      ]

   __rawToks = \
      [
      (TAG, r'\\[^\s\(\{;\?\!\[&]+', ST_MARKUP),
      (LPAREN, r'\(', ST_MARKUP),
      (RPAREN, r'\)', ST_MARKUP),
      (EQUALS, r'=', ST_MARKUP),
      (LCURL, r'\{', ST_CDATA),
      (RCURL, r'\}', ST_CDATA),
      (DQSTRING, r'"([^"\\]|\\.)*"', ST_MARKUP),
      (SQSTRING, r"'([^'\\]|\\.)*'", ST_MARKUP),
      (WS, r'\s+', ST_MARKUP),
      (SEMICOLON, r';', ST_MARKUP),
      (NAME, r'[A-Za-z_:][A-Za-z_:\-.]*', ST_MARKUP),
      (COMMA, r',', ST_MARKUP),
      (CDATA, r'([^\\\{\}]|\\\\|\\\{|\\\})+', ST_MARKUP),
      (PI, r'\\\?', ST_PI),
      (COMMENT, r'\\!--', ST_COMMENT),
      (EXPCDATA, r'\\\[\[', ST_EXPCDATA),
      (ENTITYREF, r'\\&[^;]+;', ST_ENTITY),
      ]

   __piRawToks = \
      [
      (CDATA, r'([^\?]|\?[^>])+', ST_PI),
      (ENDPI, r'\?>', 0),
      ]

   __cmRawToks = \
      [
      (CDATA, r'([^\-]|-[^\-])+', ST_COMMENT),
      (ENDCOMMENT, r'-->', 0),
      ]
   
   __cdRawToks = \
      [
      (CDATA, r'[^\]]|\][^\]]|\]\][^>]', ST_EXPCDATA),
      (ENDCDATA, r'\]\]>', 0),
      ]      

   def __fixTokDefs(rawDefs):
      toks = []
      # compile all of the regular expressions      
      for id, rx, st in rawDefs:
         toks.append((id, re.compile(rx), st))
      return toks
   
   __fixTokDefs = staticmethod(__fixTokDefs)

   def __init__(self, src, srcName = '<file>', initLineNum = 1):
      """
         parms:
            src::
               [file.readline] source for tokenizer
            srcName::
               [string] source name
            initLineNum::
               [int] initial line number
      """
      self.__src = src
      self.__tokDef = \
         [
	 self.__fixTokDefs(self.__cdataToks),
         self.__fixTokDefs(self.__rawToks),
         self.__fixTokDefs(self.__piRawToks),
         self.__fixTokDefs(self.__cmRawToks),
         self.__fixTokDefs(self.__cdRawToks),
         ]
      self.__buf = ''
      self.__state = 0
      self.__name = srcName
      self.__lineNum = initLineNum

   def __iter__(self):
      return self
   
   def __fillBuffer(self):
      """
         Makes sure that the internal buffer is not empty.  Returns the
         contents of the buffer.
      """
      if not self.__buf:
         self.__buf = self.__src.readline()
      return self.__buf
   
   def __consume(self, match):
      """
         Removes the matching string from the internal buffer and returns
         the matching string.
         
         parms:
            match::
               [re.Match]
      """
      self.__buf = self.__buf[match.end():]
      return match.group()
   
   def next(self):
      if not self.__fillBuffer():
         return Token(-1, '', self.__name, self.__lineNum)
      
      for id, rx, newState in self.__tokDef[self.__state]:
         m = rx.match(self.__buf)
         if m:
#            sys.stderr.write('%s %s\n' %( id, m.group()))
            self.__state = newState
            text = self.__consume(m)
            tok = Token(id, text, self.__name, self.__lineNum)
            
            # increment the line number based on the number of newlines in the
            # text
            self.__lineNum += len(text.split('\n')) - 1
            
            return tok

class ParseError(Exception):
   """
      Public-vars:
         token::
            [@Token] token specifying the location of the error
   """
   
   def __init__(self, token, *parms):
      self.token = token
      Exception.__init__(self, *parms)
   
   def __str__(self):
      return '%s:%s: %s' % \
         (self.token.srcName, self.token.lineNum, Exception.__str__(self))

class BadEscapeSeq(ParseError):
   """
      Raised when a bad escape sequence (backslash followed by a character)
      is encountered.
   """
   pass

class ElementFactory:
   """
      Abstract base class for element factories - used to create specific
      @spug.web.xmlo.Element derived classes.
   """
   
   def makeElement(self, name, actualNS):
      """
         Creates and returns a new element object (@spug.web.xmlo.Element
         derivative).
         
         Must be implemented by derived class.
         
         parms:
            name::
               [string or tuple<string, string>] new element name.
               If a tuple, this is the explicit namespace URL and the local 
               name.
            actualNS::
               [string or None] The actual namespace of the element.
      """
      raise NotImplementedError()

class DefaultElementFactory(ElementFactory):
   """
      The most basic form of @ElementFactory, only creates 
      @spug.web.xmlo.Element instances.
   """
   def makeElement(self, name, actualNS):
      "Implements @ElementFactory.makeElement()"
      if isinstance(name, tuple):
	 name = name[1]
      return xmlo.Element((actualNS, name))

class CXMLParser:
   """
      Parses CXML.  This is an abstract base class.  Derived classes must
      implement all "handle" methods.
   """
   
   def __init__(self, src, srcName = '<file>', initLineNum = 1):
      """
         parms:
            src::
               [file.read] source stream
            srcName::
               [string] source file name
            initLineNum::
               [int] initial line number
      """
      self.__toker = Toker(src, srcName, initLineNum)

   def __discardWS(self):
      """
         Parses the next token, discarding all leading whitespace.
         
         Returns @Token.
      """
      tok = self.__toker.next()
      while tok.id == Toker.WS:
         tok = self.__toker.next()
      return tok

   def parseAttrDef(self, attrName):
      """
         Parses an attribute definition through the following comma
         or end paren.  Returns true if there are more attribute definitions
         to come.
         
         parms:
            attrName::
               [string]
      """

      # parse the equal sign
      tok = self.__discardWS()
      if tok.id != Toker.EQUALS:
         raise ParseError(tok, 
                          '"=" expected in attribute definition, got %s' % tok
                          )
   
      # parse a string (discard all leading whitespace)
      tok = self.__discardWS()
      if tok.id not in (Toker.SQSTRING, Toker.DQSTRING):
         raise ParseError(tok, 'Expected string, got %s' % tok)
      
      # write the attribute definition
      try:
         self.handleAttrDef(attrName, tok.val[1:-1], tok.srcName, tok.lineNum)
      except BadEscapeSeq, ex:
         raise ParseError(tok, 
                          'Bad escape sequence %s found in attribute value' %
                           ex[0]
                          )
      
      # parse the comma or end paren
      tok = self.__discardWS()
      if tok.id == Toker.COMMA:
         return 1
      elif tok.id == Toker.RPAREN:
         return 0
      else:
         raise ParseError(tok, 
                          'Expected "," or ")" in attribute definition, got '
                           '%s' % tok
                          )

   def parseElem(self, elemName):
      tok = self.__toker.next()
      while tok.id == Toker.WS:
         tok = self.__toker.next()
      
      # handle the beginning of the element
      self.handleElemStart(elemName, tok.srcName, tok.lineNum)
      
      if tok.id not in  (Toker.LPAREN, Toker.LCURL, Toker.SEMICOLON) :
         raise ParseError(tok, '"(", "{" or ";" expected, got %s' % tok)
      
      if tok.id == Toker.LPAREN:
      
         # parse the attribute list
         while 1:
            tok = self.__toker.next()
            
            if tok.id == Toker.NAME:
               if not self.parseAttrDef(tok.val):
                  break
            elif tok.id == Toker.WS:
               self.handleAttrWS(tok.val)
            else:
               raise ParseError(tok, 
                                'Expected attribute definition, got %s' % tok
                                )
      
         # parse the next token for the rest of the method
         tok = self.__discardWS()
      
      if tok.id == Toker.SEMICOLON:
         self.handleElemEnd()
      elif tok.id == Toker.LCURL:
         self.handleContentStart()
         self.parseElems(1)
         self.handleContentEnd()
         self.handleElemEnd()

   class __CharDataFixer:
      __badTextDataRx = re.compile(r'&|<|\\.\n', re.DOTALL)
   
      __textEscChr = \
         {
         't': '&#9;',
         'n': '&#10;',
         '\\': '\\',
         '}': '}',
         '{': '{',
         }

      def __init__(self, token):
         self.srcName = token.srcName
         self.lineNum = token.lineNum
         self.val = token.val
      
      def fix(self):
         return self.__badTextDataRx.sub(self, self.val)
   
      def __call__(self, match):
         val = match.group()
         if val == '\n':
            self.lineNum += 1
            return val
         elif val == '&':
            return '&amp;'
         elif val == '<':
            return '&lt;'
         else:
            expanded = self.__textEscChr[val[1]]
            if not expanded:
               raise BadEscapeSeq(Token(0, val, self.srcName, self.lineNum))
            else:
               return expanded         

   def fixCharData(self, tok):
      """
         Fixes character data by escaping markup start chars and unescaping
         CXML escape sequences.
      """
      return self.__CharDataFixer(tok).fix()

   def parseLiteral(self, begin, end, endTok):
      """
         Parse any of the special "literal" tags that contain no markup
         (processing instructions, comments and CDATA).
         
         parms:
            begin::
               [callable<>] function to call before content.
            end::
               [callable<>] function to call after content.
            endTag::
               [int] type of token signalling the end of the literal.
      """
      begin()
      while 1:
         tok = self.__toker.next()
         if tok.id == endTok:
            end()
            return
         elif tok.id == Toker.END:
            raise ParseError(tok, 
                             'Unexpected end of file in processing instruction'
                             )
         else:
            self.handleSpecialData(tok.val)

   def parseElems(self, nested):
      """
         Parses all alements
         
         parms:
            nested::
               [boolean] true if we are in a nested context - if not nested,
               a bare '}' raises an exception.
      """
      while 1:
         tok = self.__toker.next()
         if tok.id == Toker.END:
            break
         elif tok.id == Toker.TAG:
            self.parseElem(tok.val[1:])
         elif tok.id == Toker.RCURL:
            if nested:
               return
            else:
               raise ParseError(tok, 'Unmatched right bracket')
         elif tok.id == Toker.PI:
            self.parseLiteral(self.handlePIStart, self.handlePIEnd, 
                              Toker.ENDPI
                              )
         elif tok.id == Toker.COMMENT:
            self.parseLiteral(self.handleCommentStart, self.handleCommentEnd, 
                              Toker.ENDCOMMENT
                              )
         elif tok.id == Toker.EXPCDATA:
            self.parseLiteral(self.handleCDataStart, self.handleCDataEnd, 
                              Toker.ENDCDATA
                              )
         elif tok.id == Toker.ENTITYREF:
            self.handleEntityRef(tok.val[1:])
         else:
            self.handleCharData(tok.val)
   
   def parse(self):
      self.parseElems(0)

   def handleAttrDef(self, attr, val, srcName, lineNum):
      pass

   def handleElemStart(self, elemName, srcName, lineNum):
      pass

   def handleAttrWS(self, val):
      """
         Called for white space in an attribute list.
      """
      pass

   def handleElemEnd(self):
      """
         Called to terminate the current element.
      """
      pass
   
   def handleContentStart(self):
      """
         Called when element content is started.
      """
      pass

   def handleContentEnd(self):
      """
         Called when element content is finished.
      """
      pass
   

   def handleEntityRef(self, val):
      pass

   def handleCharData(self, data):
      pass

   def handlePIStart(self):
      pass
   
   def handlePIEnd(self):
      pass
   
   def handleCommentStart(self):
      pass
   
   def handleCommentEnd(self):
      pass
   
   def handleCDataStart(self):
      pass
   
   def handleCDataEnd(self):
      pass
   
   def handleSpecialData(self, data):
      """
         This is called for content of a processing instruction, comment, 
         or CData block.
      """
      pass

class _Elem:
   
   def __init__(self, name):
      self.name = name
      self.gotContent = 0

class CXMLConverter(CXMLParser):
   """
      Converts CXML directly to XML on an output stream.
   """
   
   
   def __init__(self, src, dst, srcName = '<file>', initLineNum = 1):
      CXMLParser.__init__(self, src)
      self.__dst = dst
      self.__elems = []
      self.__isFirstAttr = 1

   __sqBadAttrDataRx = \
      re.compile(r"'|&|<|\\x[0-9A-Fa-f]{2}|\\[0-7]{3}|\\[^x0-9]")
   __dqBadAttrDataRx = \
      re.compile(r'"|&|<|\\x[0-9A-Fa-f]{2}|\\[0-7]{3}|\\[^x0-9]')
   
   __attrEscChr = \
      {
      't': '&#9;',
      'n': '&#10;',
      '"': '&quot;',
      "'": '&apos;',
      '\\': '\\',
      }
   
   def __fixBadAttrChrs(self, match):
      val = match.group()
      if val == '&':
         return '&amp;'
      elif val == "'":
         return '&apos;'
      elif val == '"':
         return '&quot;'
      elif val == '<':
         return '&lt;'
      elif val[:2] == '\\x':
         return '&#x%s;' % val[2:]
      elif val[0] == '\\' and val[1] in string.digits:
         return '&#%d;' % eval('0' + val[1:])
      elif val[0] == '\\':
         expanded = self.__attrEscChr[val[1]]
         if not expanded:
            raise BadEscapeSeq(Token(0, val, 'bogus', 0), val)
         else:
            return expanded

   def fixAttrVal(self, attrVal):
      """
         "Fixes" an attribute value by replacing all forbidden characters
         with acceptable ones.
      """
      if attrVal[0] == '"':
         return '"' + \
            self.__dqBadAttrDataRx.sub(self.__fixBadAttrChrs, 
                                       attrVal[1:-1]
                                       ) + \
            '"'
      else:
         return "'" + \
            self.__sqBadAttrDataRx.sub(self.__fixBadAttrChrs, 
                                       attrVal[1:-1]
                                       ) + \
            "'"
         

   def handleAttrDef(self, attr, val, srcName, lineNum):
      if self.__isFirstAttr:
         self.__dst.write(' ')
      self.__dst.write('%s=%s' % (attrName, self.fixAttrVal(val)))
      self.__isFirstAttr = 0

   def handleElemStart(self, elemName, srcName, lineNum):
      self.__elems.append(_Elem(elemName))
      self.__dst.write('<%s' % elemName)
      self.__isFirstAttr = 1

   def handleAttrWS(self, val):
      self.__dst.write(val)

   def handleElemEnd(self):
      elem = self.__elems.pop()
      if elem.gotContent:
         self.__dst.write('</%s>' % elem.name)
      else:
         self.__dst.write('/>')

   def handleContentStart(self):
      self.__elems[-1].gotContent = 1
      self.__dst.write('>')

   def handleEntityRef(self, val):
      self.__dst.write(tok.val[1:])

   def handleCharData(self, data):
      self.__dst.write(self.fixCharData(data))

   def handlePIStart(self):
      self.__dst.write('<?')
   
   def handlePIEnd(self):
      self.__dst.write('?>')
   
   def handleCommentStart(self):
      self.__dst.write('<!--')
   
   def handleCommentEnd(self):
      self.__dst.write('-->')
   
   def handleCDataStart(self):
      self.__dst.write('<![CDATA[')
   
   def handleCDataEnd(self):
      self.__dst.write(']]>')
   
   def handleSpecialData(self, data):
      self.__dst.write(data)

class ElementParser(CXMLParser):
   """
      Creates a @spug.web.xmlo.Element tree from the parsed CXML.
   """
   
   def __init__(self, src, elementFactory = DefaultElementFactory(), 
                srcName = '<file>',
                initLineNum = 1
                ):
      """
         parms:
            src::
               [file.read] source stream
            elementFactory::
               [@ElementFactory] factory used to create element objects.
            srcName::
               [string] source file or stream name
            initLineNum::
               [int] initial line number
      """
      CXMLParser.__init__(self, src, srcName, initLineNum)
      self.__root = None
      self.__cur = None
      self.__elemName = None
      self.__elemAttrs = []
      self.__elemSrcName = None
      self.__elemLineNum = None
      self.__inCData = 0
      self.__elemFact = elementFactory

   def handleEntityRef(self, val):
   
      # ignore if we're not in an element
      if not self.__cur:
         return
      
      if val == '&lt;':
         self.__root.append('<')
      elif val == '&gt;':
         self.__root.append('>')
      elif val == '&apos;':
         self.__root.append("'")
      elif val == '&amp;':
         self.__root.append('&')
      elif val == '&quot;':
         self.__root.append('"')
      else:
         raise Exception('Unknown entity reference: %s' % val)

   def handleCharData(self, data):
      if self.__cur:
         self.__cur.append(data)

   def __getAccessor(self, name, localNSMap, srcName, lineNum):
      parts = name.split(':')
      if len(parts) == 2:
      
         # get the namespace for the prefix, try the local map first
         if localNSMap.has_key(parts[0]):
            ns = localNSMap[parts[0]]
         else:
            ns = self.__cur.getNamespace(parts[0])
         
         # make sure we got one
         if ns is None:
            raise ParseError(Token(0, '', srcName, lineNum),
                             'Unknown namespace prefix %s' % parts[0]
                             )
         
         return ns, parts[1]
      elif len(parts) != 1:
         raise ParseError(Token(0, '', srcName, lineNum),
                          'Malformed element name %s' % name
                          )
      else:
         return name

   def __fixElem(self):

      # if we did this before, we're done
      if not self.__elemName:
         return

      # apply namespace identifiers first
      attrs = []
      nsMap = {}
      defaultNS = None
      for attr, val, srcName, lineNum in self.__elemAttrs:
         if attr == 'xmlns':
            nsMap[None] = val
         elif attr.startswith('xmlns:'):
            nsMap[attr[6:]] = val
         else:
            attrs.append((attr, val, srcName, lineNum))

      # fix the element name
      elemName = self.__getAccessor(self.__elemName, nsMap, self.__elemSrcName,
                                    self.__elemLineNum
                                    )
      
      # compute actual namespace for the node - this is only an issue
      # if there was no namespace qualifier, then we have to figure out the 
      # default namespace
      if isinstance(elemName, str):
         
         # see if a default namespace is specified locally.
         if nsMap.has_key(None):
            actualNS = nsMap[None]
         elif self.__cur:
            actualNS = self.__cur.getDefaultNamespace()
         else:
            actualNS = None
   
      else:
         actualNS = elemName[0]
      
      # create the element
      elem = self.__elemFact.makeElement(elemName, actualNS)
      
      # add the namespace attributes
      for ns, url in nsMap.items():
         if ns:
            elem['xmlns', ns] = url
         else:
            elem['xmlns'] = url
   
      # add the other attributes
      for attr, val, srcName, lineNum in attrs:
         elem[self.__getAccessor(attr, nsMap, srcName, lineNum)] = val
   
      # if there is no root node, make this the root node.  Otherwise, make
      # it a child of the current node
      if not self.__root:
         self.__root = elem
      else:
         self.__cur.append(elem)
      self.__cur = elem
      
      # clear the element name as an indicator that we've been here
      self.__elemName = None

   def handleAttrDef(self, attr, val, srcName, lineNum):
      self.__elemAttrs.append((attr, val, srcName, lineNum))

   def handleElemStart(self, elemName, srcName, lineNum):
      self.__elemName = elemName
      self.__elemAttrs = []
      self.__elemSrcName = srcName
      self.__elemLineNum = lineNum

   def handleElemEnd(self):
      """
         Called to terminate the current element.
      """
      self.__fixElem()
      self.__cur = self.__cur.getParent()
   
   def handleContentStart(self):
      """
         Called when element content is started.
      """
      self.__fixElem()

   def handleCDataStart(self):
      self.__inCData = 1
   
   def handleCDataEnd(self):
      self.__inCData = 0
   
   def handleSpecialData(self, data):
      """
         This is called for content of a processing instruction, comment, 
         or CData block.
      """
      if self.__inCData and self.__cur:
         self.__cur.append(data)

   def getRootElem(self):
      return self.__root

if __name__ == '__main__':
   import cStringIO
   import sys
   src = cStringIO.StringIO(r'''
\root(xmlns = 'default-namespace', xmlns:alt = 'alternate-namespace') {
   \alt:foo( alt:bar = 'this is a test') {
      this is content, \em{this is emphasized}
   }
   \alt:foo {
      another item
   }
}
''')
   parser = ElementParser(src)
   parser.parse()
   root = parser.getRootElem()
   print root.getFullName()
   print root.getDefaultNamespace()
   print root.getNamespace('alt')
   print root.getChild('alternate-namespace', 'foo')
   root.writeTo(sys.stdout)
   
   # tests
   if root.getChild('alternate-namespace', 'foo')['alternate-namespace', 'bar'] != 'this is a test':
      print 'failed test of qualified attribute access'

   src = cStringIO.StringIO(r'''
\foo {
   \bar(x = 100);
}''')
   parser = ElementParser(src, srcName = '<string>')
   try:
      parser.parse()
      print 'failed test of parse errors'
   except ParseError, ex:
      if ex.token.srcName != '<string>' or ex.token.lineNum != 3:
         print 'failed test of parse errors: bad error token'

   src = cStringIO.StringIO(r'''
\foo {
   \bar(x:y = 'test');
}''')
   parser = ElementParser(src, srcName = '<string>')
   try:
      parser.parse()
      print 'failed test of attribute qualifier parse errors'
   except ParseError, ex:
      if ex.token.srcName != '<string>' or ex.token.lineNum != 3:
         print 'failed test of attribute qualifier parse errors: bad error token'

   src = cStringIO.StringIO(r'''
\foo {
   \x:bar(a = 'test',
      b = 'this'
   );
}''')
   parser = ElementParser(src, srcName = '<string>')
   try:
      parser.parse()
      print 'failed test of element qualifier parse errors'
   except ParseError, ex:
      if ex.token.srcName != '<string>' or ex.token.lineNum != 3:
         print 'failed test of element qualifier parse errors: bad error token'
