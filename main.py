from cmu_112_graphics import *

def appStarted(app):
    app.rows = 5
    app.cols = 5

    app.cellSize = min(app.width//app.cols, app.height//app.rows)

    # app.margins = 50

    app.defColor = "white"

    app.board = [[defColor for col in range(app.cols)] for row in range(app.rows)]

def timerFired(app):
    pass

def appStopped(app):
    pass

def inWhichCell(app, x, y):
    # need to implement margins at some point
    return y//app.cellSize, x//app.cellSize

def keyPressed(app, event):
    x, y = event.x, event.y
    # also probably check if clicked special edit button(s?)
    if 0 <= x <= app.cols*app.cellSize and 0 <= y <= app.rows:
        row, col = inWhichCell(app, x, y)
        app.board[row][col] = app.defColor
    # need to implement margins at some point

def mouseDragged(app, event):
    pass

def mouseReleased(app, event):
    pass

def keyReleased(app, event):
    pass

def mousePressed(app, event):
    pass

def mouseMoved(app, event):
    pass

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

def redrawAll(app, canvas):
    drawBoard(app, canvas)

runApp(width=600, height=600)