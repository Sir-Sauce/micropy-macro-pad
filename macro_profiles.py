
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


#TODO
#define a basic numpad functionality


#TOP LEFT -> TOP RIGHT
#TOP -> BOTTOM
NUM_PROFILES = 4

#BASIC NUMPAD FUNCITONALITY # NUMPAD LOGO
key_profile_1 = {
    0 : None,
    1 : None,
    2 : Keycode.POUND, #FUNCTION SELECTOR KEY
    3 : Keycode.ONE, 
    4 : Keycode.TWO,
    5 : Keycode.THREE,
    6 : Keycode.FOUR,
    7 : Keycode.FIVE,
    8 : Keycode.SIX,
    9 : Keycode.SEVEN,
    10 : Keycode.EIGHT,
    11 : Keycode.NINE,
    12 : Keycode.ZERO,
    13 : None, #should be a decimal
    14 : Keycode.ENTER,
}

#WINDOWS KEY PRODUCTIVITY # WINDOWS LOGO
key_profile_2 = {
    0 : Keycode.GUI, #WINDOWS KEY
    1 : (Keycode.CONTROL, Keycode.S), #SAVE HOTKEY
    2 : Keycode.POUND, #FUNCTION SELECTOR KEY
    3 : None, 
    4 : None,
    5 : None,
    6 : None,
    7 : None,
    8 : None,
    9 : None,
    10 : None,
    11 : None, #file explorer
    12 : None, #alt tab
    13 : None, #tab
    14 : Keycode.ENTER,
}
# https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html

#VSCODE SHORTCUTS #VSCODE LOGO
key_profile_3 = {
    0 : Keycode.GUI, #WINDOWS KEY
    1 : (Keycode.CONTROL, Keycode.S), #SAVE HOTKEY
    2 : Keycode.POUND, #FUNCTION SELECTOR KEY
    3 : None, #CTRL + SHIFT + P #COMMAND PALLET
    4 : None,
    5 : None,
    6 : None,
    7 : None,
    8 : None,
    9 : None,
    10 : None,
    11 : None,
    12 : None,
    13 : None, #tab 
    14 : Keycode.ENTER,
}
#HOME APP LAUNCHER # GAME CONTROLLER LOGO
key_profile_4 = {
    0 : Keycode.GUI, #WINDOWS KEY
    1 : (Keycode.CONTROL, Keycode.S), #SAVE HOTKEY
    2 : Keycode.POUND, #FUNCTION SELECTOR KEY
    3 : None,
    4 : None,
    5 : None,
    6 : None,
    7 : None,
    8 : None,
    9 : None, #screenshot key
    10 : None, #alt f10 #record clip  
    11 : None, #alt z #nvidia shadowplay
    12 : None, #alt tab
    13 : None, # tab
    14 : Keycode.ENTER,
}

class Macro_Profile():
    def __init__(self, profile):
        self.key_profile : dict
        self.pot_profile = None
        self.select_profile(profile_num=profile)
        
    def profile_printout(self):
        print(self.key_profile)
        
    def select_profile(self, profile_num : int):
        
        #Select keyboard and pot profile
        if profile_num == 1:
            self.key_profile = key_profile_1 
        elif profile_num == 2:
            self.key_profile = key_profile_2
        elif profile_num == 3:
            self.key_profile = key_profile_3
        elif profile_num == 3:
            self.key_profile = key_profile_4
        else:
            self.key_profile = key_profile_1 #default back to numpad functionality
        self.profile_printout()
        
    def map_keypress_to_keycode(self, keypress_event):
        print(keypress_event.key_number, type(keypress_event.key_number))
        key_code = self.key_profile[keypress_event.key_number]
        return key_code
    