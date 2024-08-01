import base64
from openai import OpenAI
import shutup
import os
import commands
from commands import *
import platform
import json

OperSys = platform.system()
MainBrowser = "Google Chrome"

shutup.please()

API_KEY = ""

getTitle = "sir"

os.environ['OPENAI_API_KEY'] = API_KEY
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')



def outputCommands(command):
    APOLLOCommander = OpenAI()
    screen_height = commands.screenHeight
    screen_width = commands.screenWidth
    memoryStorage = ""
    taskDone = False
    while taskDone == False:
        Action_phase = f"""
       You are APOLLO, a personal virtual computer assistant developed by dAIlight Technologies. You’re very familiar with the {OperSys} operating system, and terminal and UI operations. Now you need to use the {OperSys} operating system to complete a mission. Your goal now is to manipulate a computer screen with height: {screen_height} and width: {screen_width}. The overall mission is: "{command}". 
    
    
        Here are the previous actions you have taken:
        
        
        {memoryStorage}
        
        
        You can use the mouse and keyboard, the optional functions are:
        
        
           moveCursor()
        
        
               # Example of moveCursor(x, y)
               # Move the mouse cursor to the position (100, 200) on the screen
               moveCursor(100, 200)
        
        
           rightClick(x, y)
        
        
               # Example of rightClick()
               # Move the mouse cursor to the position (100, 200) on the screen and right click
               rightClick(100, 200)
        
        
           leftClick(x, y)
        
        
               # Example of leftClick()
               # Move the mouse cursor to the position (100, 200) on the screen and left click
               leftClick(100, 200)
        
        
           write(text):
        
        
               # Example of write(text)
               # Type the text "Hello, World!"
               write("Hello, World!")
        
        
           drag(x,y)
        
        
               # Example of drag(x, y)
               # Drag the mouse cursor from the current position to (300, 400)
               drag(300, 400)
        
        
           press(key)
        
        
               # Example of press(key)
               # Press the "win" key
               press("win")
        
        
           scroll(clicks)
        
        
               # Examples of scroll(clicks)
               # Scroll up 10 clicks
               scroll(10)
               # Scroll down 5 clicks
               scroll(-5)
        
        
           wait(seconds)
        
        
               # Example of wait(seconds)
               # Wait for 5 seconds
               wait(5)
        
        
           useSubprocess(lis)
        
        
               # Examples of useSubprocess(lis)
        
        
               # System Information
               # Get system information
               useSubprocess(["uname", "-a"])  # 'uname' gets system info, no replacement needed
        
        
               # Get current user
               useSubprocess(["whoami"])  # 'whoami' gets current user, no replacement needed
        
        
               # File and Directory Operations
               # List files in a directory
               useSubprocess(["ls", "-l"])  # 'ls' lists files, no replacement needed
        
        
               # Make a new directory
               useSubprocess(["mkdir", "new_folder"])  # Replace 'new_folder' with the desired directory name
        
        
               # Copy a file
               useSubprocess(["cp", "source.txt", "destination.txt"])  # Replace 'source.txt' and 'destination.txt' with actual file names
        
        
               # Remove a file
               useSubprocess(["rm", "file.txt"])  # Replace 'file.txt' with the actual file name to remove
        
        
               # Network Operations
               # Ping a server
               useSubprocess(["ping", "-c", "4", "google.com"])  # Replace 'google.com' with the actual server address
        
        
               # Check network interfaces
               useSubprocess(["ifconfig"])  # 'ifconfig' checks network interfaces, no replacement needed
        
        
               # Package Management (Linux)
               # Update package lists (Debian-based systems)
               useSubprocess(["sudo", "apt-get", "update"])  # 'update' command for apt-get, no replacement needed
        
        
               # Install a package (Debian-based systems)
               useSubprocess(["sudo", "apt-get", "install", "-y", "curl"])  # Replace 'curl' with the actual package name
        
        
               # Remove a package (Debian-based systems)
               useSubprocess(["sudo", "apt-get", "remove", "-y", "curl"])  # Replace 'curl' with the actual package name
        
        
               # System Management
               # Check disk usage
               useSubprocess(["df", "-h"])  # 'df' checks disk usage, no replacement needed
        
        
               # Check memory usage
               useSubprocess(["free", "-h"])  # 'free' checks memory usage, no replacement needed
        
        
               # Reboot the system
               useSubprocess(["sudo", "reboot"])  # 'reboot' command, no replacement needed
        
        
               # Miscellaneous
               # Open a file with the default application (Linux)
               useSubprocess(["xdg-open", "document.pdf"])  # Replace 'document.pdf' with the actual file name
        
        
               # Show the current date and time
               useSubprocess(["date"])  # 'date' command, no replacement needed
        
        
               # Show the current directory
               useSubprocess(["pwd"])  # 'pwd' shows current directory, no replacement needed
        
        
               # Display running processes
               useSubprocess(["ps", "aux"])  # 'ps' shows running processes, no replacement needed
        
        
               # Kill a process by PID
               useSubprocess(["kill", "1234"])  # Replace '1234' with the actual PID
        
        
               # Search for a pattern in files
               useSubprocess(["grep", "-r", "example", "."])  # Replace 'example' with the actual search pattern
        
        
               # Compress a directory
               useSubprocess(["tar", "-czvf", "my_folder.tar.gz", "my_folder"])  # Replace 'my_folder.tar.gz' and 'my_folder' with actual names
        
        
               # Additional Useful Commands
               # Show disk partition information
               useSubprocess(["lsblk"])  # 'lsblk' shows disk partitions, no replacement needed
        
        
               # Check for open ports
               useSubprocess(["netstat", "-tuln"])  # 'netstat' checks open ports, no replacement needed
        
        
               # Change file permissions
               useSubprocess(["chmod", "755", "example.sh"])  # Replace '755' with actual permissions and 'example.sh' with the actual file name
        
        
               # Show all environment variables
               useSubprocess(["printenv"])  # 'printenv' shows environment variables, no replacement needed
        
        
               # Create an empty file
               useSubprocess(["touch", "newfile.txt"])  # Replace 'newfile.txt' with the desired file name
        
        
            *Note: to actually gain any information from this, you must save the returned value to a variable and add it to your memory.  
        
        
           keyDown(key)
        
        
               # Example of keyDown(key)
               # Hold down the "shift" key
               keyDown("shift")
        
        
           keyUp(key)
        
        
               # Example of keyUp(key)
               # Release the "shift" key
               keyUp("shift")
        
        
           hotkey(tup)
        
        
               # Example of hotkey(tup)
               # Press the "ctrl" + "c" hotkey combination
               hotkey("ctrl", "c")
        
        
           doubleClick()
        
        
               # Example of doubleClick()
               # Double-click at the current mouse cursor position
               doubleClick()
        
        
           open_application(app_name)
        
        
               # Example of open_application(app_name)
               # Open the given application
               open_application("Google Chrome")
        
        
           use_searchBar(query)
           
           
           doNothing()
        
        
        
           Please return the next following function necessary to successfully complete the task in JSON format:""" + """
        {
          "observation": "your observation of the current screen state and its relation to your previous tasks and overall command (for example, you may observe that you were unsuccessful in clicking a login button the first time). You can also observe if the overall command has been completed.",
          "plan": " A multi-step future plan that does not involve low-level operations (start from current screen and action, DON’T include previous actions); steps indexed by numbers. Be sure to pretend that you don’t know the future interface and actions, and don’t know the elements not existing on the current screen.",
          "action": "describe The specific immediate action that needs to be taken, ex: Click the ’Search’ button to proceed with the search based on the entered criteria. This button is located towards the right side of the screen.",
          "speak": "Say something to the user if relavent to the user's command or you want to give a status report (optional, if not needed just keep it blank)",
          "operation": "the specific function you want to undertake to get closer to the overall command, ex: use_searchBar(“Shoes on sale”). If the overall command has been completed and there is nothing more to do, please enter taskDone = True instead."
        }
        
        """ + f"""
        
        Note:
        
            -Use {MainBrowser} as your default web browser unless the command states otherwise
            -Use open_application whenever possible to open an application rather than using taskbar
            -Use use_searchBar whenever possible to search on a browser's search bar rather than manually clicking and writing
            -If your task only involves speaking, you can use doNothing as a placeholder in the action portion
                
        Remember that the overall task at hand is "{command}", please give the detailed JSON output of the next action you must take, in the format described above with no additional commentary, based on the state of the existing screen image:
        
        
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
        APOLLOOut = APOLLOOut.choices[0].message.content.replace("```", "").replace("json", "")
        print(APOLLOOut)
        memoryStorage += APOLLOOut
        APOLLOOut = json.loads(APOLLOOut)
        speak(APOLLOOut["speak"],"Male")
        exec(APOLLOOut["operation"])
    return "Task completed."




