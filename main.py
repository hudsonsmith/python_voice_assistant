import struct

import speech_recognition as sr
import pyaudio
import pyttsx3
import time
import pvporcupine

Active = False
afkCounter = 0

def speak(text, gender):
     engine = pyttsx3.init('sapi5')
     voices = engine.getProperty('voices')
     if gender == "Female":
         i = 1
     else:
         i = 0
     engine.setProperty('voice',voices[i].id)
     print("APOLLO:" + text + "\n")
     engine.say(text)
     engine.runAndWait()
def getCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source=source)
        try:
            query = r.recognize_google(audio, language = "en-US")
        except Exception as e:
            query = ""
    return query.lower()

def doTask():
    print("Placeholder")
def runner(afkCounter,Active):
    while True:
        command = getCommand()
        print("User:" + command + "\n")
        if Active:
            doTask()
        if "apollo" in command:
            speak("How may I help you?", "Male")
            Active = True
        elif "bye" in command:
            speak("Going to sleep.", "Male")
            Active = False
        elif afkCounter > 30 and Active == True:
            speak("Going to sleep.", "Male")
            Active = False



runner(afkCounter,Active)
