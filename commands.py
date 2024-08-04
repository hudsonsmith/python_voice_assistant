import time
import subprocess
import datetime as dt
import psutil
import pyttsx3
import pyautogui
import speech_recognition as sr
import pytesseract
from PIL import Image, ImageDraw
import mss
import numpy as np
from bs4 import BeautifulSoup
import requests
import APOLLO

pyautogui.FAILSAFE = False

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()


def screenSpecs():
        return screenWidth, screenHeight, currentMouseX, currentMouseY

def moveCursor(x, y):
        pyautogui.moveTo(x, y)

def rightClick(x,y):
        moveCursor(x,y)
        pyautogui.rightClick()

def leftClick(x,y):
        moveCursor(x, y)
        pyautogui.leftClick()

def write(text):
        pyautogui.write(text)

def drag(x,y):
        pyautogui.dragTo(x,y)

def press(key):
        pyautogui.press(key)

def scroll(clicks):
        pyautogui.scroll(clicks)

def wait(seconds):
        time.sleep(seconds)

def useSubprocess(lis):
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
        time.sleep(3)
        pyautogui.write(app_name)
        time.sleep(3)
        pyautogui.press('enter')
        time.sleep(3)
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


def speak(text, gender):
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        if gender == "Female":
            i = 1
        else:
            i = 0
        engine.setProperty('voice', voices[i].id)
        engine.say(text)
        engine.runAndWait()

def askQuestion(query):
        speak(query,"Male")
        return getCommand()

def getCommand():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language="en-US")
            except:
                query = ""
        return query.lower()

def doNothing():
        pass

def capture_screen():
        with mss.mss() as sct:
            screenshot = sct.grab(sct.monitors[0])
            img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
            return img

def preprocess_image(img):
        img_gray = img.convert('L')
        img_np = np.array(img_gray)
        return img_np

def draw_boxes(img, boxes, data):
        draw = ImageDraw.Draw(img)
        for i, box in enumerate(boxes):
            if data['text'][i] != '':
                draw.rectangle(box, outline="red", width=2)
        return img

def detect_text(img):
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang='eng')
        boxes = []
        ocr_list = []
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 80:
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                boxes.append((x, y, x + w, y + h))
                cx = x + w / 2
                cy = y + h / 2
                ocr_list.append([data['text'][i],(cx,cy)])
        return boxes, data, ocr_list

def screenshotOcr():
        screen_img = capture_screen()
        preprocessed_img = preprocess_image(screen_img)
        text_boxes, data,  ocr_list = detect_text(preprocessed_img)
        image = draw_boxes(screen_img, text_boxes, data)
        image_path = "screenshotForApollo.png"
        image.save(image_path)
        return image_path, ocr_list

def taskDone():
        APOLLO.tDone = True


def webScrape(link):
    r = requests.get('link')

    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find('div', class_='entry-content')
    content = s.find_all('p')
    APOLLO.memoryStorage += f""" Results of scraping {link}:

    {content}
    """
