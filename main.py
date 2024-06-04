import pyautogui as pyg
from PIL import Image, ImageGrab
from pynput import keyboard
from time import sleep
from typing import Tuple
from get_window import get_scrcpy_window_geometry
from data import *

pyg.FAILSAFE = False

scrolls_left: int = MAX_SCROLLS
scroll_down: bool = True

space_pressed: bool = False
backspace_pressed: bool = False
enter_pressed: bool = False

window_geometry: Tuple = get_scrcpy_window_geometry()

ZOOM = window_geometry[3]/NORMAL_GEOMETRY[3]

# set all the sizes for all the variables by deviding by zoom and adding the windows x and y coords
Y_OFFSET_UPGRADE_MENU = int(Y_OFFSET_UPGRADE_MENU*ZOOM)
MIDDLE_X = int(MIDDLE_X*ZOOM) + window_geometry[0]
TOP_SCROLL_Y = int(TOP_SCROLL_Y*ZOOM) + window_geometry[1]
HALF_SCROLL = int(HALF_SCROLL*ZOOM) + window_geometry[1]
BOTTOM_SCROLL_Y = int(BOTTOM_SCROLL_Y*ZOOM) + window_geometry[1]
MAX_CHECK_X = int(MAX_CHECK_X*ZOOM)
UPGRADE = (int(UPGRADE[0]*ZOOM) + window_geometry[0], int(UPGRADE[1]*ZOOM) + window_geometry[1])
TOP_UPGRADE = (int(TOP_UPGRADE[0]*ZOOM) + window_geometry[0], int(TOP_UPGRADE[1]*ZOOM) + window_geometry[1])
EXPLINATION_MARK_OFFSET = int(EXPLINATION_MARK_OFFSET*ZOOM)

for sprite_path in SPRITES:
    new_sprite_path = sprite_path.replace('.png', '_resized.png')
    image = Image.open(sprite_path)

    new_image = image.resize((int(image.width*ZOOM), int(image.height*ZOOM)))
    new_image.save(new_sprite_path)

def on_press(key):
    global space_pressed
    global backspace_pressed
    global enter_pressed

    if key == keyboard.Key.space: space_pressed = True
    elif key == keyboard.Key.backspace: backspace_pressed = True
    elif key == keyboard.Key.enter: enter_pressed = True

def on_release(key):
    global space_pressed
    global backspace_pressed
    global enter_pressed

    if key == keyboard.Key.space: space_pressed = False
    elif key == keyboard.Key.backspace: backspace_pressed = False
    elif key == keyboard.Key.enter: enter_pressed = False                             

def scroll():
    global scrolls_left
    global scroll_down

    if scroll_down == True:
        start_y = BOTTOM_SCROLL_Y
        target_y = HALF_SCROLL
    else:
        start_y = TOP_SCROLL_Y
        target_y = HALF_SCROLL

    # cant scroll on box so just click to the side so upgrade box is not blocking
    pyg.click(MIDDLE_X-int(200*ZOOM), start_y-int(100*ZOOM))

    pyg.mouseDown(MIDDLE_X, start_y)
    pyg.moveTo(MIDDLE_X, target_y, duration=1)
    pyg.mouseUp()

    scrolls_left -= 1

    if scrolls_left <= 0:
        scrolls_left = MAX_SCROLLS
        scroll_down = not scroll_down

def check_for_and_close_popup(done_once: bool = False):
    try:
        for popup in pyg.locateAllOnScreen('big_cross_resized.png', confidence=0.9, grayscale=True, region=window_geometry):
            pyg.click(popup.left+popup.width/ZOOM/2, popup.top+popup.height/ZOOM/2)
            if not done_once: check_for_and_close_popup(True)
            break
    except: return

def check_for_and_close_explaination():
    try:
        for mark in pyg.locateAllOnScreen('explination_mark_resized.png', confidence=0.85, grayscale=True, region=window_geometry):
            y_pos: int = mark.top+EXPLINATION_MARK_OFFSET
            for i in range(-MAX_CHECK_X, MAX_CHECK_X):
                if ImageGrab.grab().getpixel((mark.left+i, y_pos)) == (255, 255, 255):
                    pyg.click(mark.left+i, y_pos)
                    break

            check_for_and_close_popup()
    except: return

def crates():
    try:
        for crate in pyg.locateAllOnScreen('crate_resized.png', confidence=0.8, grayscale=True, region=window_geometry):
            pyg.click(crate.left+crate.width/2, crate.top+crate.height/2)

        for crate in pyg.locateAllOnScreen('crate1_resized.png', confidence=0.8, grayscale=True, region=window_geometry):
            pyg.click(crate.left+crate.width/2, crate.top+crate.height/2)

        for crate in pyg.locateAllOnScreen('crate4_resized.png', confidence=0.8, grayscale=True, region=window_geometry):
            pyg.click(crate.left+crate.width/2, crate.top+crate.height/2)

    except: return

def upgrades():
    pyg.click(UPGRADE)
    sleep(1)
    pyg.click(TOP_UPGRADE)
    check_for_and_close_popup()

def process_keys():
    if space_pressed: exit()
    elif backspace_pressed:
        while 1:
            if enter_pressed: break
            sleep(0.1)

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

listener.start()

while 1:
    process_keys()
    try:
        check_for_and_close_explaination()
        upgrades()
        crates()
        for upgrade in pyg.locateAllOnScreen('upgrade_resized.png', confidence=0.8, grayscale=True, region=window_geometry):
            print(upgrade)
            check_for_and_close_popup()

            station_location: Tuple = (upgrade.left+upgrade.width, upgrade.top+30*ZOOM)

            if station_location[1] > window_geometry[1]+window_geometry[3]-Y_OFFSET_UPGRADE_MENU*2: continue

            pyg.click(station_location)
            sleep(0.5)

            check_for_and_close_popup()
            process_keys()

            new_click_location: Tuple = (upgrade.left+upgrade.width, upgrade.top-Y_OFFSET_UPGRADE_MENU)
            screenshot = ImageGrab.grab()
            print(screenshot.getpixel(new_click_location))
            #if pyg.pixelMatchesColor(new_click_location[0], new_click_location[1], (85, 197, 251), tolerance=2) or pyg.pixelMatchesColor(new_click_location[0], new_click_location[1], (68, 158, 203), tolerance=2):
            if screenshot.getpixel(new_click_location) == (75, 189, 255) or screenshot.getpixel(new_click_location) == (79, 190, 255):
                for i in range(0, 20):
                    process_keys()
                    pyg.click(new_click_location)
            else:
                for i in range(-MAX_CHECK_X, MAX_CHECK_X):
                    pyg.moveTo(new_click_location[0]+i, new_click_location[1])
                    if screenshot.getpixel((new_click_location[0]+i, new_click_location[1])) == (75, 189, 255) or screenshot.getpixel((new_click_location[0]+i, new_click_location[1])) == (79, 190, 255):
                        click_location = (new_click_location[0]+i, new_click_location[1])
                        for i in range(0, 20):
                            process_keys()
                            pyg.click(click_location)
                        break

            check_for_and_close_popup()

        if MAX_SCROLLS > 0: scroll()

    except Exception as e:
        print(e)
        check_for_and_close_popup()
        crates()
        if MAX_SCROLLS > 0: scroll()
