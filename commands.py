import pyautogui as pg

screenWidth, screenHeight = pg.size()
currentMouseX, currentMouseY = pg.position()

def screenSpecs():
    return screenWidth, screenHeight, currentMouseX, currentMouseY

def moveCursor(x,y):
    pg.moveTo(x,y)

def rightClick():
    pg.rightClick()

def leftClick():
    pg.leftClick()

def write(text):
    pg.write(text)

def press(key):
    pg.press(key)

def scroll(clicks):
    pg.scroll(clicks)

