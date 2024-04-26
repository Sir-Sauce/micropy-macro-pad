# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
NeoKey 5x6 Ortho Snap-Apart simple key press NeoPixel demo.
"""
import board
import keypad
import neopixel
import time
import math
from analogio import AnalogIn
import busio
import usb_hid
from macro_profiles import Macro_Profile, NUM_PROFILES 

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import adafruit_ssd1306


potentiometer = AnalogIn(board.GP28_A2)  # potentiometer connected to A1, power & ground

#user made modules
import run_oled
import utils
 
#define constants 
REFRESH_RATE = 0.25 #constant for updating oled and potentiometer values (seconds)
COLUMNS = 3
ROWS = 5
FUNCTION_SELECT_KEYCODE = Keycode.POUND
FUNCTION_SELECT_KEYPRESS_DURATION = 3 #seconds
POT_RANGE = (0, 65535)

#hardware definitions
pixels = neopixel.NeoPixel(board.GP22, 30, brightness=0.9)

keys = keypad.KeyMatrix(
    row_pins=(board.GP21, board.GP20, board.GP19, board.GP18, board.GP17),
    column_pins=(board.GP11, board.GP12, board.GP13),
    columns_to_anodes=False,
)
# Create the I2C interface.
i2c = busio.I2C(board.GP1, board.GP0)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
#graphic = run_oled.Graphic(oled=oled) # TODO 

#create a performance timer object
timer = utils.Timer()
key_event_timer = utils.Timer()
neopixel_refresh_timer = utils.Timer()

kbd = Keyboard(usb_hid.devices)

def key_to_pixel_map(key_number):
    row = key_number // COLUMNS
    column = (key_number % COLUMNS)
    if row % 2 == 1:
        column = COLUMNS - column - 1
    return row * COLUMNS + column

def get_potentiometer_value():
    #print analog value
    print((potentiometer.value,))
    return potentiometer.value

def get_key_events(macro_profile, rgb : tuple) -> 'tuple[bool, bool]': #default function mode
    key_event = keys.events.get()
    function_select_mode = False
    try:
        if key_event:
            print(key_event)
            key_code = macro_profile.map_keypress_to_keycode(key_event)
            print('key code {}'.format(key_code))
            if key_event.pressed:
                key_event_timer.start()
                pixels[key_to_pixel_map(key_event.key_number)] = rgb
                if (key_code != None) or (key_code != FUNCTION_SELECT_KEYCODE):
                    print('sending keycode')
                    kbd.press(key_code) #INSERT DICT MAPPING
                    time.sleep(0.05) # TODO fix me
            if key_event.released: #and (key_code is not None): 
                kbd.release(key_code)

            if key_code == FUNCTION_SELECT_KEYCODE:
                print('function select key pressed')
                if (key_event_timer.update() >= FUNCTION_SELECT_KEYPRESS_DURATION):
                    function_select_mode = True
            else:
                pixels.fill((0, 0, 0))
    except TypeError:
        print('unsupported action occured')
    return function_select_mode
        #check if function selection key has been pressed and held 

def keyboard_function_selector(pot_value : int , macro_profile : Macro_Profile):
    #take input from pot to select function which will return profile
    function_selected = False
    
    key_event = keys.events.get()
    if key_event:
        key_code = macro_profile.map_keypress_to_keycode(key_event)
        if key_event.released and key_code == FUNCTION_SELECT_KEYCODE:
            #TODO 
            #logic to select one of the profiles basedo on linear range of pot values
            profile_inc = POT_RANGE[1]//NUM_PROFILES #~65000/4 =16383
            print('profile increment: {}'.format(profile_inc))
            profile = pot_value//profile_inc
            print('profile selected: {}'.format(profile))
            macro_profile.select_profile(profile_num=profile)
            function_selected = True        
    return macro_profile, function_selected
    
def initialize_behavior() -> None:
    print('initializing')
    pixels.fill((0, 0, 0))  # Begin with pixels off.
    timer.start()
    neopixel_refresh_timer.start()
    
#TODO
def update_neopixel_array(val, max_val=POT_RANGE[1]) -> 'tuple[int, int, int]':
    
    if (val > max_val):
        raise ValueError("val must not be greater than max_val")
    if (val < 0 or max_val < 0):
        raise ValueError("arguments may not be negative")
    
    i = (val * 255 / max_val)
    r = round(math.sin(0.024 * i + 0) * 127 + 128)
    g = round(math.sin(0.024 * i + 2) * 127 + 128)
    b = round(math.sin(0.024 * i + 4) * 127 + 128)
    return (r,g,b)
    
    
def run_behaivor() -> None:
    
    #initial profile NUMPAD
    macro_profile = Macro_Profile(1)
    initialize_behavior()
    
    #initialize all state flags 
    function_selection_state_exit = False
    function_key_event_state_exit = False
    pot_value = 0
    rgb = (255, 0, 0) #initial rgb -> red
    
    current_state = 'key_event'
    
    while True:
        #executes every time
        if (timer.update() >= REFRESH_RATE):
            pot_value = get_potentiometer_value()
            #graphic.update_graphic()
            timer.restart()
            print('current state: {}'.format(current_state))
        
        #should call keyboard function selector based off keypress 
        if current_state == 'function_select':
            #do behavior
            macro_profile, function_selected = keyboard_function_selector(pot_value, macro_profile) #TODO 
            if function_selected:
                print('macro profile selected')
                function_selection_state_exit = True #enables exit behavior
                current_state = 'key_event'
            #exit behavior
            if function_selection_state_exit: 
                function_selection_state_exit = False #disables exit flag
                pixels.fill((0, 0, 0))  # Begin with pixels off.

        #function selection state exit mode
        if current_state == 'key_event':
            #do behavior
            function_selection_key_ret = get_key_events(macro_profile=macro_profile, rgb=rgb) #enter function selection state
            if (neopixel_refresh_timer.update() >= REFRESH_RATE):
                rgb = update_neopixel_array(val=pot_value)
                neopixel_refresh_timer.restart()
            
            if function_selection_key_ret:
                print('entering function selection mode')
                function_key_event_state_exit = True #enables exit behavior
                current_state = 'function_select'
            #exit behavior 
            if function_key_event_state_exit:       
                function_key_event_state_exit = False #disables state entry
        

run_behaivor()