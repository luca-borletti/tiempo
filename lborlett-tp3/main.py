### XYLO CALENDAR ###
# made by Luca Borletti
# a 15-112 F21 term project

from cmu_112_graphics import *
from datetime import *
from random import *
from string import *
from PIL import ImageFont
from copy import *
from math import *
from icalendar import *
from pytz import *
from json import *
from decimal import *
from pygame import *

import os

'''
•••••• fix sound

• clean up code

••• make it write to a file

••• make it check stuff in a folder where you put ics file and auto check

••• make save mode and not save mode

        ◊ somehow store max recursive columns for each event
        use that value to change the max 

        ◊ do timer tracker 

        ◊ do toggling of visuals to ask Asad

        ◊ make deletion change coloring graph

        ◊ deal with interleaving & overlap
        
                                            ----- optimize fixEvent to only change prevDay if event.day != index

                                            ----- make events repr different to check for equality (or make __eq__???)

                                            ----- optimize selection/dragging storage of x,y pos

                                            ----- >>> do tasks by just storing tasks inside week object and casing for EVERYTHING

                                            ----- figure out SLOWNESS

                                            ----- (?) put all in same dict

                                            ----- DO TASKS ! DO TASKS ! DO TASKS
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
        self.totalCols = 1

    def __repr__(self):
        return f"{self.summary}. From {str(self.startTime)} to {str(self.endTime)}"

class calendarTask(object):
    def __init__(self, summary, dueTime):
        self.summary = summary
        self.dueTime = dueTime
        self.color = fromRGBtoHex((255, 255, 255))
        self.pixelMid = None

    def __repr__(self):
        return f"{self.summary}. At {str(self.dueTime)}"

#credit to https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#playingSounds
class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1
        mixer.music.load(path)

    def isPlaying(self):
        return bool(mixer.music.get_busy())

    def start(self, loops=1):
        self.loops = loops
        mixer.music.play(loops=loops)

    def stop(self):
        mixer.music.stop()

#credit to https://www.cs.cmu.edu/~112/syllabus.html
def roundHalfUp(d): 
    rounding = ROUND_HALF_UP
    return int(Decimal(d).to_integral_value(rounding=rounding))

#credit to https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#listFiles
def removeTempFiles(path, suffix='.DS_Store'):
    if path.endswith(suffix):
        print(f'Removing file: {path}')
        os.remove(path)
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            removeTempFiles(path + '/' + filename, suffix)

def icsParsing():
    ###########################################################################
    # ics parsing
    ###########################################################################
                                # took literally years to figure this stuff out

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
        
    calendarFile = open("icsFiles/lgborletti@gmail.com.ics", "r")
    # calendarFile = open("icsFiles/apourkav@andrew.cmu.edu.ics", "r")
    calendarInstance = Calendar.from_ical(calendarFile.read())
    
    colorList = [(81, 171, 242), (191, 120, 218), (167, 143, 108),
                 (107, 212, 95), (248, 215, 74), (240, 154, 55), 
                 (234, 66, 106), (242, 171, 207)]
    daysToNums = vWeekday.week_days
    colorIndex = 0
    for event in calendarInstance.walk("VEVENT"):
        if "RRULE" in event and "BYDAY" in event["RRULE"]:
            recurrenceList = event["RRULE"]
            if not "UNTIL" in recurrenceList or \
                recurrenceList["UNTIL"][0].date() > lastSunday.date():
                colorIndex += 1
                repeatingDays = set()
                for byDay in recurrenceList["BYDAY"]:
                    repeatingDays.add(daysToNums[byDay])
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
    return week



def appStarted(app):
    ###########################################################################
    # ADMIN TOGGLES & CHEATS
    ###########################################################################

    app.toggleTopFontLightDark = True
    app.toggleTasksLightDark = True
    app.toggleRoundedRectangle = True

    #MODES: openingMode, fileSelectionMode, calendarMode

    ###########################################################################
    # opening mode
    ###########################################################################

    app.mode = "openingMode"
    path = "images/openingModeImage.jpg"
    app.openingModeImage = app.scaleImage(app.loadImage(path), 1/3)
    app.calendarModeImage = app.scaleImage(app.loadImage(path), 1/25)
    app.widthIntroImage, app.heightIntroImage = app.openingModeImage.size
    app.cxIntroImage = app.width//2
    app.cyIntroImage = app.height//2

    app.openingModeBgColor = fromRGBtoHex((31,32,37))

    app.writeToSaveFile = False

    ###########################################################################
    # file selection mode
    ###########################################################################

    removeTempFiles('icsFiles')
    app.icsFiles = os.listdir("icsFiles")
    app.fileSelectMargin = 100
    app.fileSelectButtons = []
    # for file in app.icsFiles:
    #     x0 = 
    #     y0 = 

    ###########################################################################
    # sound variables
    ###########################################################################

    mixer.init()
    #credit to https://www.videvo.net/sound-effect/xylophone-comedy-21/452096/
    app.introSound = mixer.Sound("sounds/introSound.ogg")
    app.moveEventSound = mixer.Sound("sounds/moveEventSound.ogg")
    app.exitSound = mixer.Sound("sounds/exitSound2.ogg")
    app.createEventSound = mixer.Sound("sounds/createEventSound.ogg")
    app.editEventSound = mixer.Sound("sounds/interleavingSound.ogg")
    app.editEventSound = mixer.Sound("sounds/createEventSound2.ogg")

    path = "images/volumeOffImage.png"
    app.volumeOffImage = app.scaleImage(app.loadImage(path), 1/30)

    path = "images/volumeOnImage.png"
    app.volumeOnImage = app.scaleImage(app.loadImage(path), 1/30)
    app.widthVolumeImage, app.heightVolumeImage = app.volumeOnImage.size

    ###########################################################################
    # calendar mode initial variables
    ###########################################################################

    app.volumeOn = True

    app.calendarLeftMargin = 100
    app.calendarTopMargin = 135
    app.calendarEditMargin = 10

    app.calendarWidth = app.width
    app.calendarHeight = app.height
    
    app.cxVolumeImage = app.calendarWidth - 40
    app.cyVolumeImage = 25

    app.calendarPixelHeight = app.calendarHeight - app.calendarTopMargin
    app.calendarPixelWidth = app.calendarWidth - app.calendarLeftMargin

    app.calendarMonthYearX = 175
    app.calendarMonthYearY = 30

    # app.calendarBgColor = fromRGBtoHex((30,32,35)) last minute change
    app.calendarBgColor = fromRGBtoHex((31,32,37))
    app.calendarFgColor = fromRGBtoHex((70,70,70))
    app.calendarWkndColor = fromRGBtoHex((39,40,42))

    app.todayTrackersColor = fromRGBtoHex((235,85,69))

    app.calendarEditColor = fromRGBtoHex((47,48,49))
    app.calendarEditBorderColor = fromRGBtoHex((88,88,88))

    app.interDayColor = fromRGBtoHex((88,88,88))
    app.interPanelColor = fromRGBtoHex((47,48,49))
    app.interPanelBorderColor = fromRGBtoHex((88,88,88))

    app.calendarOuterFont = fromRGBtoHex((110,110,110))
    app.calendarInnerFont = fromRGBtoHex((255,255,255))
    
    if app.toggleTopFontLightDark:
        app.calendarTopFont = fromRGBtoHex((255,255,255))
    else:
        app.calendarTopFont = fromRGBtoHex((110,110,110))

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
    # tasks background
    ###########################################################################

    app.tasksLeftMargin = app.calendarWidth
    app.tasksTopMargin = app.calendarTopMargin
    app.tasksWidth = app.width
    app.tasksHeight = app.height
    app.tasksPixelWidth = app.width - app.tasksLeftMargin
    app.tasksPixelHeight = app.calendarHeight - app.tasksTopMargin

    if app.toggleTasksLightDark:
        app.tasksBgColor = fromRGBtoHex((51,51,51))
        app.tasksFgColor = fromRGBtoHex((0,0,0))
    else:
        app.tasksBgColor = fromRGBtoHex((30,32,35))
        app.tasksFgColor = fromRGBtoHex((70,70,70))

    app.hourObstructing = -1
    app.currentTimePixel = 0
    app.currentTimeString = ""
    app.timerDelay = 1000*30

    ###########################################################################
    # datetime variables
    ###########################################################################
    
    ''' >>> bundle into function that assigns all these values iff the user
    selects the *create new calendar from ics file* choice and not *use last save*'''
    
    ''' >>> could bundle following lines into function that changes dateToday
    depending on the input from the user (arrows left and right) to change weeks'''
    
    ### initial setup (today & sundays)
    dateToday = datetime.now(tz = None)
    
    app.today = dateToday.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo = None)
    
    app.dayInSeconds = 86400
    numDay = app.today.isoweekday()%7
    lastSunday = app.today - timedelta(days = (numDay))

    # miscellaneous time-related attributes used in model
    app.monthText = app.today.strftime("%B")
    app.yearText = app.today.strftime("%Y")
    app.colorList = [(81, 171, 242), (191, 120, 218), (167, 143, 108), (107, 212, 95), (248, 215, 74), (240, 154, 55), (234, 66, 106), (242, 171, 207)]

    ###########################################################################
    # events & task setup
    ###########################################################################

    app.weekTasks = dict()
    app.weekDays = []
    app.weekEvents = icsParsing()
    
    ### initial graph column coloring
    app.eventsGraph = initializeEventsGraph(app.weekEvents)
    app.columnColoring = dict()
    for day in app.eventsGraph:
        app.columnColoring[day] = greedyEventColumnColoring(app.eventsGraph[day])

    for day in range(7):
        ### setting up useful weekDays list
        currDate = lastSunday + timedelta(days = day)
        currDate = currDate.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo = None)
        app.weekDays.append(currDate)

        ### converting datetime values to pixel values usable by view (w/ coloring)
        for event in app.weekEvents[currDate]:
            datetimeToCalendar(app, event, day)

        ### tasks bare setup 
        app.weekTasks[currDate] = set()

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

    ### useful function that resets process
    restartInterleaving(app)
    updateTimeTracker(app)


################################################################################
# opening mode
################################################################################

''' >>> allow for selection of parsing method (***create new calendar from ics 
file*** choice or ***use last save***)'''

def openingMode_mousePressed(app, event):
    x, y = event.x, event.y
    if app.cxIntroImage - (app.widthIntroImage/2) < x < app.cxIntroImage + (app.widthIntroImage/2)\
        and app.cyIntroImage - (app.heightIntroImage/2) < y < app.cyIntroImage + (app.heightIntroImage/2):
        mixer.Sound.play(app.introSound)
        app.mode = "calendarMode"

def openingMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = app.openingModeBgColor, width = 0)
    canvas.create_image(app.cxIntroImage, app.cyIntroImage, \
        image=ImageTk.PhotoImage(app.openingModeImage))

def greedyHelper(repeatedColorsList):
    '''
    tries to "color" a node with an int given the colors of its neighbors
    '''
    # algorithm adapted from https://en.wikipedia.org/wiki/Greedy_coloring
    repeatedColorsSet = set(repeatedColorsList)
    c = 0
    while True:
        if c not in repeatedColorsSet:
            return c
        c += 1

def greedyEventColumnColoring(graph):
    '''
    "colors" a graph with approx as few int's as possible (int's being cols)
    '''
    eventColumns = dict()
    for event in graph:
        overlappingEvents = graph[event]
        othersColors = []
        for other in overlappingEvents:
            if other in eventColumns:
                othersColors.append(eventColumns[other])
        eventColumns[event] = greedyHelper(othersColors)
    return eventColumns

def initializeEventsGraph(weekEvents):
    '''
    creates dictionary of nodes keying to connected vertices 
    which represents the interval graph of the events (with real number line
    being replaced with time)
    '''
    graph = dict()
    for day in weekEvents:
        dayGraph = dict()
        events = weekEvents[day]
        for event in events:
            dayGraph[event] = dayGraph.get(event, set())
            for other in events-{event}-dayGraph[event]:
                if (event.startTime < other.startTime < event.endTime) or \
                    (event.startTime < other.endTime < event.endTime) or \
                        (other.startTime < event.startTime < event.endTime < other.endTime):
                    dayGraph[event].add(other)
                    dayGraph[other] = dayGraph.get(other, set()).add(event)
        graph[day] = dayGraph
    return graph

def datetimeToCalendar(app, event, day):
    '''
    turns an event's datetime attributes into discrete pixel values for its
    top and bottom edges relative to the size of the calendar as well as 
    its left and right edges dependent on its graph coloring and the day 
    key set that it is in in the weekEvents dictionary
    '''
    event.day = day

    midnight = app.weekDays[day]
    event.duration = (event.endTime - event.startTime)

    event.pixelTop = app.calendarTopMargin + (event.startTime - \
        midnight).total_seconds()/app.dayInSeconds*app.calendarPixelHeight
    event.pixelBot = event.pixelTop + event.duration.total_seconds()\
        /app.dayInSeconds*app.calendarPixelHeight

    if app.eventsGraph[midnight][event] == set():
        event.pixelLeft = int(app.calendarLeftMargin + day * app.calendarPixelWidth/7)
        event.pixelRight = int(app.calendarLeftMargin + day * app.calendarPixelWidth/7 \
            + app.calendarPixelWidth*.95/7)
        event.totalCols = 1
    else:
        farRight = int(app.calendarLeftMargin + day * app.calendarPixelWidth/7)
        nearbyColumns = [max([app.columnColoring[midnight][other] for other in app.eventsGraph[midnight][event]] + [app.columnColoring[midnight][event]])]
        for node in app.eventsGraph[midnight][event]:
            nearbyColumns += [app.columnColoring[midnight][other] for other in app.eventsGraph[midnight][node]] + [app.columnColoring[midnight][node]]
        totalColumns = max(nearbyColumns) + 1
        event.totalCols = totalColumns
        cellSize = app.calendarPixelWidth*.95/7/totalColumns
        column = app.columnColoring[midnight][event]
        event.pixelLeft = farRight + column*cellSize 
        event.pixelRight = farRight + (column+1)*cellSize

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
    updateTimeTracker(app)

def updateTimeTracker(app):
    '''
    create the time tracking line across calendar screen that represents real time
    also deal with obstructing time indicators on left-hand-side of screen
    by checking proximity w/ modulus
    '''
    app.currentTime = datetime.now(tz = None)
    app.currentTimePixel = app.calendarTopMargin + (app.currentTime - \
        app.currentTime.replace(hour = 0, minute = 0, second = 0, microsecond = 0))\
            .total_seconds()/app.dayInSeconds*app.calendarPixelHeight
    
    closestHourPixel = abs((app.currentTimePixel - app.calendarTopMargin + app.calendarPixelHeight/24) % \
        (app.calendarPixelHeight/12))
    if closestHourPixel < 10 or closestHourPixel > app.calendarPixelHeight/12 - 10:
        app.hourObstructing = roundHalfUp((app.currentTimePixel - app.calendarTopMargin)/(app.calendarPixelHeight/24))
    else:
        app.hourObstructing = -1
    app.currentTimeString = str(app.currentTime.strftime("%-I")) + " : " + \
        str(app.currentTime.strftime("%M")) + "  " + app.currentTime.strftime("%p")

def calendarMode_appStopped(app):
    '''>>> add key or button that triggers save mode when pressed'''
    '''
    prints string when app is stopped
    '''
    if app.volumeOn:
        mixer.Sound.play(app.exitSound)

    if app.writeToSaveFile:
        print("Exiting... \n Saving...")
        # writeToSaveFile(app)
    else:
        print("Exiting Xylo Calendar...")

def writeToSaveFile(app):
    pass

def calendarMode_rightPressed(app, event):
    '''
    create new event if right click mouse in calendar
    '''
    x, y = event.x, event.y

    if mouseOnEvent(app, x, y) == None and not app.eventEditing and \
        app.eventInterleaving == None:
        createEvent(app, x, y)

def calendarMode_mousePressed(app, event):
    '''
    check where mouse is on view
        - if on event, select event
        - if on calendar and an event is selected, deselect the event.
    '''
    x, y = event.x, event.y
    if mouseInCalendar(app, x, y) and app.eventInterleaving == None:
        if app.eventEditing and mouseInEditing(app, x, y):
            app.editingMode = mouseInMode(app, x, y)
        else: 
            dayClicked = mouseOnDay(app, x, y)
            clickedEvent = mouseOnEventForDay(app, x, y, dayClicked)
            if clickedEvent != None:
                deselectEvent(app)
                selectEvent(app, clickedEvent, dayClicked, y)
                app.draggedPosition = (x, y)
            else:
                deselectEvent(app)
    elif app.eventInterleaving != None:
        if (app.eventInterleaving == 1):
            if mouseInCalendar:
                app.interDayIndex = int((x - app.calendarLeftMargin) / (app.calendarPixelWidth/7))
                app.interDay = app.weekDays[app.interDayIndex]
                app.eventInterleaving = 2
        elif (app.eventInterleaving == 2):
            clickedEvent = mouseInInterEvents(app, x, y)
            if clickedEvent != None:
                app.immutableEvents.add(clickedEvent)
        elif (app.eventInterleaving == 3):
            clickedMode = mouseInInterPanel(app, x, y)
            if clickedMode != None:
                app.interMode = clickedMode
    else:
        deselectEvent(app)
        if mouseOnVolume(app, x, y):
            deselectEvent(app)
            app.volumeOn = not app.volumeOn

def mouseInTasks(app, x, y):
    pass

def mouseInInterPanel(app, x, y):
    if (app.interx0 <= x <= app.interx1) and \
        (app.intery0 <= y <= app.intery1):
        return (y - app.calendarTopMargin) // (app.calendarPixelHeight/2)
    return None

def mouseInInterEvents(app, x, y):
    interDayEvents = app.weekEvents[app.interDay]
    for event in interDayEvents:
        if (event.pixelLeft <= x <= event.pixelRight) and \
            (event.pixelTop <= y <= event.pixelBot):
            return event
    return None

def mouseInEditing(app, x, y):
    return (app.editingx0 <= x <= app.editingx1) and (app.editingy0 <= y <= app.editingy1)

def mouseInMode(app, x, y):
    return (y - app.editingy0) // (app.editingPanelHeight/3)

def createEvent(app, x, y):
    if app.selectedEvent == None:
        dayIndex = int((x - app.calendarLeftMargin) / (app.calendarPixelWidth/7))
        dayClicked = app.weekDays[dayIndex]
        
        proportionCalendar = (y - app.calendarTopMargin) / (app.calendarPixelHeight)
        startInSeconds = app.dayInSeconds*proportionCalendar
        

        startTime = dayClicked + timedelta(seconds = startInSeconds)
        endTime = startTime + timedelta(seconds = 60*60)

        createdEvent = calendarEvent("(no title)", startTime, endTime)

        app.eventsGraph[dayClicked][createdEvent] = set()

        redoColoring = False

        for other in app.weekEvents[dayClicked]:
            if (createdEvent.startTime < other.startTime < createdEvent.endTime) or \
                (createdEvent.startTime < other.endTime < createdEvent.endTime) or \
                    (other.startTime < createdEvent.startTime < createdEvent.endTime < other.endTime):
                app.eventsGraph[dayClicked][other].add(createdEvent)
                app.eventsGraph[dayClicked][createdEvent].add(other)
                redoColoring = True
        
        if redoColoring:
            app.columnColoring[dayClicked] = greedyEventColumnColoring(app.eventsGraph[dayClicked])
            for eventObject in app.weekEvents[dayClicked]:
                datetimeToCalendar(app, eventObject, dayIndex)
        else:
            app.columnColoring[dayClicked][createdEvent] = 0
        datetimeToCalendar(app, createdEvent, dayIndex)

        createdEvent.day = dayIndex

        createdEvent.color = choice(app.colorList)

        app.deselectedColor = createdEvent.color
        app.selectedColor = tuple([app.deselectedColor[i]//4*3 for i in range(3)])
        createdEvent.color = app.selectedColor
        app.selectedEvent = createdEvent

        if app.volumeOn:
            mixer.Sound.play(app.createEventSound)

        app.weekEvents[dayClicked].add(createdEvent)
        

def mouseOnDay(app, x, y):
    '''
    
    '''
    dayIndex = int((x - app.calendarLeftMargin) / (app.calendarPixelWidth/7))
    return app.weekDays[dayIndex]

def mouseInCalendar(app, x, y):
    '''
    return True if mouse is in calendar portion of the view
    return False otherwise
    '''
    return (app.calendarLeftMargin <= x <= app.calendarWidth) and \
        (app.calendarTopMargin <= y <= app.calendarHeight)

def mouseOnVolume(app, x, y):
    '''
    return True if mouse is on a button in view
    return False otherwise
    '''
    return (app.cxVolumeImage - 22.5 < x < app.cxVolumeImage + 22.5) and \
        (app.cyVolumeImage - 15 < y < app.cyVolumeImage + 15)

def mouseOnEventForDay(app, x, y, dayClicked):
    '''
    return the event if mouse is on an event for given day
    return None otherwise
    '''
    for event in app.weekEvents[dayClicked]:
        if (event.pixelLeft <= x <= event.pixelRight) and \
            (event.pixelTop <= y <= event.pixelBot):
            return event
    return None

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
    startAMPM = app.editingStart.strip()[-2:].strip()

    bisectedEnd = app.editingEnd.strip().split(":")
    if len(bisectedEnd) != 2:
        return
    endHour = bisectedEnd[0].strip()
    endMinute = bisectedEnd[1].strip()[:2]
    endAMPM = app.editingEnd.strip()[-2:].strip()

    startTime = deepcopy(app.weekDays[dayNum])
    endTime = deepcopy(app.weekDays[dayNum])
    
    twelveAMBug = False
    
    if startHour.isnumeric() and startMinute.isnumeric() and (startAMPM == "AM" \
        or startAMPM == "PM"):
        startHour = int(startHour)
        startMinute = int(startMinute)
        if (1 <= startHour <= 12) and (0 <= startMinute <= 59):
            if startAMPM == "AM" and startHour == 12:
                startTime = startTime.replace(hour = 0, minute = startMinute)
                twelveAMBug = True
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

    if (startTime != dayDt or twelveAMBug) and endTime != dayDt:
        if endTime > startTime + timedelta(microseconds = 1):
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
    

    event.startTime = app.weekDays[dayIndex] + timedelta(seconds = app.dayInSeconds*((event.pixelTop - app.calendarTopMargin)/app.calendarPixelHeight))
    event.endTime = app.weekDays[dayIndex] + timedelta(seconds = app.dayInSeconds*((event.pixelBot - app.calendarTopMargin)/app.calendarPixelHeight))
    
    event.startTime = event.startTime.replace(microsecond = 0)
    event.endTime = event.endTime.replace(microsecond = 0)
    
    prevDayDt = app.weekDays[event.day]
    currDayDt = app.weekDays[dayIndex]

    prevGraph = app.eventsGraph[prevDayDt]

    if prevGraph[event] != set():
        for other in prevGraph[event]:
            prevGraph[other].remove(event)
        prevGraph.pop(event)

    todayGraph = app.eventsGraph[currDayDt]
    todayGraph[event] = set()

    for other in app.weekEvents[currDayDt] - {event}:
        if (event.startTime < other.startTime < event.endTime) or \
            (event.startTime < other.endTime < event.endTime) or \
                (other.startTime < event.startTime < event.endTime < other.endTime):
            todayGraph[event].add(other)
            todayGraph[other].add(event)
    
    app.columnColoring[prevDayDt] = greedyEventColumnColoring(prevGraph)
    app.columnColoring[currDayDt] = greedyEventColumnColoring(todayGraph)

    app.eventsGraph[currDayDt] = todayGraph
    app.eventsGraph[prevDayDt] = prevGraph
    
    for eventObject in app.weekEvents[prevDayDt]:
        datetimeToCalendar(app, eventObject, event.day)

    event.day = dayIndex

    app.weekEvents[app.weekDays[event.day]].add(event)

    for eventObject in app.weekEvents[currDayDt]:
        datetimeToCalendar(app, eventObject, dayIndex)

def calendarMode_mouseDragged(app, event):
    '''
    if an event is selected, then change dragged position (where dragged event
    will be drawn)
    '''
    x, y = event.x, event.y

    if app.selectedEvent != None and not app.eventEditing and app.eventInterleaving == None:
        app.draggedPosition = (x, y)

def calendarMode_mouseReleased(app, event):
    '''
    if an event is selected, then the selected event is fixed at the x, y 
    position
    '''
    x, y = event.x, event.y

    if app.selectedEvent != None and not app.eventEditing and app.eventInterleaving == None:
        app.draggedPosition = (x, y)

        if app.volumeOn:
            mixer.Sound.play(app.moveEventSound)

        fixEventPosition(app, app.selectedEvent, x, y)

        app.draggedPosition = None

def deleteEvent(app):
    '''
    if there is a selected event
        - change color back to lighter color
    '''
    event = app.selectedEvent

    dayDt = app.weekDays[event.day]

    if event != None:
        app.weekEvents[dayDt].remove(event)
        for other in app.eventsGraph[dayDt][event]:
            app.eventsGraph[dayDt][other].remove(event)
        app.eventsGraph[dayDt].pop(event)
        app.columnColoring[dayDt] = greedyEventColumnColoring(app.eventsGraph[dayDt])
        for other in app.weekEvents[dayDt]:
            datetimeToCalendar(app, other, event.day)

    app.selectedEvent = None
    app.deselectedColor = None
    app.selectedColor = None
    app.draggedPosition = None
    app.selectedProportion = None
    app.eventEditing = False

def calendarMode_keyPressed(app, event):
    if app.selectedEvent != None and app.draggedPosition == None:
        if not app.eventEditing:
            if event.key == "Delete":
                deleteEvent(app)
            if event.key == "Space":
                app.eventEditing = True
                createEditingPanel(app)
        else:
            if event.key == "Enter" or event.key == "Escape":
                if app.volumeOn:
                    mixer.Sound.play(app.editEventSound)
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
    elif app.selectedEvent == None:
        if app.eventInterleaving != None:
            if event.key == "Escape":
                app.eventInterleaving = None
                restartInterleaving(app)
            if app.eventInterleaving == 2:
                if event.key == "Enter":
                    app.eventInterleaving = 3
                    checkSelectionValidity(app)
            elif app.eventInterleaving == 3:
                if app.interMode == 0.0:
                    if event.key in "APM0123456789:":
                        app.interWake += event.key
                    elif event.key == "Delete":
                        app.interWake = app.interWake[:-1]
                    elif event.key == "Space":
                        app.interWake += " "
                elif app.interMode == 1.0:
                    if event.key in "APM0123456789:":
                        app.interSleep += event.key
                    elif event.key == "Delete":
                        app.interSleep = app.interSleep[:-1]
                    elif event.key == "Space":
                        app.interSleep += " "
                if event.key == "Enter":
                    app.eventInterleaving = 4
                    generateSleepTimes(app)
                    generateTimeInterval(app)
                    sliceMutableEvents(app)
                    interleaveEventsRecursively(app)
                    interleave(app)
        elif event.key == "I":
            app.eventInterleaving = 1

def interleave(app):
    '''
    function that goes events and tries to fit them into real number / time
    intervals using datetime methods
    '''
    intervalList = copy(app.intervalList)
    intervalIndex = 0
    eventIndex = 0
    maxIntervalIndex = len(app.intervalList)
    maxEventIndex = len(app.interleavedSlices)
    while(intervalIndex < maxIntervalIndex and eventIndex < maxEventIndex):
        interval = app.intervalList[intervalIndex]
        if (interval[1] - interval[0]).total_seconds() >= 60*65:
            eventName = app.interleavedSlices[eventIndex][0]
            startTime = interval[0] + timedelta(minutes = 5)
            endTime = interval[0] + timedelta(minutes = 65)
            newEventSlice = calendarEvent(eventName, startTime, endTime)
            app.eventsGraph[app.interDay][newEventSlice] = set()
            datetimeToCalendar(app, newEventSlice, app.interDayIndex)
            newEventSlice.day = app.interDayIndex
            newEventSlice.color = app.interleavedSlices[eventIndex][1]
            app.interleavedEvents.add(newEventSlice)
            app.intervalList[intervalIndex][0] += timedelta(minutes = 65)
            eventIndex += 1
        else:
            intervalIndex += 1
    if len(app.interleavedSlices) == len(app.interleavedEvents):
        for event in app.interleavedEvents:
            app.weekEvents[app.interDay].add(event)
        for event in app.mutableEvents:
            app.weekEvents[app.weekDays[event.day]].remove(event)
        
        if app.volumeOn:
            mixer.Sound.play(app.interleaveSound)
        
        restartInterleaving(app)
    else:
        restartInterleaving(app)

def interleaveEventsRecursively(app):
    app.interleavedSlices = interleaveEventsHelper(app.slicedEvents)

def interleaveEventsHelper(dictOfLists):
    someEmpty = False
    emptyLists = {}
    for l in dictOfLists:
        if len(dictOfLists[l]) == 0:
            someEmpty = True
            emptyLists[l] = dictOfLists[l]
    nonEmptyDict = {n:l for n,l in dictOfLists.items() if n not in emptyLists}
    if someEmpty:
        return interleaveEventsHelper(nonEmptyDict)
    elif len(nonEmptyDict) == 1:
        for key in nonEmptyDict:
            return nonEmptyDict[key]
    elif len(nonEmptyDict) == 0:
        return []
    else:
        interleavingList = []
        newDictOfLists = dict()
        for l in dictOfLists:
            interleavingList.append(dictOfLists[l][0])
            newDictOfLists[l] = dictOfLists[l][1:]
        interleavingList += interleaveEventsHelper(newDictOfLists)
        return interleavingList

def sliceMutableEvents(app):
    for event in app.mutableEvents:
        totalSeconds = (event.endTime - event.startTime).total_seconds()
        totalHours = totalSeconds/60/60
        ceilingHours = ceil(totalHours)
        slicedEventList = []
        for slice in range(ceilingHours):
            slicedEventList.append((f"{event.summary} #{slice+1}", event.color))
        app.slicedEvents[event] = slicedEventList

def generateTimeInterval(app):
    midnight = deepcopy(app.interDay)

    prevConflicts = True
    prevTime = None
    currConflicts = False
    firstOut = None
    for fiveMins in range(12*24):
        currTime = midnight + timedelta(minutes = fiveMins*5)
        for event in app.immutableEvents:
            if event.startTime <= currTime <= event.endTime:
                currConflicts = True
                break
        
        if not currConflicts and prevConflicts:
            firstOut = currTime
        elif not currConflicts and not prevConflicts:
            if firstOut != prevTime:
                app.intervalList[-1][-1] = currTime
            else:
                app.intervalList.append([firstOut, currTime])
        prevTime = currTime
        prevConflicts = currConflicts
        currConflicts = False

def generateSleepTimes(app):
    bisectedWake = app.interWake.strip().split(":")
    if len(bisectedWake) != 2:
        restartInterleaving(app)
    wakeHour = bisectedWake[0].strip()
    wakeMinute = bisectedWake[1].strip()[:2]
    wakeAMPM = app.interWake.strip()[-2:].strip()

    bisectedSleep = app.interSleep.strip().split(":")
    if len(bisectedSleep) != 2:
        restartInterleaving(app)
    sleepHour = bisectedSleep[0].strip()
    sleepMinute = bisectedSleep[1].strip()[:2]
    sleepAMPM = app.interSleep.strip()[-2:].strip()
    
    wakeTime = deepcopy(app.interDay)
    sleepTime = deepcopy(app.interDay)
    
    if wakeHour.isnumeric() and wakeMinute.isnumeric() and (wakeAMPM == "AM" \
        or wakeAMPM == "PM"):
        wakeHour = int(wakeHour)
        wakeMinute = int(wakeMinute)
        if (1 <= wakeHour <= 12) and (0 <= wakeMinute <= 59):
            if wakeAMPM == "AM" and wakeHour == 12:
                wakeTime = wakeTime.replace(hour = 0, minute = wakeMinute)
            elif wakeAMPM == "AM":
                wakeTime = wakeTime.replace(hour = wakeHour, minute = wakeMinute)
            elif wakeAMPM == "PM" and wakeHour == 12:
                wakeTime = wakeTime.replace(hour = 12, minute = wakeMinute)
            elif wakeAMPM == "PM":
                wakeTime = wakeTime.replace(hour = wakeHour + 12, minute = wakeMinute)

    if sleepHour.isnumeric() and sleepMinute.isnumeric() and (sleepAMPM == "AM" \
        or sleepAMPM == "PM"):
        sleepHour = int(sleepHour)
        sleepMinute = int(sleepMinute)
        if (1 <= sleepHour <= 12) and (0 <= sleepMinute <= 59):
            if sleepAMPM == "AM" and sleepHour == 12:
                sleepTime = sleepTime.replace(hour = 0, minute = sleepMinute)
            elif sleepAMPM == "AM":
                sleepTime = sleepTime.replace(hour = sleepHour, minute = sleepMinute)
            elif sleepAMPM == "PM" and sleepHour == 12:
                sleepTime = sleepTime.replace(hour = 12, minute = sleepMinute)
            elif sleepAMPM == "PM":
                sleepTime = sleepTime.replace(hour = (sleepHour + 12), minute = sleepMinute)

    if wakeTime != app.interDay and sleepTime != app.interDay:
        if sleepTime > wakeTime:
            sleep1 = calendarEvent("sleep", app.interDay, wakeTime)
            sleep2 = calendarEvent("sleep", sleepTime, app.interDay.replace(hour = 23, minute = 59))

            app.immutableEvents.add(sleep1)
            app.immutableEvents.add(sleep2)

def checkSelectionValidity(app):
    for event in app.weekEvents[app.interDay]:
        if event not in app.immutableEvents:
            app.mutableEvents.add(event)
    if len(app.mutableEvents) < 2:
        restartInterleaving(app)
    else:
        createInterPanel(app)

def restartInterleaving(app):
    app.eventInterleaving = None
    app.interDay = None
    app.interDayIndex = None
    app.immutableEvents = set()
    app.mutableEvents = set()
    app.interx0 = None
    app.interx1 = None
    app.intery0 = None
    app.intery1 = None
    app.interMode = None
    app.interWake = "6 : 00 AM"
    app.interSleep = "11 : 59 PM"
    app.intervalList = []
    app.slicedEvents = dict()
    app.interleavedSlices = []
    app.interleavedEvents = set()

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

    while(get_pil_text_size(nameText, 15, "fonts/arial.ttf")[0] > (app.calendarPixelWidth/7*2 - 55)):
            nameText = nameText[:-1]

    if nameText != calendarEvent.summary:
        nameText += "…"
    
    app.editingName = nameText

def createInterPanel(app):
    app.interx0 = app.calendarLeftMargin + int(app.calendarPixelWidth/7*app.interDayIndex)
    app.interx1 = app.calendarLeftMargin + int(app.calendarPixelWidth/7*(app.interDayIndex+1))
    app.intery0 = app.calendarTopMargin
    app.intery1 = app.calendarHeight

def calendarMode_sizeChanged(app):
    pass

def calendarMode_mouseMoved(app, event):
    pass

def calendarMode_redrawAll(app, canvas):
    drawCalendar(app, canvas)
    # drawTasks(app, canvas)

def drawCalendar(app, canvas):
    drawWeekBackground(app, canvas)
    drawWeekEvents(app, canvas)
    drawDraggedEvent(app, canvas)
    drawEditingPanel(app, canvas)
    drawInterleaving(app, canvas)
    drawVolumeButton(app, canvas)

def drawVolumeButton(app, canvas):
    if app.volumeOn:
        canvas.create_image(app.cxVolumeImage, app.cyVolumeImage, \
            image=ImageTk.PhotoImage(app.volumeOnImage))
    else:
        canvas.create_image(app.cxVolumeImage, app.cyVolumeImage, \
            image=ImageTk.PhotoImage(app.volumeOffImage))

def drawInterleaving(app, canvas):
    drawSelectedDay(app, canvas)
    drawSelectedEvents(app, canvas)
    drawInterleavingPanel(app, canvas)

def drawInterleavingPanel(app, canvas):
    if app.eventInterleaving == 3:
        canvas.create_rectangle(app.interx0, app.intery0, app.interx1, app.intery1, fill = app.interPanelColor, 
                                width = 0)

        if app.interMode == 0.0:
            canvas.create_rectangle(app.interx0, app.intery0, app.interx1, app.intery0 + app.calendarPixelHeight/2,\
                fill = app.interPanelBorderColor, width = 0)
        elif app.interMode == 1.0:
            canvas.create_rectangle(app.interx0, app.intery0 + app.calendarPixelHeight/2, app.interx1, app.intery1,\
                fill = app.interPanelBorderColor, width = 0)
        
        canvas.create_text(app.interx0 + app.calendarEditMargin//2, app.intery0 + app.calendarEditMargin//2, \
            text = "Wake up time: ", anchor = "nw", fill = app.calendarOuterFont, font = "Arial 15")
        canvas.create_text(app.interx0 + app.calendarEditMargin//2, app.intery0 + app.calendarEditMargin//2 + 20, \
            text = app.interWake, anchor = "nw", fill = app.calendarInnerFont, font = "Arial 15 bold")

        canvas.create_text(app.interx0 + app.calendarEditMargin//2, app.intery0 + app.calendarPixelHeight/2 + app.calendarEditMargin//2, \
            text = "Sleep time: ", anchor = "nw", fill = app.calendarOuterFont, font = "Arial 15")
        canvas.create_text(app.interx0 + app.calendarEditMargin//2, app.intery0 + app.calendarPixelHeight/2 + app.calendarEditMargin//2 + 20, \
            text = app.interSleep, anchor = "nw", fill = app.calendarInnerFont, font = "Arial 15 bold")
        
        canvas.create_line(app.interx0, app.intery0+ app.calendarPixelHeight/2, \
                app.interx1, app.intery0+ app.calendarPixelHeight/2, fill = app.interPanelBorderColor)

def drawSelectedEvents(app, canvas):
    if app.eventInterleaving == 2:
        for event in app.immutableEvents:
            displayColor = tuple([event.color[i]//4*3 for i in range(3)])
            if app.toggleRoundedRectangle:
                drawRoundRectangle(canvas, event.pixelLeft + .5, event.pixelTop, \
                        event.pixelRight, event.pixelBot, fill = fromRGBtoHex(displayColor), \
                            width = 0)
            else:
                canvas.create_rectangle(event.pixelLeft + .5, event.pixelTop, 
                                        event.pixelRight, event.pixelBot, 
                                        fill = fromRGBtoHex(displayColor),
                                        width = 0)
            if len(event.summary) >= 19:
                    eventText = event.summary[:18] + "…"
            else:
                eventText = event.summary
                
            canvas.create_text(event.pixelLeft + 2, event.pixelTop, 
                            text = eventText, anchor = "nw",
                            fill = app.calendarInnerFont, font = "Arial 12")

def drawSelectedDay(app, canvas):
    if app.eventInterleaving == 2:
        x0 = app.calendarLeftMargin + int(app.calendarPixelWidth/7*app.interDayIndex)
        x1 = app.calendarLeftMargin + int(app.calendarPixelWidth/7*(app.interDayIndex+1))
        y0 = app.calendarTopMargin
        y1 = app.calendarHeight
        canvas.create_rectangle(x0, y0, x1, y1, fill = None, width = 3, 
                                outline = app.interDayColor)

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
        
        x0 = app.editingx0
        x1 = app.editingx1
        y0 = app.editingy0
        y1 = app.editingy1
        
        if dayNum >= 3:
            '''
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
            '''

            points = [x0, y0, x1, y0, x1, z - 10, x1 + app.calendarEditMargin, z, \
            x1, z + 10, x1, y1, x0, y1]
            
        else:
            '''
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
            '''

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


def drawRoundRectangle(canvas, x1, y1, x2, y2, radius=3, **kwargs):
    '''
    my own rounded rectangle drawing function (draws 4 circles and 2 rectangles
    for each rounded rectangle)
    '''
    canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, **kwargs)
    canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, **kwargs)
    canvas.create_oval(x1, y1, x1 + radius*2, y1 + radius*2, **kwargs)
    canvas.create_oval(x2 - radius*2, y1, x2, y1 + radius*2, **kwargs)
    canvas.create_oval(x2 - radius*2, y2 - radius*2, x2, y2, **kwargs)
    canvas.create_oval(x1, y2 - radius*2, x1 + radius*2, y2, **kwargs)
    
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

        if app.toggleRoundedRectangle:
            drawRoundRectangle(canvas, dragPixelLeft + .5, dragPixelTop, \
                    dragPixelRight, dragPixelBot, fill = fromRGBtoHex(event.color), \
                        width = 0)
        else:
            canvas.create_rectangle(dragPixelLeft + .5, dragPixelTop, 
                                    dragPixelRight, dragPixelBot, 
                                    fill = fromRGBtoHex(event.color),
                                    width = 0)
        
        if len(event.summary) >= 19:
            eventText = event.summary[:18] + "…"
        else:
            eventText = event.summary
            

        canvas.create_text(dragPixelLeft + 3, dragPixelTop + 1, 
                            text = eventText, anchor = "nw",
                            fill = app.calendarOuterFont, font = "Arial 12")

        canvas.create_text(dragPixelLeft + 2, dragPixelTop, 
                        text = eventText, anchor = "nw",
                        fill = app.calendarInnerFont, font = "Arial 12")


def drawWeekEvents(app, canvas):
    for index in range(7):
        weekDay = app.weekDays[index]
        for event in app.weekEvents[weekDay]:
            if app.toggleRoundedRectangle:
                drawRoundRectangle(canvas, event.pixelLeft + .5, event.pixelTop, \
                    event.pixelRight, event.pixelBot, fill = fromRGBtoHex(event.color), \
                        width = 0)
            else:
                canvas.create_rectangle(event.pixelLeft + .5, event.pixelTop, 
                                    event.pixelRight, event.pixelBot, 
                                    fill = fromRGBtoHex(event.color),
                                    width = 0)
            maxLength = 19//(event.totalCols)
            if len(event.summary) >= maxLength:
                eventText = event.summary[:(maxLength-1)] + "…"
            else:
                eventText = event.summary

            canvas.create_text(event.pixelLeft + 3, event.pixelTop + 1, 
                            text = eventText, anchor = "nw",
                            fill = app.calendarOuterFont, font = "Arial 12")

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
        monthDayColor = app.calendarTopFont

        circleRadius = 24

        monthDayBotYPos = app.calendarTopMargin - 30

        if dayDt == app.today:
            canvas.create_oval(dayPixel - circleRadius, monthDayBotYPos - circleRadius,
                               dayPixel + circleRadius, monthDayBotYPos + circleRadius,
                               fill = app.todayTrackersColor, width = 0)
            monthDayColor = app.calendarBgColor

        canvas.create_text(dayPixel, monthDayBotYPos - 36.7, text = textWeekDay,
                           fill = app.calendarTopFont, font = "Arial 14")

        canvas.create_text(dayPixel, monthDayBotYPos, text = textMonthDay,
                           fill = monthDayColor, font = "Arial 26")

        canvas.create_line(int(app.calendarLeftMargin + app.calendarPixelWidth/7*day), 
            app.calendarTopMargin*7//9, int(app.calendarLeftMargin + app.calendarPixelWidth/7*day), 
            app.calendarHeight, fill = app.calendarFgColor, width = .5)

    for hour in range(1, 25, 2):
        hourPixel = int(app.calendarPixelHeight/24*hour + app.calendarTopMargin)
        canvas.create_line(app.calendarLeftMargin/7*6, hourPixel, \
            app.calendarWidth, hourPixel, fill = app.calendarFgColor, width = .5)
        if hour != app.hourObstructing:
            
            if hour < 12: 
                hourText = f"{hour}  AM"
            elif hour == 12:
                hourText = f"{hour}  PM"
            else:
                hourText = f"{hour%12}  PM"

            canvas.create_text(app.calendarLeftMargin/4*3, hourPixel, \
                text = hourText, fill = app.calendarOuterFont, font = "Arial 11",
                anchor = "e")

    canvas.create_text(app.calendarMonthYearX, app.calendarMonthYearY, 
                       anchor = "e", text = app.monthText, font = "Arial 30 bold",
                       fill = app.calendarTopFont)

    canvas.create_text(app.calendarMonthYearX, app.calendarMonthYearY, 
                       anchor = "w", text = f" {app.yearText}", font = "Arial 30",
                       fill = app.calendarTopFont)

    canvas.create_line(app.calendarLeftMargin/7*6, app.currentTimePixel, \
        app.calendarWidth, app.currentTimePixel, fill = app.todayTrackersColor, 
        width = .5)

    canvas.create_text(app.calendarLeftMargin/4*3, app.currentTimePixel, \
        text = app.currentTimeString, fill = app.todayTrackersColor, font = "Arial 11",
        anchor = "e")

################################################################################
# post-tp3 task experimentation
################################################################################

def createTask(app, x, y):
    # assuming that no event is selected… 
    # if app.taskMode (preface all parts of tasks)
        # dayIndex = int((x - app.calendarLeftMargin) / (app.calendarPixelWidth/7))
        # dayClicked = app.weekDays[dayIndex]
        # create list of all tasks (so popping can happen), but also store them inside
        
        # just check to see if mouse is on tasks before events… so that if it is
        # on both, you override and select task, and also implement deselectTask
        # to be in every place that 
        
        # the events dictionary
    pass


def drawTasks(app, canvas):
    drawTasksOnCalendar(app, canvas)
    drawTasksWindow(app, canvas)

def drawTasksOnCalendar(app, canvas):
    '''
    task experimentation……… will be implemented post-tp3 on my own time
    '''
    ypos = 400
    for y in range(1,2):
        # color = fromRGBtoHex(app.colorList[y])
        # color = fromRGBtoHex((202, 171, 106))
        # color = fromRGBtoHex((83, 131, 236))
        # color = app.calendarOuterFont
        # color = "white"
        color = app.todayTrackersColor
        ypos += 360*y
        radius = 8

        # canvas.create_line(app.calendarLeftMargin + app.calendarPixelWidth/7*3,
        #                 ypos, app.calendarLeftMargin + app.calendarPixelWidth/7*4 - 5, ypos,
        #                 fill = "white", width = 4)
        cx = app.calendarLeftMargin + app.calendarPixelWidth/7*4 - radius
        cy = ypos
        # canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill = color, width = 0)
        # canvas.create_text(cx + 1, cy + 1, text = "1", fill = app.calendarOuterFont, font = "Arial 12", anchor = "center")
        # canvas.create_text(cx, cy, text = "1", fill = "white", font = "Arial 12", anchor = "center")

    for task in app.weekTasks:
        pass

def drawTasksWindow(app, canvas):
    drawTasksBackground(app, canvas)
    drawTasksOnList(app, canvas)

def drawTasksBackground(app, canvas):
    canvas.create_rectangle(app.tasksLeftMargin, 0,
                            app.tasksWidth, app.tasksHeight, 
                            fill = app.tasksBgColor, width = 0)
    canvas.create_line(app.tasksLeftMargin, 0,
                       app.tasksLeftMargin, app.tasksHeight, 
                       fill = app.tasksFgColor, width = 2)

def drawTasksOnList(app, canvas):
    pass

if __name__ == "__main__":
    runApp(width=1400, height=800)