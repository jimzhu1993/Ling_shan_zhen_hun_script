import pyautogui as pag
import time
from enum import Enum

class Button(Enum):
    # hardcode the pixel value of the center of each button
    AUTO = (73, 104, 103)
    CANCEL = (21, 28, 64)
    FUNCTION = (204, 208, 171)

class game_support(object):
    def __init__(self, resetRoundInterval = 5):
        # locate buttons for reference
        self.reset = resetRoundInterval
        self.autoButtonPosition = None
        self.cancelButtonPosition = None
        self.functionButtonPosition = self.get_button('Function.png')
        while not self.functionButtonPosition:
            self.functionButtonPosition = self.get_button('Function.png')
        self.autoButtonPosition = self.get_button('Auto.png')
        self.cancelButtonPosition = self.get_button('Cancel.png')
        if self.autoButtonPosition:
            self.click_button(Button.AUTO)
            time.sleep(0.5)
            self.cancelButtonPosition = self.get_button('Cancel.png')
        else:
            self.click_button(Button.CANCEL)
            time.sleep(0.5)
            self.autoButtonPosition = self.get_button('Auto.png')

    def get_button(self, name):
        buttonPos = pag.locateCenterOnScreen(name)
        if buttonPos:
            print (name.split('.')[0] + " button is found at " + str(buttonPos))
            return buttonPos
        else:
            # print (name.split('.')[0] + " button is not found")
            return None

    def click_button(self, button):
        if button == Button.AUTO:
            x, y = self.autoButtonPosition
        elif button == Button.CANCEL:
            x, y = self.cancelButtonPosition
        else:
            print ("Invalid Button")
            exit(1)
        pag.moveTo(x, y, 0.3, pag.easeOutQuad)
        pag.click()

    def button_overlay(self, button):
        if button == Button.AUTO:
            x, y = self.autoButtonPosition
        elif button == Button.CANCEL:
            x, y = self.cancelButtonPosition
        elif button == Button.FUNCTION:
            x, y = self.functionButtonPosition
        else:
            print ("Invalid Button")
            exit(2)
        return pag.pixelMatchesColor(x, y, button.value)

    def run(self):
        try:
            while True:
                # reset auto attack if in battle
                if self.button_overlay(Button.FUNCTION):
                    if self.button_overlay(Button.AUTO):
                        self.click_button(Button.AUTO)
                    else:
                        self.click_button(Button.CANCEL)
                        self.click_button(Button.AUTO)
                    time.sleep(self.reset)
                else:
                    print ("Not in battle")
                # auto attack has 3 seconds delay to take effect
                time.sleep(3)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    support = game_support()
    support.run()
