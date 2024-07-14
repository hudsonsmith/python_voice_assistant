import pyautogui
import time
import subprocess

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()

def screenSpecs():
    return screenWidth, screenHeight, currentMouseX, currentMouseY

def moveCursor(x, y):
    pyautogui.moveTo(x, y)

def rightClick():
    pyautogui.rightClick()

def leftClick():
    pyautogui.leftClick()

def write(text):
    pyautogui.write(text)

def drag(x, y):
    pyautogui.dragTo(x, y)

def press(key):
    pyautogui.press(key)

def scroll(clicks):
    pyautogui.scroll(clicks)

def sleep(seconds):
    time.sleep(seconds)

def subprocessTwo(lis):
    process = subprocess.Popen(lis, shell=True)
    process.wait()

def keyDown(key):
    pyautogui.keyDown(key)

def keyUp(key):
    pyautogui.keyUp(key)

def hotkey(tup):
    pyautogui.hotkey(tup)

def screenshot():
    image = pyautogui.screenshot()
    image_path = "screenshot.png"
    image.save(image_path)
    return image_path
