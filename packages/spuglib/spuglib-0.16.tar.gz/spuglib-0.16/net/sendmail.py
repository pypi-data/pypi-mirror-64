#==============================================================================
#
#  $Id: sendmail.py 565 2000-02-15 23:14:49Z mike $
#
"""
   This module contains a bunch of classes for doing e-mail.   
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
#  $Log: sendmail.py,v $
#  Revision 1.4  2000/02/15 23:14:49  mike
#  First cut at the new make paradigm.
#
#  Revision 1.3  1999/04/08 00:53:14  mike
#
#  Made e-mail addresses and mail manager aware of multiple delivery hosts.
#
#  Revision 1.2  1999/01/03 19:30:54  mike
#  Added RSET command for "unknown recipient" problem.
#  Added methods to support forking a mail agent.
#
#  Revision 1.1  1998/12/27 01:03:38  mike
#  Initial revision
#
#
#==============================================================================


import re, socket, string, time, os
from StringIO import StringIO
from spug.util import quickle

class UnexpectedResponse(Exception):
   """
      This is raised when the server sends back an unexpected response.
   """
   pass

class MalformedEMailAddress(Exception):
   """
      Raise by the @parseEMailAddress() function when a badly formed e-mail
      address is encountered.  The parameter passed in to the exception
      malformed address.
   """
   pass

_emailAddressRx = re.compile(r'(\S+)@(\S+)')

def parseEMailAddress(addressString):
   """
      Returns an EMailAddress parsed from the given address string.  At this
      time, all addresses must be of the form "user@host".
      
      Raises a @MalformedEMailAddress exception if the address doesn't parse.
   """
   match = _emailAddressRx.match(addressString)
   if not match:
      raise MalformedEMailAddress(addressString)
   return EMailAddress(match.group(1), match.group(2))

class EMailAddress:
   """
      Contains an e-mail address.
      
      Public variables:
      /login/::
         User login name.
      /host/::
         `TCP/IP` host name.
      /fullName/::
         Full name of the user.
   """
   def __init__(self, login, host, fullName = ''):
      self.login = login
      self.host = host
      self.fullName = fullName
      self.__handlerAddresses = []
   
   def asAddress(self):
      """
         Returns the e-mail address formatted as user@hostname.
      """
      return self.login + '@' + self.host
   
   def asHeader(self):
      """
         Returns the e-mail address formatted in a manner suitable for a
         header line: "Full Name <user@hostname>".  If /fullName/ is 
         an empty string, the user login is substituted for the full name.
      """
      if self.fullName:
         return self.fullName + ' <' + self.asAddress() + '>'
      else:
         return self.login + ' <' + self.asAddress() + '>'

   def setHandlerAddresses(self, addrs):
      """
         Used to set the mail handler host addresses for the e-mail domain.
      """
      self.__handlerAddresses = addrs
   
   def getHandlerAddresses(self):
      """
         Returns the mail handler host addresses for the e-mail domain.
      """
      
      # this is extremely weak, but it preserves the original interface
      # XXX really want a nameserver lookup
      if not self.__handlerAddresses:
         self.__handlerAddresses = [ self.host ]
         
      return self.__handlerAddresses

class Mailer:

   """
      A *Mailer* manages a connection to a single sendmail daemon.
   """

   ipRx = r'\d+\.\d+\.\d+\.\d+'

   def send(self, data):
      """
         Sends /data/ (a string) to the mail daemon at the other end.
         
         This is normally for internal use only.
      """
      if self.debug:
         print "send: " + repr(data)
      self.dest.write(data)
      self.dest.flush()

   def waitFor220(self):
      """
         Waits for a 220 line from the server.
         
         This is normally for internal use only.
      """
      line = self.readline()
      if line[:3] != '220':
         raise UnexpectedResponse('220 expected.')
   
   def waitFor(self, code):
      """
         Waits for a particular 3 character code from the server, discards
         all 220's that are returned.
      """
      while 1:
         line = self.readline()
         if line[:3] == code:
            return
         elif line[:3] != '220':
            raise UnexpectedResponse(code + ' expected')
   
   def sendMessage(self, fromUser, toUser, messageBody):
      """
         Sends the message in the /messageBody/ string to the user identified
         by /toUser/.  /toUser/ and /fromUser/ should both be instances of
         @EMailAddress.
      """
      try:
         self.send('MAIL From:<' + fromUser.asAddress() + '>\r\n')
         self.waitFor('250')
         self.send('RCPT To:<' + toUser.asAddress() + '>\r\n')
         self.waitFor('250')
         self.send('DATA\r\n')
         self.waitFor('354')
         for line in string.split(messageBody, '\n'):
            # lines with just a period might be misconstrued
            if line == '.':
               line = ' .'
            self.send(line + '\r\n')
         self.send('.\r\n')
         self.waitFor('250')
      except UnexpectedResponse, ex:
         # try to recover
         self.send('RSET\r\n')
         self.waitFor('250')
         
         raise ex
   
   def readline(self):
      """
         Returns the next `CR/LF` or LF terminated line from the server.
         
         This is normally for internal use only.
      """
      buf = self.src.readline()
      if self.debug:
         print "recv: " + repr(buf)   
      return buf

   def __init__(self, host, debug = 0):
      """
         Constructs a new Mailer object, creating a connection to the
	 specified host.  /host/ should be a string specifying either a
	 dotted ip address or a host name.

         if /debug/ is true, all sends and receives are printed.
      """
      self.host = host
      self.debug = debug
#      if ipRx.match(host):
#         self.ipAddr = host
#      else:
#         self.ipAddr = socket.gethostbyname(host)
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.connect( (self.host, 25) )
      self.src = self.sock.makefile('r')
      self.dest = self.sock.makefile('w')
      self.waitFor220()
      self.send('HELO ' + socket.gethostname() + '\r\n')
      self.waitFor('250')

class EMailMessage:
   """
      Sort of like an RFC822 message, only not limited to its file
      structure.
      
      Public variables:
      /fromAddr/::
         The source @EMailAddress.
      /toAddr/::
         A list of destination @EMailAddress instances.
      /date/::
         The date that the message was constructed as a UNIX time value.
      /subject/::
         Message subject.
      /cc/::
         A list of cc @EMailAddress instances.
      /bcc/::
         A list of bcc @EMailAddress instances.
      /body/::
         A string representing the body of the message.
      
      XXX should probably store its complete string representation so we
      don't have to render it every time that we process the queue.
   """
   
   def __init__(self, fromAddr, toAddrs, date, subject, body, cc = [], bcc = []):
      """
         Constructor.  /fromAddr/ is an both instances of @EMailAddress,
	 /date/ should be a UNIX time value.  /subject/ should be a string.
	 /body/ should also be a string (and may contain newlines).  /cc/,
	 /bcc/, and /toAddrs/ should both be a list of @EMailAddress
	 instances.
      """
      self.fromAddr = fromAddr
      self.toAddrs = toAddrs
      self.date = date
      self.subject = subject
      self.body = body
      self.cc = cc
      self.bcc = bcc
      self.deliver = toAddrs + cc + bcc
      self.deliver.sort(lambda addr1, addr2: cmp(addr1.host, addr2.host))
   
   def _writeAddressList(self, out, addrs):
      """
         Writes a list of addresses to the given output stream.
      """
      
      # write the first address so that we can precede all folowing addresses
      # with commas.
      if addrs:
         out.write(addrs[0].asHeader())
      
      # write each of the following addresses
      for addr in addrs[1:]:
         out.write(', ' + addr.asHeader())
   
   def writeTo(self, out):
      """
         Writes the message onto the given output stream /out/.
      """
      out.write('Date: ' + 
                 time.strftime('%a, %d %b %Y %H:%M:%S ', 
                               time.localtime(self.date)
                               ) +
                 '%04d\n' % (-time.timezone / 36 - time.timezone / 60 % 60)
                )
      out.write('To: ')
      self._writeAddressList(out, self.toAddrs)
      out.write('\n')
      
      out.write('From: %s\n' % self.fromAddr.asHeader())
      
      if self.cc:
         out.write('Cc: ')
         self._writeAddressList(out, self.cc)
         out.write('\n')
      
      if self.bcc:
         out.write('Bcc: ')
         self._writeAddressList(out, self.bcc)
         out.write('\n')
      
      out.write('Subject: %s\n' % self.subject)
      out.write('\n' + self.body)       

   def deliveredTo(self, addr):
      """
         This method is used to indicate that the message has been delivered
         to the given address.  The address will be removed from the list
         of addresses that it must be delivered to.
      """
      if addr in self.deliver:
         self.deliver.remove(addr)
   
   def getDeliveryList(self):
      """
         Returns the list of addresses that the message must still be
	 delivered to sorted by host.  Note that this list is the same list
	 that is used internally, so the caller should not attempt to modify
	 it.
      """
      return self.deliver

class MailManager: 
   """ 
      A MailManager attempts to do everything that the client side of
      sendmail does - poorly.

      Create an instance of a mail manager, and send messages to it.  Then
      invoke @processQueue().  The MailManager will take care of making sure
      that the messages get delivered, and storing them if they are not.

      You may also use the @spawnMailAgent(), @waitOnMailAgent() and
      @mailAgentFinished() methods to fork off the mail queue processing
      in another process.
   """
   
   def __init__(self, mailqueue = '/var/MailManagerQueue', debug = 0):
      """
         Constructs a new instance using the given filename as the location
         for the mail queue.
         
         If /debug/ has the 1 bit set, activity during queue processing
         is written to standard output.  If its 2 bit is set, @Mailer
         debug mode is set (which displays all connection info).
      """
      self.qfile = mailqueue
      try:
         self.queue = quickle.load(self.qfile)
      except IOError, ex:
         self.queue = []
   
   def processQueue(self):
      """
         Walks through the mail queue and attempts to send each of the
         messages.
      """
      # build a mapping from hosts to the messages that go to them.  The 
      # messages will be a tuple of the message object and its string form.
      hosts = {}
      handlerAddresses = {}
      for elem in self.queue:
      
         # convert the message to its string form
         str = StringIO()
         elem.writeTo(str)
         
         # construct a tuple associating the message object with its value
         entry = elem, str.getvalue()
         
         # walk through the list of addresses to deliver to, add an entry for
         # each of the hosts.
         for addr in elem.getDeliveryList():
            host = string.lower(addr.host)
            if not hosts.has_key(host):
               hosts[host] = [ (addr,) + entry ]
            else:
               hosts[host].append((addr,) + entry)
            
            # make sure that we also have a set of mail handler addresses
            # for that host.
            if not handlerAddresses.has_key(host):
               handlerAddresses[host] = addr.getHandlerAddresses()

      # walk through the list of hosts and deliver the messages to each of
      # the hosts.
      for host, msgs in hosts.items():
      
         try:
         
            # open a new connection to one of the host's mail handlers
            for handler in handlerAddresses[host]:
               print "opening connection to " + host
               try:
                  mailer = Mailer(host)
                  break
               except (socket.error, UnexpectedResponse), ex:
                  pass
            else:
               raise UnexpectedResponse("No handlers available")
               
            for addr, msg, msgStr in msgs:
            
               # send the message to the host.  If we fail, just
               # bypass all of the stuff indicating that we delivered 
               # successfully.
               try:
                  print "sending message to " + addr.asAddress()
                  mailer.sendMessage(msg.fromAddr, addr, msgStr)
               except UnexpectedResponse, ex:
                  print "Unable to deliver to " + addr.asAddress()
                  continue
               
               # now we can remove this address from the list of those to be
               # delivered to.
               msg.deliveredTo(addr)                  
               
               # remove the message from the queue if there is no one left
               # to deliver to
               if not msg.getDeliveryList():
                  self.queue.remove(msg)
         except (socket.error, UnexpectedResponse), ex:
            print "Unable to connect to host " + host

   def enqueueMessage(self, msg):
      """
         Adds the given message (which should be an instance of
         @EMailMessage) to the queue.
      """
      self.queue.append(msg)
   
   def writeQueue(self):
      """
         Writes the queue to the queue file.
      """
      quickle.dump(self.queue, self.qfile)

   def spawnMailAgent(self):
      """
         Forks and lets the child process process the queue.  Obviously,
         the fork command must be supported.
      """
      self.pid = os.fork()
      if not self.pid:
         self.processQueue()
         self.writeQueue()
         import sys
         sys.exit(0)
   
   def waitOnMailAgent(self):
      """
         Waits for a mail agent spawned with @spawnMailAgent() to finish.
         
         Since this uses the *waitpid* command, any subsequent attempts
         to use this after the initial wait will fail.
      """
      os.waitpid(self.pid, 0)
   
   def mailAgentFinished(self):
      """
         Returns true if a previously spawned mail agent has finished
         processing.
         
         Since this uses the *waitpid* function, once it succeeds it can
         not be used again.
      """
      return os.waitpid(self.pid, os.WNOHANG)[0] and 1

