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
    # datetime backend
    ###########################################################################

    weekDatetimeBackendSetup(app, 0)


def weekDatetimeBackendSetup(app, deltaWeek):
    '''
    setup week dictionary from month objects based on current week (taking
    inputs from user for switching weeks)
    '''
    todayDt = datetime.now(tz = None) + deltaWeek * timedelta(weeks = 1)
    todayNum = app.autoTodayDt.isoweekday()
    app.lastSunday = todayDt - timedelta(days = (todayNum))
    
    app.weekIndexes = []
    app.weekEventsDict = icalendarLibraryTests2()
    for day in range(7):
        currentDate = app.lastSunday + timedelta(days = day)
        


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