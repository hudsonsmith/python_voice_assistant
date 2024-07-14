import base64

import pyttsx3
import requests
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema.messages import HumanMessage
import shutup
import openai
import os
from PIL import Image, ImageChops, ImageStat

from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, ChatPromptTemplate

import commands
from commands import *

shutup.please()


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
    print("APOLLO: " + text)
    engine.say(text)
    engine.runAndWait()


os.environ['OPENAI_API_KEY'] = "KEY HERE"

APOLLO = ChatOpenAI(model="gpt-4o", max_tokens=256)

template = """You are a chatbot having a conversation with a human.

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are APOLLO, a virtual personal assistant designed to assist, advise, and aid users based on their given commands."
        ),
        MessagesPlaceholder(
            variable_name="chat_history"
        ),
        HumanMessagePromptTemplate.from_template(
            "{human_input}"
        ),
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm_chain = LLMChain(
    llm=APOLLO,
    prompt=prompt,
    verbose=True,
    memory=memory,
)


def output(command):
    APOLLOOut = llm_chain.predict(human_input=command)
    return APOLLOOut


def outputCommands(command):
    APOLLOCommander = OpenAI()
    screen_height = commands.screenHeight
    screen_width = commands.screenWidth

    Planning_phase = f"""
        You are APOLLO, a virtual personal assistant designed to assist, advise, and aid users based on their given commands.
        You are familiar with the Windows operating system.
        You can see a computer screen with height: {screen_height}, width: {screen_width}, and the current task is "{command}". You need to return a plan to accomplish this goal.
        Please return the plan in the format of concise and essential subtasks in the form of subtask.append("subtask details") statements in order. Avoid redundancy and minimize the number of subtasks. There is to be no outside commentary or explanation, only the code.
        You do not need to define the subtask list, it will be predefined. Use minimal subtasks, if it can be completed with just 1 use that (for example if the user wants you to tell them something based on information you already know)
        Here is a screenshot of the existing screen state for reference for your planning:
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
        max_tokens=300
    )
    APOLLOOut = APOLLOOut.choices[0].message.content
    APOLLOOut = APOLLOOut.replace("```", "").replace("python", "")
    subtask = []
    exec(APOLLOOut)
    plan_list = "\n".join(subtask)
    print(plan_list)
    memoryStorage = ""
    for task in subtask:
        memoryStorage += execute_task_with_feedback(task,APOLLOCommander, screen_width, screen_height, plan_list, command,memoryStorage)

    return "Task completed."

def reflect_task(APOLLOCommander, taskSub, plan_list, after_image):
    Reflection_phase = f"""
    Your goal was to complete the subtask: "{taskSub}". Here is the implementation plan you followed: {plan_list}.

    Check if the subtask "{taskSub}" has been completed correctly based on the screenshot that will be given at the bottom.
    
    If it was completed correctly, return True:NA.
    
    If it wasn't, return False: reason for why you think it wasn't completed correctly and what you can do next time based on the user advice if it was given. 
    
    Do not put any commas between the reasons, only one comma is to be there in case of false and that is between False and the reasoning.
    
    In the reason also add what the code ended up actually doing.
    
    There will be no extra commentary.
    
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
        max_tokens=300
    )
    APOLLOOut = APOLLOOut.choices[0].message.content
    APOLLOList = APOLLOOut.split(":")
    isDone = APOLLOList[0]
    mistake = APOLLOList[1]
    print(APOLLOList)
    return isDone, mistake
def execute_task_with_feedback(taskSub, APOLLOCommander,screen_width, screen_height, plan_list, command,memoryStorage):
    Latest_mistake = ""
    user_advice=""
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        Action_phase = f"""
                    You are familiar with the Windows operating system and UI operations. Your goal now is to manipulate a computer screen, width: {screen_width}, height: {screen_height}, to complete the task: "{command}". Here is the implementation plan: {plan_list}. The current subtask is "{taskSub}".

                    You can use the mouse and keyboard, along with other computer functions and terminal, by creating a python script using the libraries pyautogui, subprocess, and time. 

                    The mouse position is relative to the top-left corner of the screen. Return the next actions to complete the subtask "{taskSub}". There is to be no outside commentary or explanation, only the code.

                    If you want to say or tell something to the user, please use the function speak("whatever you want to say","Male"). speak is already defined, there is no need to redefine it.

                    If you have failed to complete your task, here is the reasoning for your latest failure: {Latest_mistake}. If you have failed previously, here is user advice to do better: {user_advice}. If it is blank, that means you have not failed yet.

                    Here is your current memory, if anything: {memoryStorage}. If you wish to add anything to your memory to store for future use, such as a description of the current screen state if that is related to the user's request, please use the function memoryStorage += "whatever you want to add".

                    Do not take any additional screenshots, for the image of the current screen enviornment will be provided for you here.

                    Do not time your mouse movements, ect. but make it instantaneous as possible. Use the screenshot at the bottom to precisely put the variables for mouse x and y movements.

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
            max_tokens=300,
            temperature=0
        )
        APOLLOOut = APOLLOOut.choices[0].message.content
        APOLLOOut = APOLLOOut.replace("```", "").replace("python", "")

        print(APOLLOOut)
        exec(APOLLOOut)
        after_screenshot = commands.screenshot()
        after_base64_image = encode_image(after_screenshot)
        taskDone, reason = reflect_task(APOLLOCommander,taskSub, plan_list, after_base64_image)
        print(taskDone)
        if taskDone == "True":
            break
        else:
            attempts += 1
            user_advice=input("This subtask failed, can you describe why?: ")
            print(f"Retrying task: {taskSub}, Attempt: {attempts}")
            Latest_mistake = reason
            if attempts == max_attempts:
                print(f"Failed to complete task: {taskSub} after {max_attempts} attempts.")
                break
    return memoryStorage


