from cmu_112_graphics import *

def appStarted(app):
    pass

def timerFired(app):
    pass

def appStopped(app):
    pass

def keyPressed(app, event):
    pass

def keyReleased(app, event):
    pass

def mousePressed(app, event):
    pass

def mouseReleased(app, event):
    pass

def mouseMoved(app, event):
    pass

def mouseDragged(app, event):
    pass

def sizeChanged(app):
    pass

def redrawAll(app, canvas):
    canvas.create_rectangle(10, 10, app.width - 10, app.height - 10, fill = "orange")

runApp(width=600, height=600)