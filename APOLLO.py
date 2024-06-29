import base64

from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema.messages import HumanMessage
import shutup
import os

from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, ChatPromptTemplate
from commands import *

shutup.please()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

os.environ['OPENAI_API_KEY'] = "sk-proj-vcRYkgWpMYCtw8UmEgfHT3BlbkFJI50EwzcnrPjntWvnCylT"

APOLLO = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=256)

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

APOLLOCommander = ChatOpenAI(model="gpt-4o", max_tokens=256)

templateOne = """You are a chatbot returning the commands you have been given, in correct order, to carry out the User's intended task.

{chat_history}
Human: {human_input}
Chatbot:"""

promptOne = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""You are APOLLO, a virtual personal assistant designed to assist users based on their given query, specifically performing computer tasks by returning given commands in the order that will most concisely carry out the task. The given commands and the code they do are listed here:

                    - moveCursor(x, y):
                        pyautogui.moveTo(x, y)

                    - rightClick():
                        pyautogui.rightClick()

                    - leftClick():
                        pyautogui.leftClick()

                    - write(text):
                        pyautogui.write(text)

                    - press(key):
                        pyautogui.press(key)

                    - scroll(clicks):
                        pyautogui.scroll(clicks)

                    - sleep(seconds):
                        time.sleep(seconds)

                    - subprocessTwo(lis):
                        process = subprocess.Popen(lis)
                        process.wait()

APOLLO should return commands in order that will enable the secondary script to perform the user’s desired task in the most simple way. You should not give any outside commentary at any point in time, only the commands. You should also specify the values within the command if they have one, for example, for moveCursor you must specify the x and y integers, for subprocessTwo you must specify the value within the list, ect. Before you output the commands, note that I am currently in pycharm. Do not close any tabs/apps or do something detrimental that the user has not explicitly said. Remember the power of subprocessTwo and press("win")."""

),
        MessagesPlaceholder(
            variable_name="chat_history_one"
        ),
        HumanMessagePromptTemplate.from_template(
            "{human_input}"
        ),
    ]
)

memoryOne = ConversationBufferMemory(memory_key="chat_history_one", return_messages=True)

llm_chain_one = LLMChain(
    llm=APOLLOCommander,
    prompt=promptOne,
    verbose=True,
    memory=memoryOne,
)

def output(command):
    APOLLOOut = llm_chain.predict(human_input=command)
    return APOLLOOut

def outputCommands(command):
    APOLLOOut = llm_chain_one.predict(human_input=command)
    try:
        APOLLOOut=APOLLOOut.replace("```","")
        APOLLOOut=APOLLOOut.replace("python","")
        exec(APOLLOOut)
        return "Task completed."
    except:
        return "Task completed"
