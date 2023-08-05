#==============================================================================
#
#  $Id: ez.py 468 1999-05-23 17:56:40Z mike $
#
"""
   This module is for the truly lazy.  It defines classes and functions that
   use reflection in a vile and reprehensible manner in order to minimize key 
   strokes.
   
   Examples:
   
   {{
      # defining { 'a': 10, 'b': 20 } using keyword arguments
      d = D(a = 10, b = 20)
      
      # Creating an instance with attributes a = 10 and b = 20
      i = I(a = 10, b = 20)
   }}
   
"""
#
#  Copyright (C) 1999 Michael A. Muller
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
#  $Log: ez.py,v $
#  Revision 1.1  1999/05/23 17:56:40  mike
#  Shortcuts for the truly lazy.
#
#
#==============================================================================


def D(**kw):
   """
      This function returns its own keyword parameters.  
      
      It is very useful for creating a dictionary with minimal punctuation.
   """
   return kw

class I:
   """
      This class uses the keyword arguments of its constructor as its
      attributes.
   """   

   def __init__(self, **kw):
      for key, val in kw.items():
         setattr(self, key, val)

