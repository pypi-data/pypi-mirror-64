#==============================================================================
#
#  $Id$
#
"""
   Contains the @ChildProcess class - an abstraction that makes it easy to deal
   with child processes.
"""
#
#  Copyright (C) 2003 Michael A. Muller
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

import os, select, sys, traceback
from signal import *
from spug.io.reactor import Reactable, MTU

try:
   # use the "PIPE" variable from subprocess if it exists so that subprocess
   # can be used instead of ForkExecer
   import subprocess
   _PIPE = subprocess.PIPE
except ImportError:
   _PIPE = -1

class _Stream:

   def __init__(self, handle):
      self.__fd = handle

   def __del__(self):
      if self.__fd:
         self.close()

   def read(self, size):
      return os.read(self.__fd, size)

   def write(self, data):
      os.write(self.__fd, data)

   def flush(self):
      # since we use write, we don't need to flush
      pass

   def fileno(self):
      return self.__fd

   def close(self):
      os.close(self.__fd)
      self.__fd = None

class ForkExecer:
   """
      Standard implementation of fork\/exec.  Creates a new process on
      construction with wrapped pipes for communication to stdin, stdout, and
      stderr.
   """

   def __init__(self, cmd, stdin = None, stdout = None, stderr = None):

      # create all of the pipes
      if stdout == _PIPE:
         fromChild, toParent = os.pipe()
      if stderr == _PIPE:
         fromChildErr, toParentErr = os.pipe()
      if stdin == _PIPE:
         fromParent, toChild = os.pipe()

      self.__pid = os.fork()
      if not self.__pid:
         # -- child process --

         # close parent-side streams and dup handles to child's standard in,
         # out and error
         if stdout == subprocess.PIPE:
            os.close(fromChild)
            os.dup2(toParent, 1)
         if stderr == subprocess.PIPE:
            os.close(fromChildErr)
            os.dup2(toParentErr, 2)
         if stdin == subprocess.PIPE:
            os.close(toChild)
            os.dup2(fromParent, 0)

         # ... and finally, exec the process.  If we fail on the exec, we 
         # have to do a low-level exit
         try:
            os.execv(cmd[0], cmd)
            # the buck stops here.
         except OSError as ex:
            # write and flush (we won't get a flush during exit)
            sys.stderr.write(str(ex))
            sys.stderr.flush()
         except:
            traceback.print_exc()
         os._exit(1)
      else:
         # close out the child-side pipes and instantiate wrappers around the
         # streams
         if stdin == subprocess.PIPE:
            os.close(fromParent)
            self.stdin = _Stream(toChild)
         if stderr == subprocess.PIPE:
            os.close(toParentErr)
            self.stderr = _Stream(fromChildErr)
         if stdout == subprocess.PIPE:
            os.close(toParent)
            self.stdout = _Stream(fromChild)

   def wait(self):
      """
         Wait for child process to terminate and returns its exit code.
      """
      return os.waitpid(self.__pid, 0)[1] >> 8

   def kill(self, signal = SIGTERM):
      """
         Kills the process with the given signal.  You should still call
         "wait" after calling this or you will accumulate zombies.
      """
      os.kill(self.__pid, signal)

def _createProcessStarter():
   return ForkExecer

class StreamWrapper(Reactable):
   """
      Base class for wrappers for stdin/out/err streams that provide access 
      to their associated child process and function as a reactable.
      
      Public-vars:
         process: [@ChildProcess] the associated child process
   """
   
   def __init__(self, process, stream):
      self.process = process
      self.__stream = stream

   def __getattr__(self, attr):
      return getattr(self.__stream, attr)

   def fileno(self):
      """
         Returns the file descriptor.
      """
      rc = self.__stream.fileno()
      return rc

class OutputStreamWrapper(StreamWrapper):
   """
      Wrapps stdout/err streams.
   """
   def __init__(self, process, stream, gotData):
      StreamWrapper.__init__(self, process, stream)
      self.__gotData = gotData

   def wantsToRead(self):
      """
         Returns true if the connection should be checked for readability
      """
      return True

   def wantsToWrite(self):
      """
         Returns true if the connection should be checked for writability.
      """
      return False

   def handleRead(self, dispatcher):
      """
         Called when the connection is ready to read.
      """
      data = self.read(MTU)
      self.__gotData(data)

   def handleWrite(self, dispatcher):
      """
         Called when the connection is ready to write.
      """
      raise NotImplementedError()

   def handleError(self, dispatcher):
      """
         Called when there is an error.
      """
      print("Stream got an error")
      dispatcher.removeReactor(dispatcher)

   def handleDisconnect(self, dispatcher):
      """
         Called when a disconnect occurs.
      """
      dispatcher.removeReactable(self)

class InputStreamWrapper(StreamWrapper):
   """
      Wrapps stdout/err streams.
   """
   def wantsToRead(self):
      """
         Returns true if the connection should be checked for readability
      """
      return False

   def wantsToWrite(self):
      """
         Returns true if the connection should be checked for writability.
      """
      return True

   def handleRead(self, dispatcher):
      """
         Called when the connection is ready to read.
      """
      raise NotImplementedError()

   def handleWrite(self, dispatcher):
      """
         Called when the connection is ready to write.
      """
      if self.process._handleWrite():
         dispatcher.removeReactable(self)

   def handleError(self, dispatcher):
      """
         Called when there is an error.
      """
      print("Stream got an error")
      self.handleDisconnect(self, dispatcher)

   def handleDisconnect(self, dispatcher):
      """
         Called when a disconnect occurs.
      """
      dispatcher.removeReactable(self)

class ChildProcess:
   """ Creates a child process and handles output to it and input from it.
   """

   def __init__(self, cmd, start = False, processStarter = ForkExecer,
                noPipes = False,
                noStdIn = False,
                noStdOut = False,
                noStdErr = False
                ):
      """
         parms:
            cmd::
               [list<string>] a list of the command arguments.  The first item
               in the list is the fully qualified path to the program to
               execute.
            start::
               [boolean] if true, start the process immediately.  If false,
               the process must be explicitly started using the @start()
               method.
            processStarter::
               [callable<list<string>>] A function which accepts a list of
               arguments (including an executable as the zeroth argument) and
               returns a process object.  The process object must have a
               wait() method (which waits for process termination) and stdin,
               stdout and stderr attributes, which are file objects
               implementing fileno() and read().
            noPipes::
               [boolean] disables all pipes (stdin, stdout & stderr) to and
               from the child.  Equivalent to setting all of /noStdIn/,
               /noStdOut/, and /noStdErr/ to True.
            noStdIn::
               [boolean] disables standard input to the child
            noStdOut::
               [boolean] disables collection of standard output from the
               child.  child standard output will go to the parent process
               standard output.  @gotOutput() will never be called.
            noStdErr::
               [boolean] disables collection of standard error from the
               child.  child standard error will go to the parent process
               standard error.  @gotError() will never be called.
      """
      self.__cmd = cmd
      self.__proc = None
      self.__procFact = processStarter

      if noPipes:
         noStdIn = noStdOut = noStdErr = True
      self.__noStdIn = noStdIn
      self.__noStdOut = noStdOut
      self.__noStdErr = noStdErr

      # data queued for input to the child process
      self.__inputData = []

      if start:
         self.start()
   
   def __getStdin(self):
      if not self.__proc: self.start()
      return InputStreamWrapper(self, self.__proc.stdin)
   stdin = property(__getStdin, 
                    doc = """
                     The child process stdin stream.  This is an 
                     InputStreamWrapper instance.  Note that every time this 
                     attribute is accessed, a new StreamWrapper is created.
                    """)
   
   def __getStdout(self):
      if not self.__proc: self.start()
      return OutputStreamWrapper(self, self.__proc.stdout, self.gotOutput)
   stdout = property(__getStdout, 
                    doc = """
                     The child process stdout stream.  This is a 
                     OutputStreamWrapper instance.  Note that every time this 
                     attribute is accessed, a new StreamWrapper is created.
                    """)

   def __getStderr(self):
      if not self.__proc: self.start()
      return OutputStreamWrapper(self, self.__proc.stderr, self.gotError)
   stderr = property(__getStderr, 
                    doc = """
                     The child process stderr stream.  This is an 
                     OutputStreamWrapper instance.  Note that every time this 
                     attribute is accessed, a new StreamWrapper is created.
                    """)

   def getRawStdin(self):
      if not self.__proc: self.start()
      return self.__proc.stdin

   def getRawStdout(self):
      if not self.__proc: self.start()
      return self.__proc.stdout

   def getRawStderr(self):
      if not self.__proc: self.start()
      return self.__proc.stderr

   def start(self):
      """
         Starts the child process.  Will raise an AssertionError if the
         process is already started.
      """
      assert not self.__proc
      self.__proc = \
         self.__procFact(self.__cmd, 
                         stdin = not self.__noStdIn and subprocess.PIPE or None,
                         stdout = not self.__noStdOut and subprocess.PIPE 
                           or None,
                         stderr = not self.__noStdErr and subprocess.PIPE 
                           or None,
                         )

   def run(self):
      """ 
         Runs the process and handles all input and output until termination.
         The process will be started if it has not already been.

         Returns the process' exit code.
      """
      if not self.__proc:
         self.start()

      # readable streams for our select loop
      readStreams = []

      # collect the child pipes
      stdin = stdout = stderr = None
      if not self.__noStdIn:
         stdin = self.__proc.stdin
      if not self.__noStdOut:
         stdout = self.__proc.stdout
         readStreams.append(stdout)
      if not self.__noStdErr:
         stderr = self.__proc.stderr
         readStreams.append(stderr)

      # process iteraction loop - handle all input & output
      while readStreams:
         if self.__inputData:
            writeStreams = [stdin]
         else:
            writeStreams = []

         rdx, wrx, erx = \
            select.select(readStreams, writeStreams, 
                          readStreams + writeStreams
                          )

         # XXX I think solaris routinely generates an error on termination,
         # might want to just terminate clean...
         if erx:
            raise IOError('error on child process stream')

         # process all output streams
         for src, func in ((stdout, self.gotOutput), (stderr, self.gotError)):
            if src in rdx:
               if not self.__handleRead(src, func):
                  # handleRead returns false when the stream is terminated.
                  # Remove it from the readStreams
                  readStreams.remove(src)

         # process standard input
         if wrx:
            self._handleWrite()

      # nothing left to read from ... wait for child process completion
      return self.__proc.wait()

   def write(self, data):
      """
         Writes data to the child process (actually, this queues the data.
         Write will be performed when the child is ready to read.
      """
      self.__inputData.append(data)
   
   def close(self):
      """
         Close the standard input stream.
      """
      self.__inputData.append(None)

   def __handleRead(self, src, func):

      # get data from the stream, if we got nothing, the stream is terminated
      data = src.read(4096)
      if not data:
         return False

      # pass it to the handler function
      func(data)

      return True

   def _handleWrite(self):
      """
         Write a single chunk of data from the input queue to the standard 
         input stream of the child process.
         
         Returns true if the input stream was closed during processing, false 
         if not.
      """
      item = self.__inputData.pop(0)
      stdin = self.__proc.stdin
      if item is None:
         stdin.close()
         return True
      stdin.write(item)
      stdin.flush()
      return False

   def gotOutput(self, data):
      """
         Derived classes should override this method to capture data received
         from the child's standard output stream.  Base class version just
         writes to our standard output.
      """
      sys.stdout.write(data)

   def gotError(self, data):
      """
         Derived classes should override this method to capture data received
         from the child's standard error stream.  Base class version just
         writes to our standard error.
      """
      sys.stderr.write(data)

   def wait(self):
      """
         Waits for process termination, returns the result code.
         
         This should not be called if the run() method is used, it should 
         always be called if the run method is not used.
      """
      return self.__proc.wait()

   def kill(self, signal = SIGTERM):
      """
         Sends a kill signal to the child process.
      """
      self.__proc.kill(signal)

class LineChildProcess(ChildProcess):
   """
      Processor for child processes to allow you to handle complete lines of
      output from stdout and stderr.  gotOutput() and gotError() are
      overriden to collect input into buffers and pass individual lines to
      gotOutLine() and gotErrLine().

      Note that this is only suitable for processes whose output and error
      streams produce output as finite lines of text terminated by the newline
      character.
   """

   def __init__(self, cmd, **kwargs):
      ChildProcess.__init__(self, cmd, **kwargs)
      self.__lastOutLine = ''
      self.__lastErrLine = ''

   def gotOutput(self, data):
      """
         Overrides @ChildProcess.gotOutput() to split output into single line
         chunks and feed them to @gotOutLine().
      """
      # split the data up into lines, process all but the last (the last can
      # not be assumed to be a complete line)
      lines = (self.__lastOutLine + data).split('\n')
      for line in lines[:-1]:
         self.gotOutLine(line)
      self.__lastOutLine = lines[-1]

   def gotOutLine(self, line):
      """
         Derived classes should implement this to capture single lines of
         output.  Base class version does nothing.
      """
      pass

   def gotError(self, data):
      """
         Overrides @ChildProcess.gotError() to split output into single line
         chunks and feed them to @gotOutLine().
      """
      # split the data up into lines, process all but the last (the last can
      # not be assumed to be a complete line)
      lines = (self.__lastErrLine + data).split('\n')
      for line in lines[:-1]:
         self.gotErrLine(line)
      self.__lastErrLine = lines[-1]

   def gotErrLine(self, data):
      """
         Derived classes should implement this to capture single lines of
         output.  Base class version does nothing.
      """
      pass
