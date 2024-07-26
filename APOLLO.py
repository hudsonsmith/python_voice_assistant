import base64
from openai import OpenAI
import shutup
import os
import commands
from commands import *
import platform

OperSys = platform.system()
MainBrowser = "Google Chrome"

shutup.please()

API_KEY = ""

getTitle = ""

os.environ['OPENAI_API_KEY'] = API_KEY
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')



def outputCommands(command):
    APOLLOCommander = OpenAI()
    screen_height = commands.screenHeight
    screen_width = commands.screenWidth
    dash = {"time": currTime(), "cpu": currCpu(), "ram": currRam()}
    Planning_phase = f"""
        You are APOLLO, a personal virtual computer assistant developed by dAIlight Technologies designed to assist, advise, and aid users based on their given commands. You can see a computer screen with height: {screen_height}, width: {screen_width}, and the current task is "{command}". 
        
        Here is a dashboard with extra information about the computer enviornment: 
                    
                    Current time in the format of year, month, day, hour, minute, second, and microsecond: {dash['time']}
                    
                    Current cpu usage: {dash['cpu']}
                    
                    Current ram usage: {dash['ram']}
        
        You need to return a plan to accomplish this goal. Please output your plan informat of concise and essential subtasks, e.g. my task is to search the web for " What’s the deal with the Wheat Field Circle?", the steps to disassemble this task are:

            subtasks.append(“Open web browser.”)
            subtasks.append(“Search in your browser for “What’ s the deal with the Wheat Field Circle?””)
            subtasks.append(“Open the first search result.”)
            subtasks.append(“Browse the content of the page.”)
            subtasks.append(“Answer the question "What’s the deal with the Wheat Field Circle?" according to the content.”)
        
        Another example, my task is "Write a brief paragraph about artificial intelligence in a notebook", the steps to disassemble this task are:
        
            subtasks.append(“Open Notebook.”)
            subtasks.append(“Write a brief paragraph about AI in the notebook.”)
            
        As a default browser use  {MainBrowser}, if relevant.
            
        Now, your current task is "{command}", give the disassembly steps of the task, in the format described above with no additional commentary, based on the state of the existing screen image:

    """
    base64_image = encode_image(commands.screenshot())
    APOLLOOut = APOLLOCommander.chat.completions.create(
        model="gpt-4o-mini",
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
        memoryStorage += execute_task(task, APOLLOCommander, screen_width, screen_height, plan_list,
                                                    command, memoryStorage)
    return "Task completed."


def execute_task(taskSub, APOLLOCommander, screen_width, screen_height, plan_list, command,
                               memoryStorage):
    dash = {"time": currTime(), "cpu": currCpu(), "ram": currRam()}
    Action_phase = f"""
    You are APOLLO, a personal virtual computer assistant developed by dAIlight Technologies. You’re very familiar with the {OperSys} operating system, and terminal and UI operations. Now you need to use the {OperSys} operating system to complete a mission. Your goal now is to manipulate a computer screen with height: {screen_height} and width: {screen_width}. The overall mission is: "{command }". We have developed an implementation plan for this overall mission: {plan_list}. The current subtask is "{taskSub}". Assume that all tasks in the list prior to this one have been completed, and plan your next steps accordingly. You can use the mouse and keyboard, the optional functions are: 

    moveCursor(x, y)
    
    rightClick()
    
    leftClick()
    
    write(text):
    
    drag(x,y)
    
    press(key)
    
    scroll(clicks)
    
    wait(seconds)
    
    useSubprocess(lis)
    
    keyDown(key)
      
    keyUp(key)
    
    hotkey(tup)
    
    doubleClick()
    
    open_application(app_name)
      
    use_searchBar(query)
      
    askQuestion(query)
    
    minimizeWindow()
      
    speak(text, gender)
    
    Where the mouse position is relative to the top-left corner of the screen. If the input is required in x,y format, please give them in the format of percentages between 0 - 100. As a default browser use  {MainBrowser}, use open_application to open an app at all times, and use_search bar to perform a search task. Above each line of code you should add a comment explaining your thought process based on the screen enviornment and what needs to be done to satisfy the subtask. Here is your current memory, if anything: {memoryStorage}. If you wish to add anything to your memory to store for future use, such as a description of the current screen state if that is related to the user's request, please use the function memoryStorage += "whatever you want to add". If your subtask involves asking a question to the user, use a variable to store the user's textual input and use the askQuestion function to ask it. For example, to store it in a variable called pass, do pass = askQuestion("Your question"). Finally, you will append this information to your memory using the memoryStorage += "whatever info you retrieved" function. 
    
    Here is a dashboard with extra information about the computer enviornment:
    
    
    Current time in the format of year, month, day, hour, minute, second, and microsecond: {dash['time']}
    
    
    Current cpu usage: {dash['cpu']}
    
    
    Current ram usage: {dash['ram']}
    
    
    Please make output execution actions, please format them in pythonic script. You cannot use any external libraries or imports, but you can use other basic python features such as for loops. The current subtask is "{taskSub}", please give the detailed next actions, in the format described above with no additional commentary, based on the state of the existing screen image:

                    """
    base64_image_gridded = encode_image(commands.screenshot_with_grid())
    APOLLOOut = APOLLOCommander.chat.completions.create(
            model="gpt-4o-mini",
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
                                "url": f"data:image/jpeg;base64,{base64_image_gridded}"
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
    return memoryStorage
