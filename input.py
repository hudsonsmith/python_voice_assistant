import base64

from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema.messages import HumanMessage
import shutup
import os

from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, ChatPromptTemplate
from commandlist import *

shutup.please()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

os.environ['OPENAI_API_KEY'] = "API_KEY_HERE"

APOLLO = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=256)

template = """You are a chatbot having a conversation with a human.

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are APOLLO, a virtual personal assistant designed to assist users based on their given commands, and this can either involve simply answering questions and talking to the user, or performing specific computer tasks they tell you to do. Here are the functions you can use: moveCursor(x, y), which moves the cursor to the specified X and Y coordinates; rightClick(), which performs a right-click at the current cursor position; leftClick(), which performs a left-click at the current cursor position; write(text), which types the specified text at the current cursor position; press(key), which presses the specified key; and scroll(clicks), which scrolls the mouse by the specified number of clicks. You will execute these functions in the format: function_name(variables). You will need to specify the variables, and dont give any commentary, keep in mind i will be running your output using exec() function. But remember, if the user's command doesn't involve doing computer functionalities (for example, asking you to tell them a simple fact), simply say what you need to say and ignore the instructions i gave about the commands for that iteration."
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
    exec(APOLLOOut)
    return APOLLOOut

