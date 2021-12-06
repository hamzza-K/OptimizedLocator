from optimizedLocator import Locate
try:
    from PIL import Image
except ImportError:
    import Image
import json, re
import pyautogui, sys, os, time, pytesseract
from pymsgbox import *


# Opening the Settings File
#==============================================
def openSettings():
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError as e:
        alert(text="Settings.json file was not loaded. Please Load the file and try again.", title="Settings File not Found", button="OK")
#===============================================
data = openSettings() #|||||||||||||||||||||||||
#===============================================
def click(cords):
    if len(cords) > 2:
        pyautogui.click(pyautogui.center(cords))
    else:
        pyautogui.click(cords)

# Locating Numbers in a loop
#===============================================
def numpad(numbers: str, t=data["TIME"]):
    for i in numbers:
        num = Locate(imgName=f"{i}", path=data["NUMBERS_CORDS"][f"{i}"][1], coordinates=tuple(data["NUMBERS_CORDS"][f"{i}"][0]), debug=data["DEBUG"])
        num.locateImage()
        print(f"Clicking on {num.getCoordinates()}...")
        click(num.getCoordinates())
        time.sleep(t)
#===============================================
def manualNumbers(cr: str):
    if data["DEBUG"] or data["ENTER_NUMBERS_MANUALLY"]:
        resp = prompt(text=f"The numbers to be entered are: ->'[{cr}]'", title="ID Numbers")
        if resp:
            try:
                print(f"trying user given numbers: {resp}....")
                numpad(resp)
            except ValueError:
                alert(text="Please enter only Numbers!", title="invalid input")
                sys.exit()
    else:
        print(f"Numbers to be entered are: [{cr}]")
        numpad(cr)


# ================================================
def replace_chars(text):
    """
    Replaces all characters instead of numbers from 'text'.
    
    :param text: Text string to be filtered
    :return: Resulting number
    """
    list_of_numbers = re.findall(r'\d+', text)
    result_number = ''.join(list_of_numbers)
    return result_number
# ================================================
pyautogui.FAILSAFE=data["FAILSAFE"]
# ================================================


def main(n: int):

    #CREATE ROOM
    createRoom = Locate(imgName="Create Room", path=data["createRoom"], coordinates=tuple(data["CREATE_ROOM_CORDS"]), debug=data["DEBUG"])
    createRoom.locateImage()
    

    time.sleep(data["TIME"])
    click(createRoom.getCoordinates())
    

    #ENTER ROOM
    enterRoom = Locate(imgName="Entering Room", path=data["enterARoomNumber"], coordinates=tuple(data["ENTER_ROOM_NUMBER_CORDS"]), debug=data["DEBUG"])
    enterRoom.locateImage()

    time.sleep(data["TIME"])
    click(enterRoom.getCoordinates())


    #ENTER ID NUMBER
    idbutton = Locate(imgName="id number", path=data["idnum"], coordinates=tuple(data["IDNO_CORDS"]), debug=data["DEBUG"])
    idbutton.takePic("images/idnumber.png", tuple(data["IDNO_CORDS"]))

    try:
        ocr_result = pytesseract.image_to_string(Image.open("images/idnumber.png"), lang='eng')
        clear_result = replace_chars(ocr_result)
        manualNumbers(clear_result)

    except Exception as e:
        print(f"{e}. Skipping the process.")

        resp = prompt(text="Enter numbers manually.", title="ID Numbers")
        if resp:
            try:
                print(f"trying user given numbers: {resp}....")
                numpad(resp)
            except ValueError:
                alert(text="Please enter only Numbers!", title="invalid input")
                sys.exit()

    #ENTER BUTTON
    enter = Locate(imgName="Enter Pad", path=data["enterNumbers"], coordinates=tuple(data["ENTER_ROOM_NUMBER_CORDS"]), debug=data["DEBUG"])
    enter.locateImage()


    time.sleep(data["TIME"])
    click(enter.getCoordinates())
    

    #This part is in loop
    for _ in range(n):
        #READY
        ready = Locate(imgName="ready", path=data["ready"], coordinates=tuple(data["READY_CORDS"]), debug=data["DEBUG"])
        ready.locateImage()

        time.sleep(data["TIME"])
        click(ready.getCoordinates())

        #START QUEST
        startQuest = Locate(imgName="Start Quest", path=data["startQuest"], coordinates=tuple(data["START_QUEST_CORDS"]), debug=data["DEBUG"])
        startQuest.locateImage()

        time.sleep(data["TIME"])
        click(startQuest.getCoordinates())
        
        #AUTO
        auto = Locate(imgName="Auto Button", path=data["auto"], coordinates=tuple(data["AUTO_CORDS"]), debug=data["DEBUG"])
        auto.locateImage()

        time.sleep(data["TIME"])
        click(startQuest.getCoordinates())
        
        #When game finishes
        #========================================================
        print(f"Sleeping for {data['GAME_TIME']} seconds...")
        time.sleep(data["GAME_TIME"])
        #========================================================

        #TAP TO CONTINUE 1
        tapToContinue = Locate(imgName="Tap To Continue 1", path=data["tapToContinue"],
         coordinates=tuple(data["TAP_TO_CONTINUE_U_CORDS"]), debug=data["DEBUG"])
        tapToContinue.locateImage()

        time.sleep(data["TIME"])
        click(tapToContinue.getCoordinates())
        
        #TAP TO CONTINUE 2
        tapToContinue = Locate(imgName="Tap To Continue 2", path=data["tapToContinue"],
         coordinates=tuple(data["TAP_TO_CONTINUE_B_CORDS"]), debug=data["DEBUG"])
        tapToContinue.locateImage()

        time.sleep(data["TIME"])
        click(tapToContinue.getCoordinates())
        
        #RETRY
        retry = Locate(imgName="Retry", path=data["retry"],
         coordinates=tuple(data["RETRY_CORDS"]), debug=data["DEBUG"])
        retry.locateImage()

        time.sleep(data["TIME"])
        click(retry.getCoordinates())
            
        #COOP
        coop = Locate(imgName="Co Op", path=data["coopQuestMenu"],
         coordinates=tuple(data["CO_OP_QUEST_CORDS"]), debug=data["DEBUG"])
        coop.locateImage()

        time.sleep(data["TIME"])
        click(coop.getCoordinates())
    
if __name__ == "__main__":

    resp = prompt(text="How many number of times should this script run? ", title="Loop Number")
    if data:
        try:
            main(int(resp))
            _ = input("The script will now get closed. Press Enter.")
        except ValueError:
            alert(text="Please enter only Numbers!", title="invalid input")
            sys.exit()
    else:
        print("Exiting since there is no settings file.")
        sys.exit()
