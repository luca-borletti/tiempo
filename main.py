from cmu_112_graphics import *
from datetime import *


###############################################################################
# OOP for calendar
###############################################################################

class event(object):
    def __init__(self, summary, startTime, endTime):
        self.summary = summary
        self.startTime = startTime
        self.endTime = endTime

    def __repr__(self):
        return f"{self.summary}. From {str(self.startTime)} to {str(self.endTime)}"


concepts = event("15-151 Discrete Mathematics", \
    datetime(2021, 11, 11, 13, 25), datetime(2021, 11, 11, 14, 15))






###############################################################################
# calendar graphics
###############################################################################

def appStarted(app):
    ###########################################################################
    # 
    ###########################################################################
    
    app.defColor = fromRGBtoHex((255,255,255))







    # !!!!!!DEPRECATED!!!!!! cell selection attributes

    app.isSelecting = False

    app.selectedCell = None

    app.unselectedColor = None

    app.selectedColor = None

    # !!!!!!DEPRECATED!!!!!! cell dragging attributes

    app.draggingCell = None

    app.draggingColor = None

    app.draggingPosition = None

    app.isDragging = False

    

def fromHextoRGB(hexString):
    hexVals = [hexString[2*i+1: 2*(i+1)+1] for i in range(3)]
    rgbTuple = tuple(int(hexVals[i], 16) for i in range(3))
    return rgbTuple

def fromRGBtoHex(rgbTuple):
    red, green, blue = rgbTuple
    hexString = f'#{red:02x}{green:02x}{blue:02x}'
    return hexString

def timerFired(app):
    pass
    # app.position += 1

def appStopped(app):
    pass

def mousePressed(app, event):

    return

    # !!!!!!DEPRECATED!!!!!!

    x, y = event.x, event.y
    # also probably check if clicked special edit button(s?)
    if inBoardBounds(app, x, y):
        row, col = inWhichCell(app, x, y)
        if app.board[row][col] != app.defColor:
            if not app.isSelecting:
                selectCell(app, row, col)
            else:
                deselectCell(app)
                selectCell(app, row, col)
            app.draggingColor = app.board[row][col]
            app.isDragging = True
            app.draggingCell = (row, col)
            app.board[row][col] = app.defColor
            app.draggingPosition = (x, y)
        else:
            deselectCell(app)
    else:
        deselectCell(app)


def mouseDragged(app, event):
    
    
    return
    
    # !!!!!!DEPRECATED!!!!!!

    x, y = event.x, event.y
    app.draggingPosition = (x, y)
    
def mouseReleased(app, event):
    
    return

    # !!!!!!DEPRECATED!!!!!!
    
    x, y = event.x, event.y
    if app.isDragging:
        app.isDragging = False
        if inBoardBounds(app, x, y): # and not another taken up cell?
            newRow, newCol = inWhichCell(app, x, y)
            if app.board[newRow][newCol] == app.defColor:
                app.board[newRow][newCol] = app.draggingColor
            else:
                row, col = app.draggingCell
                app.board[row][col] = app.draggingColor
        else:
            row, col = app.draggingCell
            app.board[row][col] = app.draggingColor
        app.draggingColor = None
        app.draggingPosition = None
        app.draggingCell = None


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
    pass