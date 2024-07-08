
import base64

import requests
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema.messages import HumanMessage
import shutup
import openai
import os

from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, ChatPromptTemplate

import commands
from commands import *

shutup.please()

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

os.environ['OPENAI_API_KEY'] = "KEY HERE"
api_key = "KEY HERE"

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

#***********************

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
                Please return the plan in the format of subtasks in the form of subtask.append(subtask_details) statements in order. For example: if my task is "Write a brief paragraph about artificial intelligence in a notebook", return something in this format and style:

                subtask.append("Open notebook")
                subtask.append("Write a brief paragraph about AI in the notebook")

                There will be NO outside commentary, only subtask appending in this format. You must be EXTREMELY precise and clear on your intent (no this OR that, or vague descriptions). Try to minimize the number of subtasks and when possible make the subtasks use terminal as it increases conciseness and efficiency. Now, please follow those instructions and give a well-thought-out plan via returning the subtasks to carry out the current task of {command}.

                Here is a screenshot of the existing screen state:
            """
    base64_image = encode_image(commands.screenshot())
    APOLLOOut = APOLLOCommander.chat.completions.create(
        model="gpt-4o",
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
    APOLLOOut = APOLLOOut.replace("```", "")
    APOLLOOut = APOLLOOut.replace("python", "")
    subtask = []
    exec(APOLLOOut)
    plan_list = ""
    for task in subtask:
        plan_list += task + "\n"
    print(plan_list)
    for task in subtask:
        Action_phase = f"""
        You’re very familiar with the Windows operating system and UI operations. Now you need to use the Windows operating system to complete a mission. Your goal now is to manipulate a computer screen, width: { screen_width }, height: { screen_height }, the overall mission is: "{command}". We have developed an implementation plan for this overall mission: {plan_list}.The current subtask is "{task}".
    
        You can use the mouse and keyboard, the optional actions you can take are: 
        
        -moveCursor(x,y):
            Input variables: x = int, y = int
        -rightClick():
            Input variables: none
        -leftClick():
            Input variables: none
        -write(text):
            Input variables: text = string
        -drag(x,y):
            Input variables: x = int, y = int
        -press(key):
            Input variables: key = string
        -scroll(clicks):
            Input variables: clicks = int
        -sleep(seconds):
            Input variables: seconds = int
        -subprocessTwo(lis):
            Input variables: lis = list
            *You can ue this to perform terminal commands
        -keyDown(key):
            Input variables: key = string
        -keyUp(key):
            Input variables: key = string
        
        Keep in mind these functions are based on the pyautogui, subprocess and time libraries. You may also use standard python code such as for loops if needed.
        
        
        Where the mouse position is relative to the top-left corner of the screen.
        You need to fill in the variables of the actions you take if they exist, and return them in order to complete the subtask “{task}”.
        Whenever possible, use subprocessTwo function to increase speed and conciseness, as it allows you to perform terminal commands.
        The current subtask is “{task}”, please return the next actions, without commentary or explanations (just give the actions by themselves, one per line) in order based on this screenshot of the current screen state:
    
        """
        base64_image = encode_image(commands.screenshot())
        APOLLOOut = APOLLOCommander.chat.completions.create(
            model="gpt-4o",
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
            max_tokens=300
        )
        APOLLOOut = APOLLOOut.choices[0].message.content
        APOLLOOut = APOLLOOut.replace("```", "")
        APOLLOOut = APOLLOOut.replace("python", "")
        print(APOLLOOut)
        exec(APOLLOOut)
    return "Task completed."
