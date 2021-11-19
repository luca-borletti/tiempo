from cmu_112_graphics import *
from datetime import *
from random import *
from ics_parsing import *

def main():
    pass


def appStarted(app):
    '''
    for week mode
    '''

    ###########################################################################
    # calendar background
    ###########################################################################

    app.calendarLeftMargin = 100
    app.calendarTopMargin = 100
    
    app.calendarWidth = app.width
    app.calendarHeight = app.height

    app.calendarPixelHeight = app.calendarHeight - app.calendarTopMargin
    app.calendarPixelWidth = app.calendarWidth - app.calendarLeftMargin
    app.calendarBgColor = fromRGBtoHex((150,150,150))

    ###########################################################################
    # 
    ###########################################################################

    dateToday = datetime.now(tz = None)
    numDay = dateToday.isoweekday()
    lastSunday = dateToday - timedelta(days = (numDay))

    weekDays = []
    week = icalendarLibraryTests2()
    # for day in range(7):
    #     currDate = lastSunday + timedelta(days = day)
    #     weekDays.append(currDate)
    #     for event in week[currDate]:
    #         datetimeToCalendar(app, event, currDate)
    #         pass
    
    ###########################################################################
    # calendar event selection
    ###########################################################################
    
    app.selectedEvent = None
    app.deselectedColor = None
    app.selectedColor = None
    app.draggedPosition = None

def datetimeToCalendar(app, event, day):
    '''
    convert an event's startTime and stopTime into pixelTop and pixelBot 
    for use by the "view"
    '''
    event.day = day

    dayInSeconds = 86400

    event.pixelTop = app.calendarTopMargin + (event.startTime - \
        app.midnight).total_seconds()/dayInSeconds*app.calendarPixelHeight
    event.pixelBot = event.pixelTop + \
        event.duration.total_seconds()/dayInSeconds*app.calendarPixelHeight

    event.pixelLeft = app.calendarLeftMargin
    event.pixelRight = int(app.calendarWidth*.95)
    

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
    drawWeekBackground(app, canvas)

def drawWeekBackground(app, canvas):
    '''
    draw lines across calendar side of view
    draw hours text
    '''
    canvas.create_line(0, app.calendarTopMargin, \
        app.calendarWidth, app.calendarTopMargin, fill = "gray", width = .5)
    
    for day in range(7):
        canvas.create_line(app.calendarLeftMargin + app.calendarPixelWidth//7*day, 
            app.calendarTopMargin//2, app.calendarLeftMargin + app.calendarPixelWidth//7*day, 
            app.calendarHeight, fill = "gray", width = .5)
    for hour in range(1, 13):
        hourPixel = int(app.calendarPixelHeight/12)*hour + app.calendarTopMargin
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