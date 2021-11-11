from cmu_112_graphics import *

def appStarted(app):
    ###################################################
    # board and cell attributes
    ###################################################
    
    app.rows = 10
    app.cols = 20

    app.cellSize = min(app.width//app.cols, app.height//app.rows)

        # app.margins = 50

    app.defColor = "white"

    # TESTING SHIT
    app.board = [[app.defColor for col in range(app.cols)] for row in range(app.rows)]
    for col in range(0, app.cols, 2):
        for row in range(app.rows//3, app.rows//3*2):
            app.board[row][col] = "gray"

    ###################################################
    # dragging cell attributes
    ###################################################

    app.draggingCell = None

    app.draggingColor = None

    app.draggingPosition = None

    app.isDragging = False


    ###################################################
    # major testing attributes
    ###################################################

    # app.timerDelay = 50

    # app.test = None

def timerFired(app):
    pass
    # app.position += 1

def appStopped(app):
    pass

def inWhichCell(app, x, y):
    # need to implement margins at some point
    return y//app.cellSize, x//app.cellSize

def inBoardBounds(app, x, y):
    return (0 <= x <= app.cols*app.cellSize) and \
        (0 <= y <= app.rows*app.cellSize)

def mousePressed(app, event):
    x, y = event.x, event.y
    # also probably check if clicked special edit button(s?)
    if inBoardBounds(app, x, y):
        row, col = inWhichCell(app, x, y)
        if app.board[row][col] != app.defColor:
            app.draggingColor = app.board[row][col]
            app.isDragging = True
            app.draggingCell = (row, col)
            app.board[row][col] = app.defColor
            app.draggingPosition = (x, y)
    # need to implement margins at some point


def mouseDragged(app, event):
    x, y = event.x, event.y
    app.draggingPosition = (x, y)
    # darkening color?
    
def mouseReleased(app, event):
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

def mouseMoved(app, event):
    pass
    # x, y = event.x, event.y
    # app.test = (x,y)

def sizeChanged(app):
    pass


def drawCell(app, canvas, row, col):
    cellColor = app.board[row][col]
    canvas.create_rectangle(app.cellSize*col, app.cellSize*row, \
        app.cellSize*(col+1), app.cellSize*(row+1), fill = cellColor)

def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col)

def drawDraggingCell(app, canvas):
    if app.draggingColor != None:
        x, y = app.draggingPosition
        halfSize = app.cellSize//2
        canvas.create_rectangle(x - halfSize, y - halfSize, \
            x + halfSize, y + halfSize, fill = app.draggingColor)

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawDraggingCell(app, canvas)
    # if app.test != None:
    #     x, y = app.test
    #     canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill = "black")
    # canvas.create_oval(app.width//2 - 20, app.height - 20 - app.position, \
    #     app.width//2 + 20, app.height + 20 - app.position, fill = "black")

runApp(width=1000, height=500)