import speech_recognition as sr
import pyttsx3
import time
import APOLLO
import commands

Active = False
afkCounter = 0

def speak(text, gender):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    if gender == "Female":
        i = 1
    else:
        i = 0
    engine.setProperty('voice', voices[i].id)
    print("APOLLO: " + text)
    engine.say(text)
    engine.runAndWait()

def getCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-US")
        except:
            query = ""
    return query.lower()

def doTask(command):
    return APOLLO.outputCommands(command)

def runner(afkCounter, Active):
    while True:
        command = input()
        print("User: " + command)
        if Active:
            if command != "":
                out = doTask(command)
                speak(out, "Male")
            else:
                afkCounter += 1
        if "that will be all" in command:
            speak("Going to sleep.", "Male")
            Active = False
            afkCounter = 0
        elif "apollo" in command:
            speak("How may I help you?", "Male")
            Active = True
            afkCounter = 0
        elif afkCounter > 10 and Active:
            speak("Going to sleep.", "Male")
            Active = False
            afkCounter = 0

runner(afkCounter, Active)
