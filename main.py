from cmu_112_graphics import *
from datetime import *
from random import * 

###############################################################################
# OOP for calendar
###############################################################################

class event(object):
    def __init__(self, summary, startTime, endTime):
        self.summary = summary
        self.startTime = startTime
        self.endTime = endTime
        self.duration = endTime - startTime
        self.color = (randrange(0, 256),
                      randrange(0, 256),
                      randrange(0, 256))
        self.pixelStart = None
        self.pixelEnd = None
        self.pixelWidth = None
        self.pixelHeight = None
        
    def __repr__(self):
        return f"{self.summary}. From {str(self.startTime)} to {str(self.endTime)}"


concepts = event("15-151 Discrete Mathematics", \
    datetime(2021, 11, 11, 13, 25, tzinfo=timezone.utc), \
        datetime(2021, 11, 11, 16, 15, tzinfo=timezone.utc))

# linear_algebra = event("21-241 Linear Algebra", \
#     datetime(2021, 11, 11, ), \
#         )



events = {concepts}

testEvent = datetime.now() # could be all events in one day

midnight = testEvent.replace(hour=0, minute=0, second=0, microsecond=0)

seconds_since_midnight = (testEvent - midnight).total_seconds()

sundayBeforeTestEvent = timedelta(days=((testEvent.isoweekday()) % 7))


# today = datetime(2021, 11, 11, tzinfo=timezone.utc)

# tomorrow = datetime(2021, 11, 12, tzinfo=timezone.utc)


# for event in events:
#     start = event.startTime
#     end = event.endTime
#     if (start > today and end < tomorrow):
#         print(event)



###############################################################################
# calendar graphics
###############################################################################

def appStarted(app):
    # separate into appstarted modes


    ###########################################################################
    # calendar background
    ###########################################################################

    app.calendarWidth = app.width//2

    app.calendarHeight = app.height

    app.calendarLeftMargin = 50

    app.calendarTopMargin = 100

    app.calendarBgColor = fromRGBtoHex((150,150,150))

    ###########################################################################
    # calendar events
    ###########################################################################
    
    app.eventWidth = app.calendarWidth - app.calendarLeftMargin

    app.today = datetime(2021, 11, 11, tzinfo=timezone.utc)

    app.eventsToday = {concepts}

    datetimeToCalendar(app)

    ###########################################################################
    # calendar event selection
    ###########################################################################

    
    app.selectedEvent = None
    
    app.deselectedColor = None

    app.selectedColor = None

    app.draggedPosition = None


def datetimeToCalendar(app):
    '''
    convert each event's startTime and stopTime into pixelStart and pixelEnd
    times for use by the "view"
    '''
    dayInSeconds = 86400
    calendarLength = app.calendarHeight - app.calendarTopMargin
    midnight = app.today.replace(hour=0, minute=0, second=0, microsecond=0)
    for event in app.eventsToday:
        event.pixelStart = app.calendarTopMargin + (event.startTime - \
            midnight).total_seconds()/dayInSeconds*calendarLength
        event.pixelEnd = event.pixelStart + \
            event.duration.total_seconds()/dayInSeconds*calendarLength
        event.pixelHeight = event.pixelStart - event.pixelEnd
        # event.pixelWidth = app.calendarWidth - app.calendarLeftMargin

def fromHextoRGB(hexString):
    '''
    convert a hex string to an rgb tuple using indexing and base conversion
    '''
    hexVals = [hexString[2*i+1: 2*(i+1)+1] for i in range(3)]
    rgbTuple = tuple(int(hexVals[i], 16) for i in range(3))
    return rgbTuple

def fromRGBtoHex(rgbTuple):
    '''
    convert an rgb tuple to a hex string using indexing and base conversion
    '''
    red, green, blue = rgbTuple
    hexString = f'#{red:02x}{green:02x}{blue:02x}' #CHANGE!!!!
    return hexString

def timerFired(app):
    pass

def appStopped(app):
    pass

def mousePressed(app, event):
    x, y = event.x, event.y
    if mouseInCalendar(app, x, y):
        if mouseOnButtons(app, x, y):
            pass
        else:
            selectedEvent = mouseOnEvent(app, x, y)
            if selectedEvent != None:
                selectEvent(app, selectedEvent)
                app.draggedPosition = (x, y)
            else:
                deselectEvent(app)

def mouseInCalendar(app, x, y):
    return (app.calendarLeftMargin <= x <= app.calendarWidth) and \
        (app.calendarTopMargin <= y <= app.height)

def mouseOnButtons(app, x, y):
    return False

def mouseOnEvent(app, x, y):
    for event in app.eventsToday:
        if (app.calendarLeftMargin <= x <= app.calendarWidth) and \
            (event.pixelStart <= y <= event.pixelEnd):
            return event
    return None

def selectEvent(app, event):
    app.deselectedColor = event.color
    app.selectedColor = fromRGBtoHex(tuple([app.deselectedColor[i]//4*3 for i in range(3)]))
    event.color = app.selectedColor
    app.selectedEvent = event

    app.eventsToday.remove(event)

def deselectEvent(app):
    event = app.selectedEvent

    if app.selectedEvent != None:
        event.color = app.deselectedColor
        app.eventsToday.add(event)
    
    app.selectedEvent = None
    app.deselectedColor = None
    app.selectedColor = None
    app.draggedPosition = None

def mouseDragged(app, event):
    x, y = event.x, event.y

    if app.selectedEvent != None:
        app.draggedPosition = (x, y)


# goal: get snapping to grid implemented in the daily calendar………
# as well as writing new files when click export………
# and pseudo-randomness for color generation



# def mouseReleased(app, event):
#     x, y = event.x, event.y

#     if app.selectedEvent != None:
#         # app.selectedEvent.color = app.deselectedColor
#         height = app.selectedEvent.pixelEnd - app.selectedEvent.pixelStart
#         if mouseInCalendar(app, x, y) and (mouseOnEvent(app, x, y) == None)\
#             and (height//2 + app.calendarTopMargin <= y):
#             #CHANGE actually modify datetime; make datetimeToCalendar not iterate
            
#             app.selectedEvent.pixelStart = y


def keyReleased(app, event):
    pass

def keyPressed(app, event):
    pass

def sizeChanged(app):
    pass

def mouseMoved(app, event):
    pass

def sizeChanged(app):
    pass

def redrawAll(app, canvas):
    drawCalendar(app, canvas)

def drawCalendar(app, canvas):
    drawDayBackground(app, canvas)
    drawDayEvents(app, canvas)
    drawDraggedEvent(app, canvas)

def drawDayBackground(app, canvas):
    '''
    draw background of calendar
    '''
    canvas.create_rectangle(app.calendarLeftMargin,
                            app.calendarTopMargin,
                            app.calendarWidth,
                            app.calendarHeight,
                            fill = app.calendarBgColor,
                            width = 0)

def drawDayEvents(app, canvas):
    '''
    draw each event using pixelStart/Stop values in event instances as well
    as using pixelStart and anchoring
    '''
    for event in app.eventsToday:
        canvas.create_rectangle(app.calendarLeftMargin, event.pixelStart, 
                                app.calendarWidth, event.pixelEnd, 
                                fill = fromRGBtoHex(event.color),
                                width = 0)

        canvas.create_text(app.calendarLeftMargin, event.pixelStart, 
                           text = event.summary, anchor = "nw",
                           fill = "black")

def drawDraggedEvent(app, canvas):
    event = app.selectedEvent
    if event != None:
        x, y = app.draggedPosition
        eventHeight = event.pixelEnd - event.pixelStart
        canvas.create_rectangle(app.calendarLeftMargin, y - eventHeight//2, 
                                app.calendarWidth, y + eventHeight//2, 
                                fill = event.color,
                                width = 0)
        canvas.create_text(app.calendarLeftMargin, y - eventHeight//2, 
                           text = event.summary, anchor = "nw",
                           fill = "black")


runApp(width=750, height=750)