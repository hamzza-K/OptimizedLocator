import pyautogui
import json
import sys
import time
import os
from pymsgbox import *
# =======================================

class Locate(object):
    """Returns the coordinates of the image located on screen."""

    def __init__(self, imgName: str, path: str, coordinates: tuple, debug=True):
        self.imgName = imgName
        self.path = path
        self.coordinates = coordinates
        self.debug = debug

        self.cmpltPath = os.path.join(os.getcwd(), self.path)

    def keepLocating(self, image):
        while True:
            image = pyautogui.locateOnScreen(self.path)
            if image is None:
                resp = confirm(text=f"'{self.imgName}' button cannot be located which is stored as {self.path}. Is it present? Press 'Retry' to try again or 'Cancel' to bypass.", \
                title="Button Not Present", buttons=["Retry", "Cancel"])
                if resp == "Retry":
                    print("Retrying...")
                elif resp == "Cancel":
                    print(f"image:{self.imgName} was not found which is stored as {self.path}..skipping the process and using coordinates {self.coordinates} instead.")
                    if len(self.coordinates) == 2:
                        pyautogui.moveTo((self.coordinates))
                    else:
                        pyautogui.moveTo(pyautogui.center(self.coordinates))
                    break
                else:
                    break
            elif image:
                self.coordinates = image

                print(f"Image found...moving to X:{self.coordinates[0]} Y:{self.coordinates[1]}")
                if len(self.coordinates) == 2:
                    pyautogui.moveTo((self.coordinates))
                else:
                    pyautogui.moveTo(pyautogui.center(self.coordinates))
                break
            else:
                print(f"Unexpected behavior happened. Terminating the process.")
                sys.exit()


    def takePic(self, name, coordinates):
        self.locateImage()
        print("taking the screenshot now..")
        if len(coordinates) < 4:
            print(f"There should be 4 arguments. Currently standing at {self.coordinates}")
            if self.debug:
                print(f"Currently standing at {self.coordinates}....")
                resp = prompt(text=f"There should be 4 arguments (left, top, width, height). Please enter. Currently standing at {self.coordinates}",
                title="Less Arguments provided")
                if resp:
                    try:
                        print(f"trying user given coordinates: {resp}....")
                        coordinates = tuple(map(int, resp.split(",")))
                        print(f"Difference to the original place: {tuple(map(lambda i, j: i - j, coordinates, self.coordinates))}")
                        pyautogui.screenshot(f"{name}", coordinates)
                        print(f"Successfully took a screenshot at {resp}. saving the screenshot as {name}")
                    except ValueError:
                        alert(text="Please enter only Numbers and separate them with commas!", title="invalid input")
            else:
                print(f"Arguments were less than 4. Using coordinates in settings instead..{coordinates} and width:228, height:51. Storing image as {name}")
                pyautogui.screenshot(f"{name}", region=(coordinates[0], coordinates[1], 228, 51))

        elif len(self.coordinates) == 4:
            print(f"Taking screenshot..storing as {name}")
            pyautogui.screenshot(f"{name}", region=(coordinates))

        else:
            print("Something Unexpected happened. Terminating")
            sys.exit()



    def locateImage(self):
        try:
            image = pyautogui.locateOnScreen(self.path)
            if image is None:
                if self.debug:
                    self.keepLocating(image)
                else:
                    print(f"image:{self.imgName} was not found which is stored as {self.path}..skipping the process and using coordinates {self.coordinates} instead.")
                    if len(self.coordinates) == 2:
                        pyautogui.moveTo((self.coordinates))
                    else:
                        pyautogui.moveTo(pyautogui.center(self.coordinates))

            elif image:
                self.coordinates = image
                print(f"Image found...moving to X:{self.coordinates[0]} Y:{self.coordinates[1]}")
                if len(self.coordinates) == 2:
                    pyautogui.moveTo((self.coordinates))
                else:
                    pyautogui.moveTo(pyautogui.center(self.coordinates))
            else:
                print(f"Unexpected behavior happened. Terminating the process.")
                sys.exit()

        except FileNotFoundError as e:
            print(f"{e}")
            if self.debug:
                # resp = prompt(text=f"Image {self.path} was not found. Would you like to manually enter coordinates and save?",
                # title="Image not Found")

                resp = alert(text=f"Image {self.path} was not found. Does the image exists? Please check and try again",
                title="Image not Found", button="OK")
                # if resp:
                #     try:
                #         self.coordinates = tuple(map(int, resp.split(",")))
                #     except ValueError:
                #         alert(text="Please enter only Numbers and separate them with commas!", title="invalid input")
                #     print(f"Entering custom coordinates..{self.coordinates}")
                #
                #     data = {f"{self.imgName}": self.coordinates}
                #     with open("Regions.json", "a+") as f:
                #         json.dump(data, f)
            else:
                print(f"using given coordinates: {self.coordinates} instead.")

                if len(self.coordinates) == 2:
                    pyautogui.moveTo((self.coordinates))
                else:
                    pyautogui.moveTo(pyautogui.center(self.coordinates))

    def getCoordinates(self):
        return self.coordinates


    def __str__(self):
        return "Locating Images on Screen"
