from ics import *
from datetime import *

###############################################################################
# notes about ics library and classes for events and calendars
###############################################################################

# def begin(self) -> Arrow:
#     """Get or set the beginning of the event.
#     |  Will return an :class:`Arrow` object.
#     |  May be set to anything that :func:`Arrow.get` understands.
#     |  If an end is defined (not a duration), .begin must not
#         be set to a superior value.
#     """
#     return self._begin

# def make_all_day(self) -> None:
#     """Transforms self to an all-day event.
#     The event will span all the days from the begin to the end day.
#     """
#     if self.all_day:
#         # Do nothing if we already are a all day event
#         return
#     begin_day = self.begin.floor('day')
#     end_day = self.end.floor('day')
#     self._begin = begin_day
#     # for a one day event, we don't need a _end_time
#     if begin_day == end_day:
#         self._end_time = None
#     else:
#         self._end_time = end_day + timedelta(days=1)
#     self._duration = None
#     self._begin_precision = 'day'

# def clone(self):
#     """
#     Returns:
#         Event: an exact copy of self"""
#     clone = copy.copy(self)
#     clone.extra = clone.extra.clone()
#     clone.alarms = copy.copy(self.alarms)
#     clone.categories = copy.copy(self.categories)
#     return clone


c = Calendar()
# print(type(c))
e = Event()
e.name = "15-151"
e.begin = datetime(2021, 11, 11, 9)
e.duration = timedelta(0, 7200)
# e.end = '2021-11-11 10:00:00'
c.events.add(e)
c.events
print(c)
# [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
with open('/Users/lucaborletti/Desktop/tiempo/ics_files/output.ics', 'w') as my_file:
    my_file.writelines(c)

# and it's done !