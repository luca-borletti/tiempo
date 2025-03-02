from cmu_112_graphics import *
from datetime import *
from random import *
from ics_parsing import *
from string import *
from PIL import ImageFont
from copy import *

'''
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
    app.calendarEditColor = fromRGBtoHex((47,48,49))
    app.calendarEditBorderColor = fromRGBtoHex((88,88,88))

    app.calendarOuterFont = fromRGBtoHex((110,110,110))
    app.calendarInnerFont = fromRGBtoHex((255,255,255))

    app.editingx0 = None
    app.editingx1 = None
    app.editingy0 = None
    app.editingy1 = None

    app.editingPanelHeight = 200

    app.editingMode = None
    app.editingStart = None
    app.editingEnd = None
    app.editingName = None

    ###########################################################################
    # datetime variables
    ###########################################################################

    dateToday = datetime.now(tz = None) #NOT NEEDED
    app.today = dateToday.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo = None)
    numDay = dateToday.isoweekday()
    lastSunday = dateToday - timedelta(days = (numDay))

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

    ###########################################################################
    # interleaving
    ###########################################################################

    # restartInterleaving(app)

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

    event.duration = (event.endTime - event.startTime)

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
        if mouseOnEvent(app, x, y) == None and not app.eventEditing:
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
        if app.eventEditing and mouseInEditing(app, x, y):
            app.editingMode = mouseInMode(app, x, y)
        else: 
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
                    # if app.eventEditing:

                    #     pass
                    # else: 
                    deselectEvent(app)
    # elif (app.eventInterleaving == 1):
    #     day = mouseOnDay(app, x, y)
    #     if day != None:
    #         app.daySelected = day
    else:
        deselectEvent(app)

def mouseInEditing(app, x, y):
    return (app.editingx0 <= x <= app.editingx1) and (app.editingy0 <= y <= app.editingy1)

def mouseInMode(app, x, y):
    return (y - app.editingy0) // (app.editingPanelHeight/3)
    # if mode == 0.0 and (app.editingy0 + 30 - app.calendarEditMargin//2 <= y <= app.editingy1):
    # elif mode == 1.0 and :
    # elif mode == 2.0 and :
    # else:
    #     return None 

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

        createdEvent.day = dayIndex
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
        app.weekEvents[app.weekDays[event.day]].remove(event)
        event.color = app.deselectedColor
        app.weekEvents[app.weekDays[event.day]].add(event)
    
    app.selectedEvent = None
    app.deselectedColor = None
    app.selectedColor = None
    app.draggedPosition = None
    app.selectedProportion = None
    app.eventEditing = False
    app.editingMode = None

def fixEventContents(app):
    event = app.selectedEvent
    dayNum = event.day
    dayDt = app.weekDays[dayNum]

    bisectedStart = app.editingStart.strip().split(":")
    if len(bisectedStart) != 2:
        return
    startHour = bisectedStart[0].strip()
    startMinute = bisectedStart[1].strip()[:2]
    startAMPM = app.editingStart[-2:].strip()

    bisectedEnd = app.editingEnd.strip().split(":")
    if len(bisectedEnd) != 2:
        return
    endHour = bisectedEnd[0].strip()
    endMinute = bisectedEnd[1].strip()[:2]
    endAMPM = app.editingEnd[-2:].strip()

    startTime = deepcopy(app.weekDays[dayNum])
    endTime = deepcopy(app.weekDays[dayNum])
    
    if startHour.isnumeric() and startMinute.isnumeric() and (startAMPM == "AM" \
        or startAMPM == "PM"):
        startHour = int(startHour)
        startMinute = int(startMinute)
        if (1 <= startHour <= 12) and (0 <= startMinute <= 59):
            if startAMPM == "AM" and startHour == 12:
                startTime = startTime.replace(hour = 0, minute = startMinute)
            elif startAMPM == "AM":
                startTime = startTime.replace(hour = startHour, minute = startMinute)
            elif startAMPM == "PM" and startHour == 12:
                startTime = startTime.replace(hour = 12, minute = startMinute)
            elif startAMPM == "PM":
                startTime = startTime.replace(hour = startHour + 12, minute = startMinute)

    if endHour.isnumeric() and endMinute.isnumeric() and (endAMPM == "AM" \
        or endAMPM == "PM"):
        endHour = int(endHour)
        endMinute = int(endMinute)
        if (1 <= endHour <= 12) and (0 <= endMinute <= 59):
            if endAMPM == "AM" and endHour == 12:
                endTime = endTime.replace(hour = 0, minute = endMinute)
            elif endAMPM == "AM":
                endTime = endTime.replace(hour = endHour, minute = endMinute)
            elif endAMPM == "PM" and endHour == 12:
                endTime = endTime.replace(hour = 12, minute = endMinute)
            elif endAMPM == "PM":
                endTime = endTime.replace(hour = (endHour + 12), minute = endMinute)

    if startTime != dayDt and endTime != dayDt:
        if endTime > startTime:
            event.startTime = startTime
            event.endTime = endTime
            datetimeToCalendar(app, app.selectedEvent, dayNum)
            app.weekEvents[app.weekDays[event.day]].remove(event)
            app.weekEvents[app.weekDays[event.day]].add(event)

def fixEventPosition(app, event, x, y):
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
    
    event.day = dayIndex

    event.startTime = app.weekDays[dayIndex] + timedelta(seconds = app.dayInSeconds*((event.pixelTop - app.calendarTopMargin)/app.calendarPixelHeight))
    event.endTime = app.weekDays[dayIndex] + timedelta(seconds = app.dayInSeconds*((event.pixelBot - app.calendarTopMargin)/app.calendarPixelHeight))
    
    event.startTime = event.startTime.replace(microsecond = 0)
    event.endTime = event.endTime.replace(microsecond = 0)
    
    app.weekEvents[app.weekDays[event.day]].add(event)

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

    if app.selectedEvent != None and not app.eventEditing:
        app.draggedPosition = (x, y)

# def calendarMode_rightReleased(app, event):
#     '''
#     if an event is selected, then the selected event is fixed at the x, y 
#     position
#     '''
#     x, y = event.x, event.y

#     if app.selectedEvent != None:
#         app.draggedPosition = (x, y)

#         fixEventPosition(app, app.selectedEvent, x, y)

#         app.draggedPosition = None

def calendarMode_mouseReleased(app, event):
    '''
    if an event is selected, then the selected event is fixed at the x, y 
    position
    '''
    x, y = event.x, event.y

    if app.selectedEvent != None and not app.eventEditing:
        app.draggedPosition = (x, y)

        fixEventPosition(app, app.selectedEvent, x, y)

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
        app.weekEvents[app.weekDays[event.day]].remove(event)
    
    app.selectedEvent = None
    app.deselectedColor = None
    app.selectedColor = None
    app.draggedPosition = None
    app.selectedProportion = None
    app.eventEditing = False

def calendarMode_keyPressed(app, event):
    if app.selectedEvent != None and app.draggedPosition == None:
        if app.eventEditing == True:
            if event.key == "Enter":
                fixEventContents(app)
                app.eventEditing = False
            if app.editingMode == 0.0:
                if event.key in printable:
                    app.selectedEvent.summary += event.key
                    truncateEditingName(app, app.selectedEvent)
                elif event.key == "Delete":
                    app.selectedEvent.summary = app.selectedEvent.summary[:-1]
                    truncateEditingName(app, app.selectedEvent)
                elif event.key == "Space":
                    app.selectedEvent.summary += " "
                    truncateEditingName(app, app.selectedEvent)
            elif app.editingMode == 1.0:
                if event.key in "APM0123456789:":
                    app.editingStart += event.key
                elif event.key == "Delete":
                    app.editingStart = app.editingStart[:-1]
                elif event.key == "Space":
                    app.editingStart += " "
            elif app.editingMode == 2.0:
                if event.key in "APM0123456789:":
                    app.editingEnd += event.key
                elif event.key == "Delete":
                    app.editingEnd = app.editingEnd[:-1]
                elif event.key == "Space":
                    app.editingEnd += " "
        else:
            if event.key == "Delete":
                deleteEvent(app)
            if event.key == "Space":
                app.eventEditing = True
                createEditingPanel(app)
    # elif not app.eventEditing:
    #     if app.eventInterleaving == 1:
    #         if event.key == "Escape":
    #             app.eventInterleaving = 0
    #             restartInterleaving(app)
    #     elif event.key == "I":
    #         app.eventInterleaving = 1

# def restartInterleaving(app):
#     app.eventInterleaving = 0
#     app.interDay = None
#     app.interEvents = None

def createEditingPanel(app):
    event = app.selectedEvent
    
    dayNum = event.day
    dayDt = app.weekDays[dayNum]
    z = (event.pixelBot - event.pixelTop)//2 + event.pixelTop
    
    if dayNum >= 3:
        app.editingx1 = app.calendarLeftMargin + int(app.calendarPixelWidth/7*dayNum)\
             - app.calendarEditMargin
        # y1 = app.calendarHeight - app.calendarEditMargin
        app.editingx0 = app.editingx1 - int(app.calendarPixelWidth/7*2) + 2*app.calendarEditMargin
        # x0 = app.calendarLeftMargin + app.calendarEditMargin
        # y0 = app.calendarTopMargin + app.calendarEditMargin
        app.editingy0 = max(app.calendarTopMargin, \
            z - app.editingPanelHeight//2)
        app.editingy1 = min(app.calendarHeight - app.calendarEditMargin, app.editingy0 + app.editingPanelHeight)
        app.editingy0 = app.editingy1 - app.editingPanelHeight
    else:
        app.editingx0 = app.calendarLeftMargin + int(app.calendarPixelWidth/7*(dayNum+1)\
            + app.calendarEditMargin)
        # y0 = app.calendarTopMargin + app.calendarEditMargin
        app.editingx1 = app.editingx0 + int(app.calendarPixelWidth/7*2) - 2*app.calendarEditMargin
        # x1 = app.calendarWidth - app.calendarEditMargin
        # y1 = app.calendarHeight - app.calendarEditMargin
        app.editingy0 = max(app.calendarTopMargin, \
            z - app.editingPanelHeight//2)
        app.editingy1 = min(app.calendarHeight - app.calendarEditMargin, app.editingy0 + app.editingPanelHeight)
        app.editingy0 = app.editingy1 - app.editingPanelHeight
    
    truncateEditingName(app, event)

    eventDay = event.startTime.day
    
    eventStartHr = event.startTime.hour
    eventStartMin = event.startTime.minute
    if eventStartHr == 0:
        s_M = "AM"
        s_hour = 12
    elif eventStartHr < 12:
        s_M = "AM"
        s_hour = eventStartHr
    elif eventStartHr == 12:
        s_M = "PM"
        s_hour = eventStartHr
    else:
        s_M = "PM"
        s_hour = eventStartHr % 12
    s_min = event.startTime.strftime("%M")
    app.editingStart = f"{s_hour} : {s_min} {s_M}"


    eventEndHr = event.endTime.hour
    eventEndMin = event.endTime.minute
    if eventEndHr == 0:
        e_M = "AM"
        e_hour = 12
    elif eventEndHr < 12:
        e_M = "AM"
        e_hour = eventEndHr
    elif eventEndHr == 12:
        e_M = "PM"
        e_hour = eventEndHr
    else:
        e_M = "PM"
        e_hour = eventEndHr % 12
    e_min = event.endTime.strftime("%M")
    app.editingEnd = f"{e_hour} : {e_min} {e_M}"

def truncateEditingName(app, calendarEvent):
    nameText = calendarEvent.summary

    while(get_pil_text_size(nameText, 15, "arial.ttf")[0] > (app.calendarPixelWidth/7*2 - 55)):
            nameText = nameText[:-1]

    if nameText != calendarEvent.summary:
        nameText += "…"
    
    app.editingName = nameText

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
    drawEditingPanel(app, canvas)

# credit to https://stackoverflow.com/a/35772222
def get_pil_text_size(text, font_size, font_name):
    font = ImageFont.truetype(font_name, font_size)
    size = font.getsize(text)
    return size

def drawEditingPanel(app, canvas):
    event = app.selectedEvent

    if app.selectedEvent != None and app.eventEditing:
        dayNum = event.day
        dayDt = app.weekDays[dayNum]    


        
        z = (event.pixelBot - event.pixelTop)//2 + event.pixelTop
        
        if dayNum >= 3:
            x1 = app.calendarLeftMargin + int(app.calendarPixelWidth/7*dayNum)\
                 - app.calendarEditMargin
            # y1 = app.calendarHeight - app.calendarEditMargin
            x0 = x1 - int(app.calendarPixelWidth/7*2) + 2*app.calendarEditMargin
            # x0 = app.calendarLeftMargin + app.calendarEditMargin
            # y0 = app.calendarTopMargin + app.calendarEditMargin
            y0 = max(app.calendarTopMargin, \
                z - app.editingPanelHeight//2)
            y1 = min(app.calendarHeight - app.calendarEditMargin, y0 + app.editingPanelHeight)
            y0 = y1 - app.editingPanelHeight

            points = [x0, y0, x1, y0, x1, z - 10, x1 + app.calendarEditMargin, z, \
            x1, z + 10, x1, y1, x0, y1]
        else:
            x0 = app.calendarLeftMargin + int(app.calendarPixelWidth/7*(dayNum+1)\
                + app.calendarEditMargin)
            # y0 = app.calendarTopMargin + app.calendarEditMargin
            x1 = x0 + int(app.calendarPixelWidth/7*2) - 2*app.calendarEditMargin
            # x1 = app.calendarWidth - app.calendarEditMargin
            # y1 = app.calendarHeight - app.calendarEditMargin
            y0 = max(app.calendarTopMargin, \
                z - app.editingPanelHeight//2)
            y1 = min(app.calendarHeight - app.calendarEditMargin, y0 + app.editingPanelHeight)
            y0 = y1 - app.editingPanelHeight

            points = [x0, y0, x1, y0, x1, y1, x0, y1, x0, z + 10, \
                x0 - app.calendarEditMargin, z, x0, z - 10]

        canvas.create_polygon(points, fill = app.calendarEditColor,
                              outline = app.calendarEditBorderColor)

        if app.editingMode == 0.0:
            canvas.create_rectangle(x0, y0, x1, y0 + app.editingPanelHeight/3,\
                fill = app.calendarEditBorderColor, width = 0)
        elif app.editingMode == 1.0:
            canvas.create_rectangle(x0, y0 + app.editingPanelHeight/3, x1, y0 + app.editingPanelHeight/3*2,\
                fill = app.calendarEditBorderColor, width = 0)
        elif app.editingMode == 2.0:
            canvas.create_rectangle(x0, y0 + app.editingPanelHeight/3*2, x1, y0 + app.editingPanelHeight, \
                fill = app.calendarEditBorderColor, width = 0)

        canvas.create_text(x0 + app.calendarEditMargin//2, y0 + app.calendarEditMargin//2, \
            text = "Name: ", anchor = "nw", fill = app.calendarOuterFont, font = "Arial 15")
        canvas.create_text(x0 + app.calendarEditMargin//2, y0 + 30 - app.calendarEditMargin//2, \
            text = app.editingName, anchor = "nw", fill = app.calendarInnerFont, font = "Arial 15 bold")
        
        canvas.create_text(x0 + app.calendarEditMargin//2, y0 + app.calendarEditMargin//2 + app.editingPanelHeight/3, \
            text = "Start time: ", anchor = "nw", fill = app.calendarOuterFont, font = "Arial 15")
        canvas.create_text(x0 + app.calendarEditMargin//2, y0 + 30 - app.calendarEditMargin//2 + app.editingPanelHeight/3, \
            text = app.editingStart, anchor = "nw", fill = app.calendarInnerFont, font = "Arial 15 bold")

        canvas.create_text(x0 + app.calendarEditMargin//2, y0 + app.calendarEditMargin//2 + 2*app.editingPanelHeight/3, \
            text = "End time: ", anchor = "nw", fill = app.calendarOuterFont, font = "Arial 15")
        canvas.create_text(x0 + app.calendarEditMargin//2, y0 + 30 - app.calendarEditMargin//2 + 2*app.editingPanelHeight/3, \
            text = app.editingEnd, anchor = "nw", fill = app.calendarInnerFont, font = "Arial 15 bold")
        
        for line in range(2):
            canvas.create_line(x0, (line + 1)*app.editingPanelHeight//3 + y0, \
                x1, (line + 1)*app.editingPanelHeight//3 + y0, fill = app.calendarEditBorderColor)
        
        # eventName = event.summary

        # startTime = 
        # endTime = 
# credit to https://stackoverflow.com/a/44100075
def drawRoundRectangle(canvas, x1, y1, x2, y2, radius=8, **kwargs):
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
        
        drawRoundRectangle(canvas, dragPixelLeft + .5, dragPixelTop, \
                dragPixelRight, dragPixelBot, fill = fromRGBtoHex(event.color), \
                    width = 0)

        # canvas.create_rectangle(dragPixelLeft + .5, dragPixelTop, 
        #                         dragPixelRight, dragPixelBot, 
        #                         fill = fromRGBtoHex(event.color),
        #                         width = 0)
        
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
            drawRoundRectangle(canvas, event.pixelLeft + .5, event.pixelTop, \
                event.pixelRight, event.pixelBot, fill = fromRGBtoHex(event.color), \
                    width = 0)
            # canvas.create_rectangle(event.pixelLeft + .5, event.pixelTop, 
            #                     event.pixelRight, event.pixelBot, 
            #                     fill = fromRGBtoHex(event.color),
            #                     width = 0)

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
    runApp(width=1400, height=800)