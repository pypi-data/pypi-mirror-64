
import socket, struct, string

class Error(Exception):
   "Raised on a protocol error"

class SOCKSSocket:

   """
      This is an extremely simple SOCKS socket class.  To use it
      create an instance, and it will automatically connect to 
      your destination through your SOCKS firewall.
      
      At this point you can either apply socket methods directly
      to this object (optionally using the /reader/ and /writer/
      attributes as input and output files), or you can directly
      operate on the /sock/ attribute, which is the connected
      socket object.
      
      Example:
      
      {{
         # connect to foreign.host.com's http server via 
         # socks-server.domain.com
         s = SOCKSSocket('socks-server.domain.com', 'foreign.host.com', 80)
         
         # get the index page
         s.writer.write('GET /\n')
         s.writer.flush()
         
         # read the result
         print s.reader.read()
         
         # close the socket explicitly (this is unnecessary, but demonstrates
         # our direct access to the _real_ socket object.
         s.sock.close()
      }}
      
      Public-vars:
         sock::
            A standard python socket object instance.
         reader::
            Input file object for the socket
         writer::
            Output file object for the socket
   """
   
   def __init__(self, socksServer, foreignServer, foreignPort,
                socksPort = 1080,
                userId = '',
                ):
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.connect((socksServer, socksPort))
      
      # convert the foreign adddress to a list of integers, then
      # to a single integer
      foreignServerAddr = \
         map(int, string.split(socket.gethostbyname(foreignServer), '.'))
      foreignServerAddr = foreignServerAddr[0] << 24 | \
         foreignServerAddr[1] << 16 | \
         foreignServerAddr[2] << 8 | \
         foreignServerAddr[3]
      
      # create the initial request:
      #  socks version = 4
      #  command = 1 (connect)
      #  remote port number
      #  remote IP address
      req = struct.pack('>bbhl', 4, 1, foreignPort, foreignServerAddr)
      
      # append the user id
      req = '%s%s\000' % (req, userId)
      
      # create some streams
      self.writer = self.sock.makefile('wb')
      self.reader = self.sock.makefile('rb')
      
      # write the request
      self.writer.write(req)
      self.writer.flush()
      
      # read the reply, 90 indicates success
      reply = self.reader.read(8)
      if ord(reply[1]) != 90:
         raise Error('Connection refused')
   
   def __getattr__(self, attr):
      return getattr(self.sock, attr)
