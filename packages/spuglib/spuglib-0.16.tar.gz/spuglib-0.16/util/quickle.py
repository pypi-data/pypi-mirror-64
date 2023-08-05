#==============================================================================
#
#  $Id: quickle.py 550 2000-02-13 00:00:11Z mike $
#
"""
   Quick versions of pickle functions that allow you to dump to and load
   from a pickle file using the filename instead of a file object.
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
#  $Log: quickle.py,v $
#  Revision 1.4  2000/02/13 00:00:11  mike
#  Changed comments to docstrings.xs
#
#  Revision 1.3  1999/09/07 18:51:26  mike
#  Added the binary option when opening files so that Windows systems don't
#  add carriage returns.
#
#  Revision 1.2  1998/12/02 21:25:52  mike
#  Converted to cPickle module.
#
#  Revision 1.1  1998/10/22 23:44:37  mike
#  Initial revision
#
#
#==============================================================================

import cPickle

def load(name):
   "Load and return the first object in file named /name/."
   f = open(name, 'rb')
   return cPickle.load(f)

def dump(obj, name):
   "Dump /obj/ to a file named /name/."
   f = open(name, 'wb')
   cPickle.dump(obj, f)

