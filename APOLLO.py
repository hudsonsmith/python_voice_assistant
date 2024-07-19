import base64

import pyttsx3
import requests
from openai import OpenAI
import shutup
import os
import commands
from commands import *
import platform

OperSys = platform.system()


shutup.please()

os.environ['OPENAI_API_KEY'] = "SECRET KEY"
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


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



def outputCommands(command):
    APOLLOCommander = OpenAI()
    screen_height = commands.screenHeight
    screen_width = commands.screenWidth

    Planning_phase = f"""
        You are APOLLO, a personal virtual computer assistant developed by dAIlight Technologies designed to assist, advise, and aid users based on their given commands.
        You are familiar with the {OperSys} operating system.
        You can see a computer screen with height: {screen_height}, width: {screen_width}, and the current task is "{command}". You need to return a plan to accomplish this goal.
        Please return the plan in the format of concise and essential subtasks in the form of subtasks.append("subtask details") statements in order. Avoid redundancy and minimize the number of subtasks. There is to be no outside commentary or explanation, only the code.
        You do not need to define the subtask list, it will be predefined. Use minimal subtasks, if it can be completed with just 1 use that (for example if the user wants you to tell them something based on information you already know).
        Just so you know, you have the ability to speak to the user.
        You can also ask questions to the user as subtasks, in case you need specific information that your current knowledge base does not have, such as login credentials or specific inputs the user may want for a task such as the date of a flight ticket. In that same subtask you will also add that the memory needs to be appended with this information.        
        Here is a screenshot of the existing screen state, reference your planning off of the current screen state as context if needed:
    """
    base64_image = encode_image(commands.screenshot())
    APOLLOOut = APOLLOCommander.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": Planning_phase
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1024
    )
    APOLLOOut = APOLLOOut.choices[0].message.content
    APOLLOOut = APOLLOOut.replace("```", "").replace("python", "")
    subtasks = []
    exec(APOLLOOut)
    plan_list = "\n".join(subtasks)
    print(plan_list)
    memoryStorage = ""
    for task in subtasks:
        memoryStorage += execute_task_with_feedback(task, APOLLOCommander, screen_width, screen_height, plan_list,
                                                    command, memoryStorage)

    return "Task completed."


def reflect_task(APOLLOCommander, taskSub, plan_list, after_image):
    Reflection_phase = f"""
    Your goal was to complete the subtask: "{taskSub}". Here is the implementation plan you followed: {plan_list}.
    Check if the subtask "{taskSub}" has been completed correctly based on the screenshot that will be given at the bottom.
    If it was completed correctly, return True:NA.
    If it wasn't, return the answer in the format of False:insert reason for why you think it wasn't completed correctly and what you can do next time based on the user advice if it was given. 
    In the reason also add what the code ended up actually doing, and how you can better it so it succeeds next attempt. If the entire plan needs to be changed, please detail the specifics of that as well.
    There will be no extra commentary.
    If the subtask involves speaking or taking user input, automatically mark it as True:NA.
    Here is a screenshot of the current screen state after your code was executed, for reference:
    """
    APOLLOOut = APOLLOCommander.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": Reflection_phase
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{after_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1024
    )
    APOLLOOut = APOLLOOut.choices[0].message.content
    print(APOLLOOut)
    APOLLOList = APOLLOOut.split(":")
    isDone = APOLLOList[0]
    mistake = APOLLOList[1]
    return isDone, mistake


def execute_task_with_feedback(taskSub, APOLLOCommander, screen_width, screen_height, plan_list, command,
                               memoryStorage):
    dash = {"time": currTime(), "cpu": currCpu(), "ram": currRam(), "apps": currApps()}
    Latest_mistake = ""
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        Action_phase = f"""
                    You are APOLLO, a personal virtual computer assistant developed by dAIlight Technologies, familiar with the {OperSys} operating system and UI operations. Your goal now is to manipulate a computer screen, width: {screen_width}, height: {screen_height}, to complete the task: "{command}". Here is the implementation plan: {plan_list}. The current subtask is "{taskSub}".
                    
                    Here is a dashboard with information about the computer enviornment: 
                    
                    Current time in the format of year, month, day, hour, minute, second, and microsecond: {dash['time']}
                    
                    Current cpu usage: {dash['cpu']}
                    
                    Current ram usage: {dash['ram']}
                    
                    Current apps open: {dash['apps']}
                    
                    You can use the mouse and keyboard, along with other computer functions and terminal, using only the following functions:
                    
                    -moveCursor(x, y):
                        x = (x / 100) * screenWidth
                        y = (y / 100) * screenHeight
                        pyautogui.moveTo(x, y)
                    
                    -rightClick():
                        pyautogui.rightClick()
                    
                    -leftClick():
                        pyautogui.leftClick()
                    
                    -write(text):
                        pyautogui.write(text)
                    
                    -drag(x,y):
                        x = (x/100)*screenWidth
                        y = (y/100)*screenHeight
                        pyautogui.dragTo(x,y)
                    
                    -press(key):
                        pyautogui.press(key)
                    
                    -scroll(clicks):
                        pyautogui.scroll(clicks)
                    
                    -wait(seconds):
                        time.sleep(seconds)
                    
                    -subprocessTwo(lis):
                        process = subprocess.Popen(lis, shell=True)
                        process.wait()
                    
                    -keyDown(key):
                        pyautogui.keyDown(key)
                    -keyUp(key):
                        pyautogui.keyUp(key)
                    
                    -hotkey(tup):
                        pyautogui.hotkey(tup)
                    
                    -doubleClick():
                        pyautogui.rightClick()
                        pyautogui.rightClick()
                    
                    -open_application(app_name):
                        pyautogui.press('win')
                        pyautogui.write(app_name)
                        pyautogui.press('enter')
                        
                    -use_searchBar(query):
                        pyautogui.keyDown("ctrl")
                        pyautogui.keyDown("l")
                        pyautogui.keyUp("l")
                        pyautogui.keyUp("ctrl")
                        pyautogui.write(query)
                        pyautogui.press("enter")
                        
                    The mouse position is relative to the top-left corner of the screen, you should return a percent value for the x and y of mouse action that require them, for example to move the cursor to the center of the screen do moveCursor(50,50). Now, return the next actions to complete the subtask "{taskSub}". There is to be no outside commentary or explanation, only the code.

                    You may not use any other imports, but you can use basic python code along with these functions, such as adding for loops.
                    
                    If you want to say or tell something to the user, please use the function speak("whatever you want to say","Male"). speak is already defined, there is no need to redefine it. Be very conversational and descriptive in your speech. Your speech should be charactterized by the following characteristics: polite, witty, intelligent, efficient, loyal, calm, supportive, and articulate presence, characterized by formal manners, a sense of humor, vast knowledge, precision, protective instincts, composure, adaptability, and sophistication.

                    If you have failed to complete your task, here is the reasoning for your latest failure: {Latest_mistake}.If it is blank, that means you have not failed yet.

                    Here is your current memory, if anything: {memoryStorage}. If you wish to add anything to your memory to store for future use, such as a description of the current screen state if that is related to the user's request, please use the function memoryStorage += "whatever you want to add".
                    
                    If your subtask involves asking a question to the user, do it by first using the speak function to say the question, then using a variable to store the user's textual input like pass = input("Your question"). Finally, you will append this information to your memory.
                    
                    Do not take any additional screenshots, for the image of the current screen enviornment will be provided for you here.

                    Do not time your mouse movements, ect. but make it instantaneous as possible. Use the screenshot at the bottom to precisely put the variables for mouse x and y movements.
                    
                    There will be no need for you to take your screenshots on your own for analysis, they will be provided for you at the beginning of each subtask such as this one.
                                        
                    Here is a screenshot of the current screen state for reference to create your code:
                    """
        base64_image = encode_image(commands.screenshot())
        APOLLOOut = APOLLOCommander.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": Action_phase
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1024,
            temperature=0
        )
        APOLLOOut = APOLLOOut.choices[0].message.content
        APOLLOOut = APOLLOOut.replace("```", "").replace("python", "")
        print(APOLLOOut)
        exec(APOLLOOut)
        after_screenshot = commands.screenshot()
        after_base64_image = encode_image(after_screenshot)
        taskDone, reason = reflect_task(APOLLOCommander, taskSub, plan_list, after_base64_image)
        if taskDone == "True":
            break
        else:
            attempts += 1
            print(f"Retrying task: {taskSub}, Attempt: {attempts}")
            Latest_mistake = reason
            if attempts == max_attempts:
                speak(f"Failed to complete task: {taskSub} after {max_attempts} attempts.","Male")
                break
    return memoryStorage
