import pyautogui
import time
import os
import subprocess

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()

def screenSpecs():
    return screenWidth, screenHeight, currentMouseX, currentMouseY

def moveCursor(x,y):
    pyautogui.moveTo(x,y)

def rightClick():
    pyautogui.rightClick()

def leftClick():
    pyautogui.leftClick()

def write(text):
    pyautogui.write(text)

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
