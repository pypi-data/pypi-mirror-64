#==============================================================================
#
#  $Id: Date.py 1055 2006-08-23 23:05:47Z mike $
#
"""
   Simple Date class.
   
   Synopsis:
   
   {{
      # get the current date
      d = Date()
      d = Date(now = 1)
      
      # get 2/12/1999
      d = Date(year = 1999, month = 2, day = 12)
      
      # get 2/12/1999 from a string
      d = Date(stdfmt = '2/12/99')
      d = Date(stdfmt = '2/12/1999')
      
      # get a date from the current timeval
      d = Date(time = time.time())
      
      # get a date infinitely far in the future or past
      d = Date(foreverPast = 1)
      d = Date(foreverFuture = 1)
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
#  $Log: Date.py,v $
#  Revision 1.7  2000/05/16 01:01:56  mike
#  Moved private __toTime() to protected _toTime() so that DateTime could
#  override.
#
#  Revision 1.6  2000/02/13 21:58:52  mike
#  Doc fixes.
#
#  Revision 1.5  1999/08/12 19:00:12  mike
#  Fixed date math AGAIN.  Hopefully correctly, this time.
#
#  Revision 1.4  1999/07/02 15:33:07  mike
#  Converted internal representation from localtime to YMD
#
#  Revision 1.3  1999/05/04 21:39:57  mike
#  Fixed documentation; fixed bug which caused adding and subtracting days
#  accross daylight savings time boundaries to yield the wrong time.
#
#  Revision 1.2  1998/10/23 00:50:26  mike
#  Added header
#
#
#==============================================================================

import string, re, time
from types import IntType, FloatType

_time = time

_dateFmt = re.compile(r'(\d{1,2})/(\d{1,2})/((\d\d)?\d\d)')

# really should be a MAXFLOAT somewhere, but I couldn't find one
MAXFLOAT = 1.7976e+308
MINFLOAT = -MAXFLOAT

class DateParseError(Exception):
   """
      Exception thrown when date is of bad format
   """
   pass

def _parseStd(date):
   """
      Parse a `mm/dd/yy` or `mm/dd/yyyy` format year.  Takes best guess at
      century. returns a year, month, day tuple.
   """

   # parse the date with the regular expression and make sure that it is
   # correct
   match = _dateFmt.match(date)
   if not match:
      raise DateParseError('Date ' + date + ' is of bad format.  Format must ' +
                            'be mm/dd/yy or mm/dd/yyyy.'
                           )
   
   month = int(match.group(1))
   day = int(match.group(2))
   year = match.group(3)
   
   # for a two digit year, we have to figure out which is the most likely
   # century
   if len(year) == 2:
      year = int(year)
      
      # get the current year and century
      curYear = time.localtime(time.time())[0]
      century = curYear - curYear % 100
      
      # if adding the year to the current century puts us more than 50 years
      # before the current year, use the next century
      if year + century < curYear - 50:
         year = year + century + 100
      
      # if adding the year to the current centure puts us more than 50 years
      # ahead of the current year, use the previous century
      elif year + century > curYear + 50:
         year = year + century - 100
      
      else:
         year = year + century
   
   else:
      year = int(year)
   
   return year, month, day

class Date:
   """
      A date may be any date (including forever into the past and forever into
      the future).
      
      A date is assumed to be immutable - multiple entities may safely refer
      to the same date.  For this reason, there are no "set" methods.
      
      Public data members:
      /time/::
          Internal representation of the date - seconds since the beginning of
          the epoch.  *Don't modify this.*
          
          This attribute used to contain the internal representation, but now
          it is a _pseudo-attribute_: it is computed upon demand.
          
      This class includes a number of class variables for symbolic constants:
      *sunday*, *monday*, *tuesday*, *wednesday*, *thursday*, *friday*, 
      *saturday*, *january*, *february*, *march*, *april*, *may*, *june*, 
      *july*, *august*, *september*, *october*, *november*, *december*.
   """

   # nice symbolic form for weekdays and months
   
   sunday = 0
   monday = 1
   tuesday = 2
   wednesday = 3
   thursday = 4
   friday = 5
   saturday = 6

   january = 1
   february = 2
   march = 3
   april = 4
   may = 5
   june = 6
   july = 7
   august = 8
   september = 9
   october = 10
   november = 11
   december = 12

   __FOREVER_PAST = -1.0, 0, 0
   __FOREVER_FUTURE = MAXFLOAT, 0, 0

   def _toTime(self):
      """
         Returns the localtime representation of the date.
      """
      return time.mktime((self.__year, self.__month, self.__day, 
                          0, 0, 0, 0, 0, 0
                          )
                         )

   def __timeToDate(self, t):
      """
         Returns a `year/month/day` tuple for the localtime represented by /t/.
      """
      dateinfo = time.localtime(t)
      return dateinfo[0], dateinfo[1], dateinfo[2]
   
   def __currentDate(self):
      """
         returns the current date, which is the current time truncated of all
         precision greater than the day.
      """
      return self.__timeToDate(time.time())

   def __init__(self, time = 0, stdfmt = "", other = None, year = 0, 
                month = 0, day = 0, foreverPast = 0, foreverFuture = 0, 
                now = 0
                ):
      if stdfmt:
         self.__year, self.__month, self.__day = _parseStd(stdfmt)
      elif year:
         self.__year = year
         self.__month = month
         self.__day = day
         
      elif other:
         self.__year = other.__year
         self.__month = other.__month
         self.__day = other.__day
      elif time:
         self.__year, self.__month, self.__day = self.__timeToDate(time)
      elif foreverPast:
         self.__year, self.__month, self.__day = self.__FOREVER_PAST
      elif foreverFuture:
         self.__year, self.__month, self.__day = self.__FOREVER_FUTURE
      else:
         # use the current date, exclude info more precise than day
         self.__year, self.__month, self.__day = self.__currentDate()

   def ymd(self):
      """
         Returns a tuple consisting of the year, month, and day.
      """
      return (self.__year, self.__month, self.__day)
   
   def formatStd(self):
      """
         Returns a string consisting of the receiver formatted as `mm/dd/yy`
      """
      return '%02d/%02d/%02d' % (self.__month, self.__day, self.__year % 100)

   def formatNewStd(self):
      """
         Returns a string consisting of the receiver formatted as `mm/dd/yyyy`
      """
      return '%02d/%02d/%04d' % (self.__month, self.__day, self.__year)

   def formatShort(self):
      """
         Returns a string consisting of the receiver formatted as mmddyy
      """
      return '%02d%02d%02d' % (self.__month, self.__day, self.__year)
   
   def getMonth(self):
      """
         Returns the month
      """
      return self.__month

   def getYear(self):
      """
         Returns the year.
      """
      return self.__year
   
   def getDay(self):
      """
         Returns the day of the month.
      """
      return self.__day

   def getDayOfWeek(self):
      """
         Returns the current day of the week as a number.
      """
      return int(self.format('%w'))

   def __cmp__(self, other):
      """
         Allows us to use the comparison operators on dates.
      """
      return cmp(self.__year, other.__year) or \
         cmp(self.__month, other.__month) or \
         cmp(self.__day, other.__day)
   
   def __str__(self):
      """
         Returns the date formatted in the new standard format.
      """
      return self.formatNewStd()
   
   def format(self, formatStr):
      """
         Returns the date and time formated using the strftime function.
      """
      return time.strftime(formatStr, time.localtime(self._toTime()))

   def last(self, weekday):
      """
         Returns a new date which is the given /weekday/ immediately prior to
         the date of /self/.  If /self/s date falls on that weekday, returns
         a copy of /self/.
      """
      curWeekday = self.getDayOfWeek()
      if curWeekday < weekday:
         curWeekday = curWeekday + 7
      return self - (curWeekday - weekday)
   
   def next(self, weekday):
      """
         Returns a new date which is the given /weekday/ following the date of 
         /self/.  If /self/s date falls on that weekday, returns a copy of /self/.
      """
      curWeekday = self.getDayOfWeek()
      if weekday < curWeekday:
         weekday = weekday + 7
      return self + (weekday - curWeekday)

   def dst(self):
      """
         Returns true if daylight savings time is in effect for this date,
         false if not.
      """
      return time.localtime(self._toTime())[-1]

   def __sub__(self, other):
      """
         Returns the difference (in days) between two dates.  A day is assumed
         to be 86400 seconds.
         
         If /other/ is not a date, but is a number, a new date is returned that
         is /other/ days before /self/.
      """
      if type(other) in (IntType, FloatType):
         mytime = self._toTime()
         date = Date(time = mytime - other * 86400)
         dst = self.dst() - date.dst() 
         if dst:
            date = Date(time = mytime - other * 86400 + dst * 3600)
         return date
      elif isinstance(other, Date):
         dst = (self.dst() - other.dst()) * 3600
         return int((self._toTime() - other._toTime() + dst) / 86400)

   def __add__(self, days):
      """
         Returns a new date consisting of the given date plus /days/.
      """
      mytime = self._toTime()
      date = Date(time = mytime + days * 86400)
      dst = self.dst() - date.dst()
      if dst:
         date = Date(time = mytime + days * 86400 + dst * 3600)
      return date

   def __getattr__(self, attr):
      """
         Provides the transparent computation of the time attribute.
      """
      if attr == 'time':
         return self._toTime()
      else:
         raise AttributeError(attr)
   
   def __setstate__(self, dict):
      """
         Allows conversion from old-style representation.
      """
      if dict.has_key('time'):
         t = dict['time']
         if t == MINFLOAT:
            self.__year, self.__month, self.__day = self.__FOREVER_PAST
         elif t == MAXFLOAT:
            self.__year, self.__month, self.__day = self.__FOREVER_FUTURE 
         else:
            self.__year, self.__month, self.__day = \
               self.__timeToDate(dict['time'])
      else:
         self.__dict__.update(dict)

