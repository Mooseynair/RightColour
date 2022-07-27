import cv2
import numpy as np
import mss
import matplotlib.pyplot as plt
import time
import pyautogui
import keyboard


class RightColour:
    def __init__(self):
        self.SCT = mss.mss()
        self.check = 0

    # Returns the RGB value of the prompt text
    def ReadTextColour(self, debug=False):
        
        area = {
            'left': 900,
            'top': 350,
            'width': 100,
            'height': 40
        }

        scr = self.SCT.grab(area)
        img = np.array(scr)
        color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        value = color[24, 48]
        print(value)

        # Only show if we are debugging
        if debug:
            plt.imshow(color)
            plt.show()

        return value

    # Returns the RGB value of the given shape
    def ReadShapeColour(self, debug=False):
    
        area = {
            'left': 900,
            'top': 715,
            'width': 100,
            'height': 85
        }

        scr = self.SCT.grab(area)
        img = np.array(scr)
        color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        value = color[42, 50]
        print(value)

        # Only show if we are debugging
        if debug:
            plt.imshow(color)
            plt.show()

        return value
        
    # Convert the RGB values to strings
    def CvtInt2Str(self, value):
        colour = ""
        if np.array_equal(value,[255,0,0]):
            colour = "red"
        elif np.array_equal(value,[255,234,0]) or np.array_equal(value,[252,255,0]):
            colour = "yellow"
        elif np.array_equal(value,[0,212,70]):
            colour = "green"
        elif np.array_equal(value,[0,0,0]):
            colour = "black"
        else:
            colour = "unknown"
        return colour

    # Compare the string values to see if colours match
    def CompareColours(self, colour1, colour2):
        command = ""
        if colour1 == "unknown" or colour2 == "unknown":
            command = "Unknown colour"
            print("Unknown colour")
        elif colour1 == colour2:
            command = "Yes"
            print("Yes")
        else:
            command = "No"
            print("No")
        return command

    # Move the mouse in the desired fashion
    def MoveMouse(self, command):
    
        pyautogui.moveTo(950, 760)  
        if command == "Yes" and self.check == 0:
            self.check = 1
            pyautogui.dragTo(950, 460, 0.101, button='left')
        elif command == "No" or self.check == 1:
            self.check = 0
            pyautogui.dragTo(1250, 760, 0.101, button='left')

        
    def Retry(self, debug=False, click=False):
        area = {
            'left': 870,
            'top': 600,
            'width': 250,
            'height': 250
        }
        scr = self.SCT.grab(area)
        img = np.array(scr)
        try_again = cv2.imread('Retry.png', cv2.IMREAD_UNCHANGED)
        result = cv2.matchTemplate(img, try_again, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if debug:
            print("Max val: ")
            print(max_val)
            print(max_loc)

        if max_val > .85:
            if click:
                # print(max_loc[0] + area['left'], max_loc[1] + area['top'])
                left_adj = max_loc[0] + area['left']
                top_adj = max_loc[1] + area['top']
                pyautogui.click(left_adj, top_adj)

            return True
        return False

# text
# red = 255 0 0 
# yellow = 255 234 0 
# green = 0 212 70
# black = 0 0 0 

# red = 255 0 0 
# yellow = 252 255 0 
# green = 0 212 70
# black = 0 0 0 



        
if __name__ == "__main__":
    # Testing class
    bot = RightColour()
    bot.Retry(debug=True, click=True)
    while not keyboard.is_pressed('q'):
        value1 = bot.ReadTextColour(debug=False)
        value2 = bot.ReadShapeColour(debug=False)
        colour1 = bot.CvtInt2Str(value1)
        colour2 = bot.CvtInt2Str(value2)
        command = bot.CompareColours(colour1, colour2)
        bot.MoveMouse(command)
        # time.sleep(.1)
