import pyautogui as pyg
from pynput import keyboard
from time import sleep
from typing import Tuple
from data import *

scrolls_left: int = MAX_SCROLLS
scroll_down: bool = True

space_pressed: bool = False

def on_press(key):
    global space_pressed
    if key == keyboard.Key.space: space_pressed = True

def on_release(key):
    global space_pressed
    if key == keyboard.Key.space: space_pressed = False

def scroll():
    global scrolls_left
    global scroll_down

    if scroll_down == True:
        start_y = BOTTOM_SCROLL_Y
        target_y = HALF_SCROLL
    else:
        start_y = TOP_SCROLL_Y
        target_y = HALF_SCROLL

    pyg.mouseDown(MIDDLE_X, start_y)
    pyg.moveTo(MIDDLE_X, target_y, duration=1)
    pyg.mouseUp()

    scrolls_left -= 1

    if scrolls_left <= 0:
        scrolls_left = MAX_SCROLLS
        scroll_down = not scroll_down

def check_for_and_close_popup(done_once: bool = False):
    try:
        for popup in pyg.locateAllOnScreen('big_cross.png', confidence=0.90, grayscale=True):
            pyg.click(popup.left+popup.width/2, popup.top+popup.height/2)
            if not done_once: check_for_and_close_popup(True)
            break
    except: return

def get_key_exit():
    if space_pressed: exit()

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

listener.start()

while 1:
    get_key_exit()
    try:
        for upgrade in pyg.locateAllOnScreen('upgrade.png', confidence=0.90, grayscale=True):
            check_for_and_close_popup()

            pyg.click(upgrade.left+upgrade.width, upgrade.top+30)
            sleep(0.5)

            check_for_and_close_popup()

            new_click_location: Tuple = (upgrade.left+upgrade.width, upgrade.top-Y_OFFSET_UPGRADE_MENU)
            if pyg.pixelMatchesColor(new_click_location[0], new_click_location[1], (85, 197, 251), tolerance=2) or pyg.pixelMatchesColor(new_click_location[0], new_click_location[1], (68, 158, 203), tolerance=2):
                for i in range(0, 20):
                    get_key_exit()
                    pyg.click(new_click_location)
                    sleep(0.1)
            else:
                for i in range(-MAX_CHECK_X, MAX_CHECK_X):
                    if pyg.pixelMatchesColor(new_click_location[0]+i, new_click_location[1], (85, 197, 251), tolerance=2) or pyg.pixelMatchesColor(new_click_location[0]+i, new_click_location[1], (68, 158, 203), tolerance=2):
                        for i in range(0, 20):
                            get_key_exit()
                            pyg.click(new_click_location[0]+i, new_click_location[1])
                            sleep(0.1)
                        break

        scroll()

    except:
        check_for_and_close_popup()
        scroll()
        sleep(1)