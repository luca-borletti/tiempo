from cmu_112_graphics import *
from datetime import *
from random import *
from ics_parsing import icalendarLibraryTests2

###############################################################################
# OOP for calendar
###############################################################################
seed(15)

# class event(object):
#     def __init__(self, summary, startTime, endTime):
#         self.summary = summary
#         self.startTime = startTime
#         self.endTime = endTime
#         self.duration = endTime - startTime
#         self.color = (randrange(0, 256),
#                       randrange(0, 256),
#                       randrange(0, 256))
#         self.pixelTop = None
#         self.pixelBot = None
#         self.pixelLeft = None
#         self.pixelRight = None

        
#     def __repr__(self):
#         return f"{self.summary}. From {str(self.startTime)} to {str(self.endTime)}"

_week = icalendarLibraryTests2()

index = 0 
for day in _week:
        _day = _week[day]
        index += 1
        if index > 4:
            break

# concepts = event("15-151 Discrete Mathematics", \
#     datetime(2021, 11, 11, 13, 25, tzinfo=timezone.utc), \
#         datetime(2021, 11, 11, 16, 15, tzinfo=timezone.utc))

# linear_algebra = event("21-241 Linear Algebra", \
#     datetime(2021, 11, 11, 17, 5, tzinfo=timezone.utc), \
#         datetime(2021, 11, 11, 19, 55, tzinfo=timezone.utc))

###############################################################################
# calendar graphics
###############################################################################

def appStarted(app):
    # separate into appstarted modes
    ###########################################################################
    # calendar background
    ###########################################################################

    app.calendarWidth = app.width

    app.calendarHeight = app.height

    app.calendarDayWidth = 100

    app.calendarLeftMargin = 100

    app.calendarTopMargin = 100

    app.calendarLength = app.calendarHeight - app.calendarTopMargin

    app.calendarBgColor = fromRGBtoHex((150,150,150))

    ###########################################################################
    # calendar events
    ###########################################################################

    # CHANGE midnight time finder

    app.today = datetime(2021, 11, 18, tzinfo=timezone.utc)

    app.midnight = app.today.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo = None)

    # app.eventsToday = {concepts, linear_algebra}

    app.eventsToday = _day

    for event in app.eventsToday:
        datetimeToCalendar(app, event)
 
    ###########################################################################
    # calendar event selection
    ###########################################################################
    
    app.selectedEvent = None
    
    app.deselectedColor = None

    app.selectedColor = None

    app.draggedPosition = None


    ###########################################################################
    # TESTING
    ###########################################################################

    app.timerDelay = 1000


def datetimeToCalendar(app, event):
    '''
    convert an event's startTime and stopTime into pixelTop and pixelBot 
    for use by the "view"
    '''
    dayInSeconds = 86400

    event.pixelTop = app.calendarTopMargin + (event.startTime - \
        app.midnight).total_seconds()/dayInSeconds*app.calendarLength
    event.pixelBot = event.pixelTop + \
        event.duration.total_seconds()/dayInSeconds*app.calendarLength

    event.pixelLeft = app.calendarLeftMargin
    event.pixelRight = int(app.calendarWidth*.95)

# def calendarToDatetime(app, event):
#     '''
#     convert an event's pixelTop and pixelBot to startTime and stopTime
#     for use by backend
#     '''
#     event.startTime = 

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
    '''
    check where mouse is on view
        - if on event, select event
        - if on calendar and an event is selected, deselect the event.
    '''
    x, y = event.x, event.y
    if mouseInCalendar(app, x, y):
        if mouseOnButtons(app, x, y):
            deselectEvent(app)
            pass
        else:
            clickedEvent = mouseOnEvent(app, x, y)
            if clickedEvent != None:
                deselectEvent(app)
                selectEvent(app, clickedEvent)
                app.draggedPosition = (x, y)
            else:
                deselectEvent(app)
    else:
        deselectEvent(app)

def mouseInCalendar(app, x, y):
    '''
    return True if mouse is in calendar portion of the view
    return False otherwise
    '''
    return (app.calendarLeftMargin <= x <= app.calendarWidth) and \
        (app.calendarTopMargin <= y <= app.height)

def mouseOnButtons(app, x, y):
    '''
    return True if mouse is on a button in view
    return False otherwise
    '''
    return False

def mouseOnEvent(app, x, y):
    '''
    return the event if mouse is on an event
    return None otherwise
    '''
    for event in app.eventsToday:
        if (event.pixelLeft <= x <= event.pixelRight) and \
            (event.pixelTop <= y <= event.pixelBot):
            return event
    return None

def selectEvent(app, event):
    '''
    - store the color of an event before selection
    - create darker "highlighted" new selected color and make it event's color 
    - remove from events set
    '''
    app.deselectedColor = event.color
    app.selectedColor = tuple([app.deselectedColor[i]//4*3 for i in range(3)])
    event.color = app.selectedColor
    app.selectedEvent = event

    app.eventsToday.remove(event)

def deselectEvent(app):
    '''
    if there is a selected event
        - change color back to lighter color
    '''
    event = app.selectedEvent

    if event != None:
        app.eventsToday.remove(event)
        event.color = app.deselectedColor
        app.eventsToday.add(event)
    
    app.selectedEvent = None
    app.deselectedColor = None
    app.selectedColor = None
    app.draggedPosition = None

def fixEvent(app, event, x, y):
    '''
    changes the attributes of an event to match the given x, y coordinates
    of the mouse
    '''
    height = event.pixelBot - event.pixelTop
    if y - height//2 < app.calendarTopMargin:
        event.pixelTop = app.calendarTopMargin
        event.pixelBot = app.calendarTopMargin + height
    elif y + height//2 > app.calendarHeight:
        event.pixelBot = app.calendarHeight
        event.pixelTop = app.calendarHeight - height
    else:
        event.pixelTop = y - height//2
        event.pixelBot = y + height//2

    # calendarToDatetime(app, event)

    app.eventsToday.add(event)

def mouseDragged(app, event):
    '''
    if an event is selected, then change dragged position (where dragged event
    will be drawn)
    '''
    x, y = event.x, event.y

    if app.selectedEvent != None:
        app.draggedPosition = (x, y)

def mouseReleased(app, event):
    '''
    if an event is selected, then the selected event is fixed at the x, y 
    position
    '''
    x, y = event.x, event.y

    if app.selectedEvent != None:
        app.draggedPosition = (x, y)

        fixEvent(app, app.selectedEvent, x, y)

        app.draggedPosition = None

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
    drawOverlapTest(app, canvas)

def drawOverlapTest(app, canvas):
    '''
    
    '''
    for event in app.eventsToday:
        for other in app.eventsToday:
            if event != other: #CHANGE byday?!?!?!
                if (other.pixelTop < event.pixelTop and \
                    event.pixelTop < other.pixelBot) or \
                    (other.pixelTop < event.pixelBot and \
                    event.pixelBot < other.pixelBot):
                    canvas.create_oval(app.width//2 - 10, app.height//2 - 10, \
                        app.width//2 + 10, app.height//2 + 10, fill = "red")

def drawDraggedEvent(app, canvas):
    '''
    draws the dragged event within bounds of calendar but following the
    position of the mouse during dragging
    '''
    event = app.selectedEvent
    if app.draggedPosition != None:
        x, y = app.draggedPosition
        eventHeight = event.pixelBot - event.pixelTop #CHANGE if slow

        #CHANGE optimize
        if y - eventHeight//2 < app.calendarTopMargin:
            y = app.calendarTopMargin + eventHeight//2
        elif y + eventHeight//2 > app.calendarHeight:
            y = app.calendarHeight - eventHeight//2
        
        canvas.create_rectangle(app.calendarLeftMargin, y - eventHeight//2, 
                                app.calendarWidth, y + eventHeight//2, 
                                fill = fromRGBtoHex(event.color),
                                width = 0)
        canvas.create_text(app.calendarLeftMargin, y - eventHeight//2, 
                           text = event.summary, anchor = "nw",
                           fill = "white", font = "Arial 15")

def drawDayEvents(app, canvas):
    '''
    draw each event using pixelTop/End values in event instances as well
    as using pixelTop and anchoring
    '''
    for event in app.eventsToday:
        canvas.create_rectangle(event.pixelLeft, event.pixelTop, 
                                event.pixelRight, event.pixelBot, 
                                fill = fromRGBtoHex(event.color),
                                width = 0)

        canvas.create_text(event.pixelLeft, event.pixelTop, 
                           text = event.summary, anchor = "nw",
                           fill = "white", font = "Arial 15")

def drawDayBackground(app, canvas):
    '''
    draw lines across calendar side of view
    draw hours text
    '''
    canvas.create_line(0, app.calendarTopMargin, \
        app.calendarWidth, app.calendarTopMargin, fill = "gray", width = .5)
    canvas.create_line(app.calendarLeftMargin, app.calendarTopMargin//2, \
        app.calendarLeftMargin, app.calendarHeight, fill = "gray", width = .5)
    for hour in range(1, 13):
        hourPixel = int(app.calendarLength/12)*hour + app.calendarTopMargin
        canvas.create_line(app.calendarLeftMargin//2, hourPixel, \
            app.calendarWidth, hourPixel, fill = "gray", width = .5)
        
        if hour < 6: 
            hourText = f"{2*hour} AM"
        else:
            hourText = f"{2*hour} PM"
        canvas.create_text(app.calendarLeftMargin//4, hourPixel, \
            text = hourText, fill = "gray", font = "Arial 11")


if __name__ == "__main__":
    runApp(width=1000, height=800)