import time
import subprocess
import datetime as dt
import psutil
import pyttsx3
import wmi
import pyautogui
from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup
import speech_recognition as sr



f = wmi.WMI()

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()

def screenSpecs():
    return screenWidth, screenHeight, currentMouseX, currentMouseY

def moveCursor(x, y):
    x = (x / 100) * screenWidth
    y = (y / 100) * screenHeight
    pyautogui.moveTo(x, y)

def rightClick():
    pyautogui.rightClick()

def leftClick():
    pyautogui.leftClick()

def write(text):
    pyautogui.write(text)

def drag(x,y):
    x = (x/100)*screenWidth
    y = (y/100)*screenHeight
    pyautogui.dragTo(x,y)

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
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(5)
def use_searchBar(query):
    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("l")
    pyautogui.keyUp("l")
    pyautogui.keyUp("ctrl")
    pyautogui.write(query + " ")
    pyautogui.press("enter")
def screenshot():
    image = pyautogui.screenshot()
    image_path = "screenshotForApollo.png"
    image.save(image_path)
    return image_path


def screenshot_with_grid():
    image = pyautogui.screenshot()
    draw = ImageDraw.Draw(image)

    step_size = 60

    for x in range(0, screenWidth, step_size):
        line = ((x, 0), (x, screenHeight))
        draw.line(line, fill=128)

    for y in range(0, screenHeight, step_size):
        line = ((0, y), (screenWidth, y))
        draw.line(line, fill=128)

    for x in range(0, screenWidth, step_size):
        for y in range(0, screenHeight, step_size):
            draw.text((x + 5, y + 5), f'({round(x / screenWidth * 100,1)}, {round(y / screenHeight * 100,1)})', fill=128)

    image_path = "screenshotForApolloGridded.png"
    image.save(image_path)
    return image_path

def currTime():
    return dt.datetime.now()

def currCpu():
    return psutil.cpu_percent()

def currRam():
    return psutil.virtual_memory().percent

def currApps():
    openApps = ""
    for process in f.Win32_Process():
        openApps+= " " + process.Name
    return openApps

def speak(text, gender):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    if gender == "Female":
        i = 1
    else:
        i = 0
    engine.setProperty('voice', voices[i].id)
    print("[APOLLO] " + text)
    engine.say(text)
    engine.runAndWait()

def askQuestion(query):
    speak(query,"Male")
    return getCommand()

def webScrape(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', class_='entry-content')
    content = s.find_all('p')
    return content

def getCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-US")
        except:
            query = ""
    return query.lower()
