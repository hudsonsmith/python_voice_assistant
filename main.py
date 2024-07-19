from PIL import Image, ImageTk
import struct
import speech_recognition as sr
import pyaudio
import pyttsx3
import time
import pvporcupine
import APOLLO
import commands
import tkinter as tk
from threading import Thread

Active = False
afkCounter = 0
listening_thread = None

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

def runner(text_widget):
    global Active, afkCounter
    while Active:
        command = getCommand()
        text_widget.insert(tk.END, f"User: {command}\n")
        text_widget.see(tk.END)

        if command != "":
            out = doTask(command)
            speak(out, "Male")
            text_widget.insert(tk.END, f"[APOLLO] {out}\n")
            text_widget.see(tk.END)
        else:
            afkCounter += 1

        if "that will be all" in command:
            speak("Going to sleep.", "Male")
            text_widget.insert(tk.END, "[APOLLO] Going to sleep.\n")
            text_widget.see(tk.END)
            Active = False
            afkCounter = 0
        elif "apollo" in command or "appollo" in command:
            speak("How may I help you?", "Male")
            text_widget.insert(tk.END, "[APOLLO] How may I help you?\n")
            text_widget.see(tk.END)
            Active = True
            afkCounter = 0
        elif afkCounter > 10 and Active:
            speak("Going to sleep.", "Male")
            text_widget.insert(tk.END, "[APOLLO] Going to sleep.\n")
            text_widget.see(tk.END)
            Active = False
            afkCounter = 0

def create_gui():
    root = tk.Tk()
    root.title("APOLLO Assistant")

    logo = tk.PhotoImage(file='pngtree-sun-icon-logo-png-png-image_5687131.png')
    root.iconphoto(False, logo)

    text_widget = tk.Text(root, wrap=tk.WORD)
    text_widget.pack(expand=True, fill=tk.BOTH)

    gif_path = "ezgif.com-gif-maker.gif"
    gif = Image.open(gif_path)

    gif_frames = []
    try:
        while True:
            gif_frames.append(ImageTk.PhotoImage(gif.copy()))
            gif.seek(len(gif_frames))
    except EOFError:
        pass

    gif_label = tk.Label(root)
    gif_label.pack()

    def update_gif(frame_index=0):
        frame = gif_frames[frame_index]
        gif_label.configure(image=frame)
        root.after(50, update_gif, (frame_index + 1) % len(gif_frames))

    def toggle_listening():
        global Active, listening_thread
        if Active:
            Active = False
            if listening_thread is not None and listening_thread.is_alive():
                listening_thread.join()
            speak("Stopped listening.", "Male")
        else:
            Active = True
            listening_thread = Thread(target=runner, args=(text_widget,))
            listening_thread.start()
            speak("Started listening.", "Male")

    gif_label.bind("<Button-1>", lambda event: toggle_listening())

    update_gif()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
