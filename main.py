from cmu_112_graphics import *
from datetime import *
from random import *
from ics_parsing import *

'''
implement…

event creation

event description pop-up

interleaving algorithm plan

scrolling
'''

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

def main():
    pass


def appStarted(app):
    '''
    for week mode
    '''


    # openingMode, calendarMode, eventCreationMode, taskCreationMode, pomodoroMode

    app.mode = "calendarMode"
    # url = "https://lh3.googleusercontent.com/proxy/XFVcPr1-SZFLA58dSI5X3dSQhZLELv9CtgkU6Xo3ufSy4CVXu8vd2mY5sZphzvjhkoV4wguChnjWj2DADDcytPesoWkUl6vQk7uRZm_nzUp7I25qhtC_s338fdjB4LYCdntsRDM6zjY5PU-GiV0kcliZ8Y2nhSR3TwYJFEi_zlEbH2TRs7xnjaLNeOIEcbJqQqq1xkU"
    # app.openingModeImage = app.loadImage(url)


    ###########################################################################
    # calendar background
    ###########################################################################

    app.calendarLeftMargin = 100
    app.calendarTopMargin = 100
    
    app.calendarEditMargin = 10

    app.calendarWidth = app.width
    app.calendarHeight = app.height

    app.calendarPixelHeight = app.calendarHeight - app.calendarTopMargin
    app.calendarPixelWidth = app.calendarWidth - app.calendarLeftMargin

    app.calendarBgColor = fromRGBtoHex((30,32,35))
    app.calendarFgColor = fromRGBtoHex((70,70,70))
    app.calendarWkndColor = fromRGBtoHex((39,40,42))
    app.todayCircleColor = fromRGBtoHex((235,85,69))

    app.calendarOuterFont = fromRGBtoHex((110,110,110))
    app.calendarInnerFont = fromRGBtoHex((255,255,255))

    ###########################################################################
    # 
    ###########################################################################

    dateToday = datetime.now(tz = None) #NOT NEEDED
    app.today = dateToday.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo = None)
    numDay = dateToday.isoweekday()
    lastSunday = dateToday - timedelta(days = (numDay))

    # app.midnight = app.today.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo = None)

    app.dayInSeconds = 86400

    app.weekDays = []
    app.weekEvents = icalendarLibraryTests2()
    for day in range(7):
        currDate = lastSunday + timedelta(days = day)
        currDate = currDate.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo = None)
        app.weekDays.append(currDate)
        for event in app.weekEvents[currDate]:
            datetimeToCalendar(app, event, day)
            
    app.colorList = [(81, 171, 242), (191, 120, 218), (167, 143, 108), (107, 212, 95), (248, 215, 74), (240, 154, 55), (234, 66, 106), (242, 171, 207)]
    
    ###########################################################################
    # calendar event selection
    ###########################################################################
    
    app.selectedEvent = None
    app.selectedProportion = None
    app.deselectedColor = None
    app.selectedColor = None
    app.draggedPosition = None

    app.eventEditing = False

def openingMode_redrawAll(app, canvas):
    canvas.create_image(app.width//2, app.height//2, \
        image=ImageTk.PhotoImage(app.openingModeImage))

def openingMode_keyPressed(app, event):
    app.mode = "calendarMode"

def datetimeToCalendar(app, event, day):
    '''
    convert an event's startTime and stopTime into pixelTop and pixelBot 
    for use by the "view"
    '''
    event.day = day

    midnight = app.weekDays[day]

    event.pixelTop = int(app.calendarTopMargin + (event.startTime - \
        midnight).total_seconds()/app.dayInSeconds*app.calendarPixelHeight)
    event.pixelBot = int(event.pixelTop + \
        event.duration.total_seconds()/app.dayInSeconds*app.calendarPixelHeight)

    event.pixelLeft = int(app.calendarLeftMargin + day * app.calendarPixelWidth/7)
    event.pixelRight = int(app.calendarLeftMargin + day * app.calendarPixelWidth/7 \
        + app.calendarPixelWidth*.95/7)
    

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

def calendarMode_timerFired(app):
    pass

def calendarMode_appStopped(app):
    pass

def calendarMode_rightPressed(app, event):
    x, y = event.x, event.y

    if mouseInCalendar(app, x, y):
        if mouseOnEvent(app, x, y) == None:
            createEvent(app, x, y)

# def calendarMode_rightPressed(app, event):
#     '''
#     check where mouse is on view
#         - if on event, select event
#         - if on calendar and an event is selected, deselect the event.
#     '''
#     x, y = event.x, event.y
#     if mouseInCalendar(app, x, y):
#         if mouseOnButtons(app, x, y):
#             deselectEvent(app)
#             pass
#         else:
#             dayClicked = mouseOnDay(app, x, y)
#             clickedEvent = mouseOnEvent(app, x, y)
#             if clickedEvent != None:
#                 deselectEvent(app)
#                 selectEvent(app, clickedEvent, dayClicked, y)
#                 app.draggedPosition = (x, y)
#             else:
#                 # createEvent(app, x, y)
#                 deselectEvent(app)
#     else:
#         deselectEvent(app)



def calendarMode_mousePressed(app, event):
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
            dayClicked = mouseOnDay(app, x, y)
            clickedEvent = mouseOnEvent(app, x, y)
            if clickedEvent != None:
                deselectEvent(app)
                selectEvent(app, clickedEvent, dayClicked, y)
                app.draggedPosition = (x, y)
            else:
                deselectEvent(app)
    else:
        deselectEvent(app)

def createEvent(app, x, y):
    if app.selectedEvent == None:
        dayIndex = int((x - app.calendarLeftMargin) / (app.calendarPixelWidth/7))
        dayClicked = app.weekDays[dayIndex]
        
        proportionCalendar = (y - app.calendarTopMargin) / (app.calendarPixelHeight)
        startInSeconds = app.dayInSeconds*proportionCalendar
        

        startTime = dayClicked + timedelta(seconds = startInSeconds)
        endTime = startTime + timedelta(seconds = 60*60)

        
        # datetime(dayDt.year, dayDt.month, dayDt.day, y stuff hour, y stuff, tzinfo=None)
        # endTime = datetime(dayDt.year, dayDt.month, dayDt.day, y stuff hour + 1, y stuff, tzinfo=None)

        createdEvent = calendarEvent("(no title)", startTime, endTime) # placeholders
        
        datetimeToCalendar(app, createdEvent, dayIndex)

        createdEvent.day = dayClicked
        # createdEvent.pixelTop = y # placeholder for datetimeToCalendar
        # createdEvent.pixelBot = y + app.calendarPixelHeight//24
        # createdEvent.pixelLeft = int(app.calendarLeftMargin + dayIndex * app.calendarPixelWidth/7)
        # createdEvent.pixelRight = int(app.calendarLeftMargin + dayIndex * app.calendarPixelWidth/7 \
        # + app.calendarPixelWidth*.95/7)
        createdEvent.color = choice(app.colorList)

        app.deselectedColor = createdEvent.color
        app.selectedColor = tuple([app.deselectedColor[i]//4*3 for i in range(3)])
        createdEvent.color = app.selectedColor
        app.selectedEvent = createdEvent
        app.weekEvents[dayClicked].add(createdEvent)

def mouseOnDay(app, x, y):
    '''
    
    '''
    if mouseInCalendar(app, x, y):
        dayIndex = int((x - app.calendarLeftMargin) / (app.calendarPixelWidth/7))
        return app.weekDays[dayIndex]
    return None

def mouseInCalendar(app, x, y):
    '''
    return True if mouse is in calendar portion of the view
    return False otherwise
    '''
    return (app.calendarLeftMargin <= x <= app.calendarWidth) and \
        (app.calendarTopMargin <= y <= app.calendarHeight)

def mouseOnButtons(app, x, y):
    '''
    return True if mouse is on a button in view
    return False otherwise
    '''
    return False

def mouseOnEvent(app, x, y): ##########
    '''
    return the event if mouse is on an event
    return None otherwise
    '''
    for day in app.weekEvents:
        for event in app.weekEvents[day]:
            if (event.pixelLeft <= x <= event.pixelRight) and \
                (event.pixelTop <= y <= event.pixelBot):
                return event
    return None

def selectEvent(app, event, day, y):
    '''
    - store the color of an event before selection
    - create darker "highlighted" new selected color and make it event's color 
    - remove from events set
    '''
    app.deselectedColor = event.color
    app.selectedColor = tuple([app.deselectedColor[i]//4*3 for i in range(3)])
    event.color = app.selectedColor
    app.selectedEvent = event

    # app.selectedProportion = (event.pixelBot - event.pixelTop) / (y - event.pixelTop)
    app.selectedProportion = y - event.pixelTop

    app.weekEvents[day].remove(event)

def deselectEvent(app):
    '''
    if there is a selected event
        - change color back to lighter color
    '''
    event = app.selectedEvent

    if event != None:
        app.weekEvents[event.day].remove(event)
        event.color = app.deselectedColor
        app.weekEvents[event.day].add(event)
    
    app.selectedEvent = None
    app.deselectedColor = None
    app.selectedColor = None
    app.draggedPosition = None
    app.selectedProportion = None
    app.eventEditing = False

def fixEvent(app, event, x, y):
    '''
    changes the attributes of an event to match the given x, y coordinates
    of the mouse
    '''
    height = event.pixelBot - event.pixelTop
    if y - app.selectedProportion < app.calendarTopMargin:
        event.pixelTop = app.calendarTopMargin
        event.pixelBot = app.calendarTopMargin + height
    elif y + (height - app.selectedProportion) > app.calendarHeight:
        event.pixelBot = app.calendarHeight
        event.pixelTop = app.calendarHeight - height
    else:
        event.pixelTop = y - app.selectedProportion
        event.pixelBot = y + (height - app.selectedProportion)

    if x + (app.calendarPixelWidth/7)/2 > app.calendarWidth:
        dayIndex = 6
        event.pixelLeft = int(app.calendarLeftMargin + dayIndex * app.calendarPixelWidth/7)
        event.pixelRight = int(app.calendarLeftMargin + dayIndex * app.calendarPixelWidth/7 \
        + app.calendarPixelWidth*.95/7)
    elif x - (app.calendarPixelWidth/7)/2 < app.calendarLeftMargin:
        dayIndex = 0
        event.pixelLeft = int(app.calendarLeftMargin)
        event.pixelRight = int(app.calendarLeftMargin + app.calendarPixelWidth*.95/7)
    else:
        dayIndex = int((x - app.calendarLeftMargin)/(app.calendarPixelWidth/7))
        event.pixelLeft = int(app.calendarLeftMargin + dayIndex * app.calendarPixelWidth/7)
        event.pixelRight = int(app.calendarLeftMargin + dayIndex * app.calendarPixelWidth/7 \
            + app.calendarPixelWidth*.95/7)
    
    event.day = app.weekDays[dayIndex]
    
    app.weekEvents[event.day].add(event)

# def calendarMode_rightDragged(app, event):
#     '''
#     if an event is selected, then change dragged position (where dragged event
#     will be drawn)
#     '''
#     x, y = event.x, event.y

#     if app.selectedEvent != None:
#         app.draggedPosition = (x, y)

def calendarMode_mouseDragged(app, event):
    '''
    if an event is selected, then change dragged position (where dragged event
    will be drawn)
    '''
    x, y = event.x, event.y

    if app.selectedEvent != None:
        app.draggedPosition = (x, y)

# def calendarMode_rightReleased(app, event):
#     '''
#     if an event is selected, then the selected event is fixed at the x, y 
#     position
#     '''
#     x, y = event.x, event.y

#     if app.selectedEvent != None:
#         app.draggedPosition = (x, y)

#         fixEvent(app, app.selectedEvent, x, y)

#         app.draggedPosition = None

def calendarMode_mouseReleased(app, event):
    '''
    if an event is selected, then the selected event is fixed at the x, y 
    position
    '''
    x, y = event.x, event.y

    if app.selectedEvent != None:
        app.draggedPosition = (x, y)

        fixEvent(app, app.selectedEvent, x, y)

        app.draggedPosition = None

def calendarMode_keyReleased(app, event):
    # if app.selectedEvent != None:
    #     if event.key == "Delete":
    #         deleteEvent(app)
    #     if event.key == "Space":
    #         pass
    pass

def deleteEvent(app):
    '''
    if there is a selected event
        - change color back to lighter color
    '''
    event = app.selectedEvent

    if event != None:
        app.weekEvents[event.day].remove(event)
    
    app.selectedEvent = None
    app.deselectedColor = None
    app.selectedColor = None
    app.draggedPosition = None
    app.selectedProportion = None
    app.eventEditing = False

def calendarMode_keyPressed(app, event):
    if app.selectedEvent != None:
        if event.key == "Delete":
            deleteEvent(app)
        if event.key == "Space":
            app.eventEditing = True
    if app.eventEditing == True:
        if event.key == "Enter":
            app.eventEditing = False

'''
press space,
cause new mode to happen where mouse is disabled
make Delete map to app.selectedEvent.summary = app.selectedEvent.summary[:-1]
make event.key 's that are in ASCII map to app.selectedEvent.summary += event.key
make Enter map to closing new mode
obviously make a screen that shows the startTime and endTime
obviously case on numbers for startTime endTime
'''

def calendarMode_sizeChanged(app):
    pass

def calendarMode_mouseMoved(app, event):
    pass

def calendarMode_redrawAll(app, canvas):
    drawCalendar(app, canvas)

def drawCalendar(app, canvas):
    drawWeekBackground(app, canvas)
    drawWeekEvents(app, canvas)
    drawDraggedEvent(app, canvas)
    drawEventDescription(app, canvas)

def drawEventDescription(app, canvas):
    event = app.selectedEvent

    if app.selectedEvent != None and app.eventEditing:
        dayDt = event.day
        dayNum = app.weekDays.index(dayDt)

        eventMiddlePixel = (event.pixelBot - event.pixelTop)//2 + event.pixelTop

        panelHeight = 200
        
        if dayNum >= 3:
            x1 = app.calendarLeftMargin + int(app.calendarPixelWidth/7*dayNum)\
                 - app.calendarEditMargin
            # y1 = app.calendarHeight - app.calendarEditMargin
            x0 = x1 - int(app.calendarPixelWidth/7*2) + 2*app.calendarEditMargin
            # x0 = app.calendarLeftMargin + app.calendarEditMargin
            # y0 = app.calendarTopMargin + app.calendarEditMargin
            y0 = max(app.calendarTopMargin, \
                eventMiddlePixel - panelHeight//2)
            y1 = min(app.calendarHeight - app.calendarEditMargin, y0 + panelHeight)
            y0 = y1 - panelHeight
        else:
            x0 = app.calendarLeftMargin + int(app.calendarPixelWidth/7*(dayNum+1)\
                + app.calendarEditMargin)
            # y0 = app.calendarTopMargin + app.calendarEditMargin
            x1 = x0 + int(app.calendarPixelWidth/7*2) - 2*app.calendarEditMargin
            # x1 = app.calendarWidth - app.calendarEditMargin
            # y1 = app.calendarHeight - app.calendarEditMargin
            y0 = max(app.calendarTopMargin, \
                eventMiddlePixel - panelHeight//2)
            y1 = min(app.calendarHeight - app.calendarEditMargin, y0 + panelHeight)
            y0 = y1 - panelHeight

        canvas.create_rectangle(x0, y0, x1, y1, fill = app.calendarBgColor,
                                outline = app.calendarBgColor)

# credit to https://stackoverflow.com/a/44100075
def drawRoundRectangle(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def drawDraggedEvent(app, canvas):
    event = app.selectedEvent

    if app.draggedPosition != None:
        x, y = app.draggedPosition
        eventHeight = event.pixelBot - event.pixelTop

        if y - app.selectedProportion < app.calendarTopMargin:
            dragPixelTop = app.calendarTopMargin
            dragPixelBot = app.calendarTopMargin + eventHeight
        elif y + (eventHeight - app.selectedProportion) > app.calendarHeight:
            dragPixelTop = app.calendarHeight - eventHeight
            dragPixelBot = app.calendarHeight
        else:
            dragPixelTop = y - app.selectedProportion
            dragPixelBot = y + (eventHeight - app.selectedProportion)

        if x + (app.calendarPixelWidth/7)/2 > app.calendarWidth:
            dayIndex = 6
            dragPixelLeft = int(app.calendarLeftMargin + dayIndex * app.calendarPixelWidth/7)
            dragPixelRight = int(app.calendarLeftMargin + dayIndex * app.calendarPixelWidth/7 \
            + app.calendarPixelWidth*.95/7)
        elif x - (app.calendarPixelWidth/7)/2 < app.calendarLeftMargin:
            dayIndex = 0
            dragPixelLeft = int(app.calendarLeftMargin)
            dragPixelRight = int(app.calendarLeftMargin + app.calendarPixelWidth*.95/7)
        else:
            dayIndex = int((x - app.calendarLeftMargin)/(app.calendarPixelWidth/7))
            dragPixelLeft = int(app.calendarLeftMargin + dayIndex * app.calendarPixelWidth/7)
            dragPixelRight = int(app.calendarLeftMargin + dayIndex * app.calendarPixelWidth/7 \
                + app.calendarPixelWidth*.95/7)
            
        canvas.create_rectangle(dragPixelLeft + .5, dragPixelTop, 
                                dragPixelRight, dragPixelBot, 
                                fill = fromRGBtoHex(event.color),
                                width = 0)
        if len(event.summary) >= 19:
            eventText = event.summary[:18] + "…"
        else:
            eventText = event.summary
            
        canvas.create_text(dragPixelLeft + 2, dragPixelTop, 
                        text = eventText, anchor = "nw",
                        fill = app.calendarInnerFont, font = "Arial 12")


def drawWeekEvents(app, canvas):
    for index in range(7):
        weekDay = app.weekDays[index]
        for event in app.weekEvents[weekDay]:
            canvas.create_rectangle(event.pixelLeft + .5, event.pixelTop, 
                                event.pixelRight, event.pixelBot, 
                                fill = fromRGBtoHex(event.color),
                                width = 0)

            if len(event.summary) >= 19:
                eventText = event.summary[:18] + "…"
            else:
                eventText = event.summary
                
            canvas.create_text(event.pixelLeft + 2, event.pixelTop, 
                            text = eventText, anchor = "nw",
                            fill = app.calendarInnerFont, font = "Arial 12")

def drawWeekBackground(app, canvas):
    '''
    draw lines across calendar side of view
    draw hours text
    '''
    canvas.create_rectangle(0, 0, app.width, app.height, fill = app.calendarBgColor)

    canvas.create_rectangle(app.calendarLeftMargin, app.calendarTopMargin, \
        app.calendarLeftMargin + app.calendarPixelWidth//7, app.height, \
            fill = app.calendarWkndColor, width = 0)
    
    canvas.create_rectangle(app.calendarLeftMargin + app.calendarPixelWidth*6//7, \
        app.calendarTopMargin, app.calendarWidth, app.height, fill = app.calendarWkndColor, width = 0)

    canvas.create_line(0, app.calendarTopMargin, \
        app.calendarWidth, app.calendarTopMargin, fill = app.calendarFgColor, width = 2)

    for day in range(7):
        dayDt = app.weekDays[day]

        dayPixel = app.calendarLeftMargin + int(app.calendarPixelWidth/7*(day + 1/2))
        textWeekDay = dayDt.strftime('%A').upper()[:3]
        textMonthDay = dayDt.strftime('%d')
        
        monthDayColor = app.calendarOuterFont

        if dayDt == app.today:
            canvas.create_oval(dayPixel - 22, app.calendarTopMargin*2//3 - 22,
                               dayPixel + 22, app.calendarTopMargin*2//3 + 22,
                               fill = app.todayCircleColor, width = 0)
            monthDayColor = app.calendarBgColor

        canvas.create_text(dayPixel, app.calendarTopMargin*3//10, text = textWeekDay,
                           fill = app.calendarOuterFont, font = "Arial 14")

        canvas.create_text(dayPixel, app.calendarTopMargin*2//3, text = textMonthDay,
                           fill = monthDayColor, font = "Arial 28")

        canvas.create_line(int(app.calendarLeftMargin + app.calendarPixelWidth/7*day), 
            app.calendarTopMargin*7//9, int(app.calendarLeftMargin + app.calendarPixelWidth/7*day), 
            app.calendarHeight, fill = app.calendarFgColor, width = .5)

    # if app.today in app.weekEvents:


    for hour in range(1, 25, 2):
        hourPixel = int(app.calendarPixelHeight/24*hour + app.calendarTopMargin)
        canvas.create_line(app.calendarLeftMargin//2, hourPixel, \
            app.calendarWidth, hourPixel, fill = app.calendarFgColor, width = .5)
        
        if hour < 12: 
            hourText = f"{hour} AM"
        elif hour == 12:
            hourText = f"{hour} PM"
        else:
            hourText = f"{hour%12} PM"

        canvas.create_text(app.calendarLeftMargin//4, hourPixel, \
            text = hourText, fill = app.calendarOuterFont, font = "Arial 11")



if __name__ == "__main__":
    runApp(width=1000, height=800)