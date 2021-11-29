from time import localtime
from datetime import *
from icalendar import *
from pytz import *
from random import *

###############################################################################
# notes about icalendar library
###############################################################################
def icalendarLibraryTests():
    calendarFile = open("lgborletti@gmail.com.ics", "r")

    calendarInstance = Calendar.from_ical(calendarFile.read())


    eventIndex = 20

    vEvent = calendarInstance.walk("VEVENT")[eventIndex]
    # print(vEvent)
    # print("VEVENT" in vEvent)

    # print(.date())
    for i in vEvent:
        print(i)

    print(calendarInstance.walk("VEVENT")[50]["DESCRIPTION"])

    # vRecur = calendarInstance.walk("VEVENT")[eventIndex]["RRULE"]

    # for i in (vRecur):
    #     print(i)
    #     print(vRecur[i])
    #     print("\n")


class calendarEvent(object):
    def __init__(self, summary, startTime, endTime):
        self.summary = summary
        self.startTime = startTime
        self.endTime = endTime
        self.duration = endTime - startTime
        self.day = None
        self.color = None
        self.pixelTop = None
        self.pixelBot = None
        self.pixelLeft = None
        self.pixelRight = None
        
    def __repr__(self):
        return f"{self.summary}. From {str(self.startTime)} to {str(self.endTime)}"

# icalendarLibraryTests()

def icalendarLibraryTests2():



    '''
    MONTH APPROACH
    '''

    # dateToday = date.today()
    # dateFirstDayOfMonth = dateToday - timedelta(days = dateToday.day - 1)
    # month = {}

    # numDays = 30
    # for i in range(numDays):
    #     currDate = dateFirstDayOfMonth + timedelta(days = i)
    #     month[currDate] = set()

    '''
    WEEK APPROACH (temporary)
    '''

    tz = timezone("America/New_York")
    dateToday = datetime.now(tz = tz)

    numDay = dateToday.isoweekday()%7
    lastSunday = dateToday - timedelta(days = (numDay))
    nextSunday = lastSunday + timedelta(days = 7)

    week = {}
    for weekDay in range(7):
        currDate = lastSunday + timedelta(days = weekDay)
        currDate = currDate.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo = None)
        week[currDate] = set()

    calendarFile = open("lgborletti@gmail.com.ics", "r")
    calendarInstance = Calendar.from_ical(calendarFile.read())
    
    events = {}
    eventIndex = 40
    vEvent = calendarInstance.walk("VEVENT")[eventIndex]
    startTime = vEvent["DTSTART"].dt.replace(tzinfo=None)
    endTime =  vEvent["DTEND"].dt.replace(tzinfo=None)
    time = startTime.time()

    # print(datetime.now(tz = None).replace(hour = time.hour, minute = time.minute, second = time.second, microsecond=0))
    # print(endTime)
    # print(repr(str(vEvent["SUMMARY"])))

    # print(vEvent["SUMMARY"])
    # dtstart = vEvent["DTSTART"].dt
    # print(dtstart.tzinfo)
    # print(dtstart)
    # print(datetime(2021, 8, 24, 12, 20, tzinfo = dateToday.tzinfo))
    # print(dtstart < datetime(2021, 8, 24, 12, 20, tzinfo = dateToday.tzinfo))

    # print(dateToday.tzinfo)
    # print(vEvent["DTEND"].dt)


    # print(vEvent["RRULE"]["UNTIL"][0])
    
    # for i in vEvent:
    #     print(i)

    # for event in calendarInstance.walk("VEVENT"):
    #     description = event["SUMMARY"]
    #     events[description] = event
    
    daysToNums = vWeekday.week_days
    colorIndex = 0
    colorList = [(81, 171, 242), (191, 120, 218), (167, 143, 108), (107, 212, 95), (248, 215, 74), (240, 154, 55), (234, 66, 106), (242, 171, 207)]

    for event in calendarInstance.walk("VEVENT"):
        if "RRULE" in event and "BYDAY" in event["RRULE"]:
            recurrenceList = event["RRULE"]
            if not "UNTIL" in recurrenceList or \
                recurrenceList["UNTIL"][0] > lastSunday:
                colorIndex += 1

                repeatingDays = set()
                for byDay in recurrenceList["BYDAY"]:
                    repeatingDays.add(daysToNums[byDay])
                # color = (min(randrange(0, 256) + 50, 255),
                #          min(randrange(0, 256) + 50, 255),
                #          min(randrange(0, 256) + 50, 255))
                # color = (randrange(0, 256)*7//8,
                #          randrange(0, 256)*7//8,
                #          randrange(0, 256)*7//8)
                color = colorList[colorIndex%len(colorList)]
                for day in week:
                    if day.isoweekday()%7 in repeatingDays:
                        startTime = event["DTSTART"].dt
                        endTime =  event["DTEND"].dt
                        startTime = startTime.replace(day = day.day, month = day.month, year = day.year, tzinfo = None)
                        endTime = endTime.replace(day = day.day, month = day.month, year = day.year, tzinfo = None)
                        eventObject = calendarEvent(str(event["SUMMARY"]), startTime, endTime)
                        eventObject.color = color
                        week[day].add(eventObject)
                        test = eventObject


    # for i in week:
    #     print(week[i])
    #     print('\n')

    return week
                

            # print(event["SUMMARY"])
            # for item in event["RRULE"]:
            #     print(item)
            # if "UNTIL" in event["RRULE"]:
            #     print(event["RRULE"]["UNTIL"])
            # print("\n")
# icalendarLibraryTests2()
'''


establish current date (for use in month/day)

create a dictionary with keys as string of each day in the month (taken from
date objects) assigned to sets containing events in that day (*)

most recent sunday, etc. (do so by DAY -> NUM and then …
    DATE minus NUM)


(*) create a set with all of our events
    for event in our list of events
        if there is an rrule
            remove it from set and add it to rrule set (**)
        else
            check if it is in the month

(**) now with rrules
    if until < 'beginning of month':
        remove from set
    now check frequency:
        if weekly
            check byday number
            if byday number of first day
        else (check daily… for now remove from set)


'''

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
            