from PIL import Image, ImageTk
import APOLLO
from commands import *
import tkinter as tk
from threading import Thread, Event
import pyttsx3
import speech_recognition as sr

Active = False
stop_event = Event()
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


def runner(stop_event, text_widget):
    text_widget.insert(tk.END, "[APOLLO] Started Listening.\n")
    isActive = False
    afkCounter = 0
    while not stop_event.is_set():
        command = getCommand()
        if isActive:
            if command != "":
                text_widget.insert(tk.END, f"[USER] {command}\n")
                text_widget.insert(tk.END, f"[APOLLO] On it, {getTitle()}.\n")
                speak(f"On it, {getTitle()}", "Male")
                try:
                    out = doTask(command)
                    text_widget.insert(tk.END, f"[APOLLO] {out}\n")
                    speak(out, "Male")
                except:
                    speak("Sorry, I was unable to complete the task.", "Male")
                    text_widget.insert(tk.END, f"[APOLLO] Sorry, I was unable to complete the task.\n")
            else:
                afkCounter += 1
        if "apollo" in command:
            speak(f"What's up, {getTitle()}?", "Male")
            text_widget.insert(tk.END, f"[APOLLO] What's up, {getTitle()}?\n")
            isActive = True
            afkCounter = 0
        elif afkCounter > 3 and isActive:
            isActive = False
            afkCounter = 0
        if not Active:
            text_widget.insert(tk.END, "[APOLLO] Stopped Listening.\n")
            break


def create_gui():
    root = tk.Tk()
    root.title("APOLLO Assistant")

    logo = tk.PhotoImage(file='logo.png')
    root.iconphoto(False, logo)

    text_widget = tk.Text(root, wrap=tk.WORD)
    text_widget.pack(expand=True, fill=tk.BOTH)

    gif_path = "apollo_orb.gif"
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

    label = tk.Label(root, text="Enter your API Key here: ")
    label.pack()
    inputtxt = tk.Text(root, height=1, width=20)
    inputtxt.pack()

    label2 = tk.Label(root, text="Enter your preferred title here: ")
    label2.pack()
    inputtxt2 = tk.Text(root, height=1, width=20)
    inputtxt2.pack()

    def update_gif(frame_index=0):
        frame = gif_frames[frame_index]
        gif_label.configure(image=frame)
        root.after(50, update_gif, (frame_index + 1) % len(gif_frames))

    def toggle_listening():
        global Active, listening_thread, stop_event
        if Active:
            Active = False
            stop_event.set()
            if listening_thread is not None and listening_thread.is_alive():
                listening_thread.join()
            speak("Stopped listening.", "Male")
        else:
            Active = True
            stop_event.clear()
            listening_thread = Thread(target=runner, args=(stop_event, text_widget))
            listening_thread.start()
            speak("Started listening.", "Male")

    gif_label.bind("<Button-1>", lambda event: toggle_listening())

    update_gif()

    options = [
        "Google Chrome",
        "Mozilla Firefox",
        "Microsoft Edge",
        "Opera"
    ]

    clicked = tk.StringVar()
    clicked.set(options[0])

    def on_option_change(*args):
        APOLLO.MainBrowser = clicked.get()

    clicked.trace("w", on_option_change)

    def on_entered(*args):
        APOLLO.API_KEY = inputtxt.get("1.0", "end-1c")

    def on_entered_two(*args):
        APOLLO.getTitle = inputtxt.get("1.0", "end-1c")

    inputtxt.bind('<Return>', on_entered)
    inputtxt2.bind("<Return>",on_entered_two())
    drop = tk.OptionMenu(root, clicked, *options)
    drop.pack()

    root.mainloop()


if __name__ == "__main__":
    create_gui()
