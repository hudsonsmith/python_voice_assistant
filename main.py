import struct

import speech_recognition as sr
import pyaudio
import pyttsx3
import time
import pvporcupine
import APOLLO

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

def doTask(command):
    if "i command you" in command:
        return APOLLO.outputCommands(command)
    else:
        return APOLLO.output(command)
def runner(afkCounter,Active):
    while True:
        command = getCommand()
        print("User:" + command + "\n")
        if Active:
            if command != "":
                out = doTask(command)
                if "i command you" not in command:
                    speak(out.content,"Male")
            else:
                afkCounter+=1
        if "that will be all" in command:
            speak("Going to sleep.", "Male")
            Active = False
            afkCounter = 0
        elif "apollo" in command:
            speak("How may I help you?", "Male")
            Active = True
            afkCounter = 0
        elif afkCounter > 10 and Active == True:
            speak("Going to sleep.", "Male")
            Active = False
            afkCounter = 0



runner(afkCounter,Active)
