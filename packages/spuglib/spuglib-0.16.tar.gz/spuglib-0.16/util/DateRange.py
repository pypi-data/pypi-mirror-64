#==============================================================================
#
#  $Id: DateRange.py 678 2000-05-14 18:44:35Z mike $
#
"""
   Class representing a date range.
   
   A DateRange is created using two dates and can be used to make 
   determinations about dates within the range.
   
   Synopsis:
   
   {{
      r0 = DateRange(Date(stdfmt = '2/12/98'), Date(stdfmt = '3/13/99'))
      
      # see if a date range includes a particular date
      if r0.includes(Date(stdfmt = '12/1/98')):
         print 'yup'
      
      # see if the range overlaps with another data range
      if r0.overlap(DateRange(Date(stdfmt = '12/1/98'),
                              Date(stdfmt = '1/1/2000')
                              )
                    ):
         print 'double-yup'
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
#  $Log: DateRange.py,v $
#  Revision 1.6  2000/05/14 18:44:35  mike
#  Fixed comparison in union method.
#
#  Revision 1.5  2000/02/13 21:58:52  mike
#  Doc fixes.
#
#  Revision 1.4  2000/02/12 23:59:33  mike
#  Fixed comments; fixed bug in overlap() method.
#
#  Revision 1.3  1998/11/08 01:15:49  mike
#  Changed the semantics of the includes() method to be inline with the
#  spirit of a DateRange - now returns true if the date in question is
#  greater than or equal to the start date, and strictly less than the end
#  date.
#
#  Revision 1.2  1998/10/23 00:50:26  mike
#  Added header
#
#
#==============================================================================

from Date import Date

class DateRange:
   """
      A date range is a period in time.  By default, a date range begins with
      negative infinity and ends with infinity.
   """   
   
   def __init__(self, 
                startDate = Date(foreverPast = 1), 
                endDate = Date(foreverFuture = 1)):
      """
         Constructs a date range.  By default, the start date is the
	 bottomless past and the end date is the endless future.  This
	 allows us to define date ranges from a given point to the end of
	 time, or from the beginning of time to a given point.
      """
      self.start = startDate
      self.end = endDate

   def setStart(self, start):
      "Resets the start Date."
      self.start = start
   
   def setEnd(self, end):
      "Resets the end Date."
      self.end = end

   def getStart(self):
      "Returns the start date."
      return self.start
   
   def getEnd(self):
      "Returns the end date."
      return self.end

   def union(self, other):
      """
         Returns a date range that is the union of the periods defined by
         self and other, or None if the two periods do not overlap.
      """
      
      if other.end >= self.start and other.start <= self.end:
      
         # latest start date marks the beginning of the union
         if other.start > self.start:
            start = other.start
         else:
            start = self.start
         
         if other.end < self.end:
            return DateRange(start, other.end)
         else:
            return DateRange(start, self.end)
      else:
         return None

   def overlap(self, other):
      """
         Returns true if the receiver date range overlaps with the /other/ date
         range.
      """
      return other.end >= self.start and \
         other.start <= self.end and \
         not self.alignedWith(other)

   def includes(self, date):
      """
         Returns true if the date range includes the given date.  In keeping
	 with the spirit of date ranges, inclusion is defined as being
	 greater than or equal to the start date but less than the end date.
      """
      return date >= self.start and date < self.end

   def alignedWith(self, other):
      """
         Returns true if the records are "aligned" - that is, if the start
         date of one matches the end date of the other.
      """
      return self.start == other.end or self.end == other.start

   def __cmp__(self, other):
      """
         Compares the start date of two date ranges.  If the two date ranges
	 have the same start date, compares the end date.
      """
      return self.start.__cmp__(other.start) or self.end.__cmp__(other.end)
   
   def __str__(self):
      """
         Formats the receiver as a string (two new standard format dates
         seperated by a dash.
      """
      return self.start.formatNewStd() + '-' + self.end.formatNewStd()
