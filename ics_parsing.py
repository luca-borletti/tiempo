from time import localtime
from datetime import *
from icalendar import *
# from ics import *

class event(object):
    def __init__(self, summary, startTime, endTime):
        self.summary = summary
        self.startTime = startTime
        self.endTime = endTime

    def __repr__(self):
        return f"{self.summary}. From {str(self.startTime)} to {str(self.endTime)}"

concepts = event("15-151 Discrete Mathematics", \
    datetime(2021, 11, 11, 13, 25), datetime(2021, 11, 11, 14, 15))

print(concepts)
    

###############################################################################
# notes about icalendar library
###############################################################################
def icalendarLibraryTests():
    calendarFile = open("/Users/lucaborletti/Desktop/tiempo/ics_files/lgborletti@gmail.com.ics", "r")

    calendarInstance = Calendar.from_ical(calendarFile.read())

    print(calendarInstance.walk("VEVENT")[50])

    print(calendarInstance.walk("VEVENT")[50]["DTSTART"].dt)

    print(type(calendarInstance.walk("VEVENT")[50]["RRULE"]))



icalendarLibraryTests()

###############################################################################
# !!!!!!DEPRECATED!!!!!! notes about ics library and classes for events and calendars
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


###############################################################################
# !!!!!!DEPRECATED!!!!!! code from ics website
###############################################################################

def icsLibraryStartCode():
    c = Calendar()
    # print(type(c))
    e = Event()
    e.name = "15-151"
    e.begin = datetime(2021, 11, 11, 9)
    e.duration = timedelta(0, 7200)

    # e.end = '2021-11-11 10:00:00'

    c.events.add(e)


    # [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
    with open('/Users/lucaborletti/Desktop/tiempo/ics_files/output.ics', 'w') as my_file:
        my_file.writelines(c)


###############################################################################
# !!!!!!DEPRECATED!!!!!! testing on google calendar
###############################################################################

def icsLibraryTesting():
    calendarFile = open("/Users/lucaborletti/Desktop/tiempo/ics_files/lgborletti@gmail.com.ics", "r")

    calendarInstance = Calendar(calendarFile.read())


    # ATTEMPT AT TIMELINE
    # timelineInstance = calendarInstance.timeline
    # print(timelineInstance.today())


    # ATTEMPT AT USING .DATE TO SIMPLIFY TODAY PROBLEM
    # today = datetime.today()
    # tomorrow = today.date() + timedelta(1)

    today = datetime(2021, 11, 11, tzinfo=timezone.utc)
    tomorrow = datetime(2021, 11, 12, tzinfo=timezone.utc)



    # for event in calendarInstance.events:
    #     start = event.begin
    #     stop = event.end

    #     if (start > today and stop < tomorrow):
    #         print(event)


    for event in calendarInstance.events:
        if event.name == '''Introduction to Psychology 85-102''':
            print(type(event.begin))
            # print(event.begin)
        # if event.begin > today:
        #     print(event)
        #     print("\n")
        #     print(event.begin)
            