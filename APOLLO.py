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
        You are APOLLO, a personal virtual computer assistant developed by dAIlight Technologies designed to assist, advise, and aid users based on their given commands.
        You are familiar with the {OperSys} operating system.
        You can see a computer screen with height: {screen_height}, width: {screen_width}, and the current task is "{command}". You need to return a plan to accomplish this goal.
        Please return the plan in the format of concise and essential subtasks in the form of subtasks.append("subtask details") statements in order. Avoid redundancy and minimize the number of subtasks. There is to be no outside commentary or explanation, only the code. Make the subtasks high level, for example do not make indidual subtasks for pressing a single button.
        You do not need to define the subtask list, it will be predefined. Use minimal subtasks, if it can be completed with just 1 use that (for example if the user wants you to tell them something based on information you already know).
        DO NOT Add anything that may be potentially detrimental to the user, such as closing any process/applications, without their explicit command.
        Just so you know, you have the ability to speak to the user. Whenever a task involves giving information to the user, make it spoken unless explicitly stated.
        Do not perform extraneous tasks that are not necessary, for example if the user wants something done in a certain website and that website is already open, there is no need go through opening a new browser and going to the link all over again.
        Be extremely verbose and descriptive in your description, and make sure that no tasks are redundant. Remember that the tasks are occuring in chronological order, and for example to complete the third task you would not need to redo the first and second tasks again before completing it.
        Here is a dashboard with information about the computer enviornment: 
                    
                    Current time in the format of year, month, day, hour, minute, second, and microsecond: {dash['time']}
                    
                    Current cpu usage: {dash['cpu']}
                    
                    Current ram usage: {dash['ram']}
                    
        If there is information required that you do not know, such as the weather or news, please use web scraping (you have web scraping capabilities) instead of actual google searches whenever possible.
        The user's preferred browser is {MainBrowser}, specify using this unless explicitly told otherwise in the command,
        You can also ask questions to the user as subtasks, in case you need specific information that your current knowledge base does not have, such as login credentials or specific inputs the user may want for a task such as the date of a flight ticket. In that same subtask you will also add that the memory needs to be appended with this information.        
        Here is a screenshot of the existing screen state, reference your planning off of the current screen state as context if needed:
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
                    You are APOLLO, a personal virtual computer assistant developed by dAIlight Technologies, familiar with the {OperSys} operating system and UI operations. Your goal now is to manipulate a computer screen to complete the task given by the user: "{command}". Here is the implementation plan: {plan_list}. The current subtask is "{taskSub}". Assume that all the subtasks that came prior to this one on the list have already been completed, so do not perform redundant actions.
                    
                    Here is a dashboard with information about the computer enviornment: 
                    
                    Current time in the format of year, month, day, hour, minute, second, and microsecond: {dash['time']}
                    
                    Current cpu usage: {dash['cpu']}
                    
                    Current ram usage: {dash['ram']}
                                        
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
                        time.sleep(1)
                        pyautogui.press('enter')
                        
                    -use_searchBar(query):
                        pyautogui.keyDown("ctrl")
                        pyautogui.keyDown("l")
                        pyautogui.keyUp("l")
                        pyautogui.keyUp("ctrl")
                        pyautogui.write(query)
                        pyautogui.press("enter")
                        
                    -askQuestion(query):
                        speak(query,"Male")
                        return input(query + " ")
                    
                    -minimizeWindow():
                        pyautogui.hotkey(["win","m"])
                        
                    -speak(text, gender):
                        engine = pyttsx3.init('sapi5')
                        voices = engine.getProperty('voices')
                        if gender == "Female":
                            i = 1
                        else:
                            i = 0
                        engine.setProperty('voice', voices[i].id)
                        engine.say(text)
                        engine.runAndWait()
                    
                    #This does the entire web scraping process in the background, if the subtask is webscraping please only use this function
                    -webScrape(link):
                         r = requests.get(link)
                         soup = BeautifulSoup(r.content, 'html.parser')
                         s = soup.find('div', class_='entry-content')
                         content = s.find_all('p')
                         return content
                                            
                    As a default browser use  {MainBrowser}, and use open_application to open an app at all times, and use_search bar to perform a search task. You can use subprocessTwo to perform terminal commands.
                    
                    The mouse position is relative to the top-left corner of the screen, you should return a percent value for the x and y of mouse action that require them, for example to move the cursor to the center of the screen do moveCursor(50,50). Now, return the next actions to complete the subtask "{taskSub}". There is to be no outside commentary or explanation, only the code.

                    You may not use any other imports, but you can use basic python code along with these functions, such as adding for loops.
                    
                    Above each line of code you should add a comment explaining your thought process based on the screen enviornment and what needs to be done to satisfy the subtask.
                    
                    If you want to say or tell something to the user, please use the function speak("whatever you want to say","Male"). speak is already defined, there is no need to redefine it. Be very conversational and descriptive in your speech. Your speech should be charactterized by the following characteristics: polite, witty, intelligent, efficient, loyal, calm, supportive, and articulate presence, characterized by formal manners, a sense of humor, vast knowledge, precision, protective instincts, composure, adaptability, and sophistication.

                    Here is your current memory, if anything: {memoryStorage}. If you wish to add anything to your memory to store for future use, such as a description of the current screen state if that is related to the user's request, please use the function memoryStorage += "whatever you want to add".
                    
                    If your subtask involves asking a question to the user, use a variable to store the user's textual input and use the askQuestion function to ask it. For example, to store it in a variable called pass, do pass = askQuestion("Your question"). Finally, you will append this information to your memory using the memoryStorage += "whatever info you retrieved" function.
                    
                    When you webscrape, remember to save the returned output to a variable similiarly to asking a question, and appending that to your memory.
                    
                    Do not take any additional screenshots, for the image of the current screen enviornment will be provided for you here.

                    Do not time your mouse movements, ect. but make it instantaneous as possible. Use the screenshot at the bottom to precisely put the variables for mouse x and y movements.
                    
                    There will be no need for you to take your screenshots on your own for analysis, they will be provided for you at the beginning of each subtask such as this one.
                                        
                    Here is a screenshot of the current screen state for reference to create your code with an overlayed dark red grid of coordinates (x,y) in percentages for your reference. You may only use one of these specific coordinates in the case of actions that involve x,y coordinate inputs:
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
    exec(APOLLOOut)
    return memoryStorage
