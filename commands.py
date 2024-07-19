import pyautogui
import time
import subprocess
import os
import pygetwindow as gw
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from screen_brightness_control import set_brightness
import requests
from bs4 import BeautifulSoup



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

def wait(seconds):
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

def doubleClick():
    pyautogui.rightClick()
    pyautogui.rightClick()

def open_application(app_name):
    pyautogui.press('win')
    pyautogui.write(app_name)
    pyautogui.press('enter')
def use_searchBar(query):
    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("l")
    pyautogui.keyUp("l")
    pyautogui.keyUp("ctrl")
    pyautogui.write(query)
    pyautogui.press("enter")
def screenshot():
    image = pyautogui.screenshot()
    image_path = "screenshot.png"
    image.save(image_path)
    return image_path
