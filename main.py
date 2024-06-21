import traceback
from PIL import Image, ImageGrab
from os import remove, path
from vncdotool import api
from imageUtils import _locateAll_opencv
from pynput import keyboard
from time import sleep
from typing import Tuple
#from twisted.internet import reactor, defer
#from get_window import get_scrcpy_window_geometry
from data import *

client = api.connect(PHONE_IP_ADDRESS)

def get_screen() -> Image:
    client.captureScreen('shot.png')

    while not path.exists("shot.png"):
        sleep(0.01)

    image = Image.open("shot.png")
    remove("shot.png")

    return image

scrolls_left: int = MAX_SCROLLS
scroll_down: bool = True

space_pressed: bool = False
backspace_pressed: bool = False
enter_pressed: bool = False

#window_geometry: Tuple = get_scrcpy_window_geometry()
width, height = get_screen().size
window_geometry: Tuple = (0, 0, width, height)

print(f"@@@!!! FOUND DEVICE WIDTH AND HEIGHT -> CONFIGURING GEOMETRY AS SIZE: {window_geometry} !!!@@@")

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

sprite_images = {}

for sprite_path in SPRITES:
    new_sprite_path = sprite_path.replace('.png', '_resized.png')
    image = Image.open("assets/" + sprite_path)

    new_image = image.resize((int(image.width*ZOOM), int(image.height*ZOOM)))

    sprite_images[new_sprite_path] = new_image

    new_image.save("assets/" + new_sprite_path)

def click(*args) -> None:
    if len(args) == 1 and isinstance(args[0], tuple):
        x, y = args[0]
    else:
        x, y = args

    client.mouseMove(int(x - window_geometry[0]), int(y - window_geometry[1]))
    client.mousePress(1)

    sleep(0.05)

def on_press(key):
    global space_pressed
    global backspace_pressed
    global enter_pressed

    if key == keyboard.Key.f8: space_pressed = True
    elif key == keyboard.Key.f7:
        backspace_pressed = True
        enter_pressed = False

    elif key == keyboard.Key.f9:
        enter_pressed = True
        backspace_pressed = False

def on_release(key):
    global space_pressed
    global backspace_pressed
    global enter_pressed

    if key == keyboard.Key.space: space_pressed = False
    elif key == keyboard.Key.backspace: backspace_pressed = False
    elif key == keyboard.Key.enter: enter_pressed = False                             

def scroll():
    # TODO: PATCH THIS TO WORK WITH VNCDOTOOL

    global scrolls_left
    global scroll_down

    if scroll_down == True:
        start_y = BOTTOM_SCROLL_Y
        target_y = HALF_SCROLL
    else:
        start_y = TOP_SCROLL_Y
        target_y = HALF_SCROLL

    # cant scroll on box so just click to the side so upgrade box is not blocking
    click(MIDDLE_X-int(200*ZOOM), start_y-int(100*ZOOM))

    """
    pyg.mouseDown(MIDDLE_X, start_y)
    pyg.moveTo(MIDDLE_X, target_y, duration=1)
    pyg.mouseUp()
    """

    scrolls_left -= 1

    if scrolls_left <= 0:
        scrolls_left = MAX_SCROLLS
        scroll_down = not scroll_down

def check_for_and_close_popup(done_once: bool = False) -> bool: # returns true if a popup is found (checks for popups twice to be sure)
    try:
        found_popup = False

        for popup in _locateAll_opencv(sprite_images['big_cross_resized.png'], get_screen(), confidence=0.8, grayscale=True):
            found_popup = True
            click(popup.left+popup.width/ZOOM/2, popup.top+popup.height/ZOOM/2)
            if not done_once: check_for_and_close_popup(True)
            break

        return found_popup

    except: return False

def check_for_and_close_explaination():
    try:
        for mark in _locateAll_opencv(sprite_images['explination_mark_resized.png'], get_screen(), confidence=0.85, grayscale=True):
            y_pos: int = mark.top+EXPLINATION_MARK_OFFSET
            for i in range(-MAX_CHECK_X, MAX_CHECK_X):
                if ImageGrab.grab().getpixel((mark.left+i, y_pos)) == (255, 255, 255):
                    click(mark.left+i, y_pos)
                    break

            check_for_and_close_popup()
    except: return

def crates():
    try:
        for crate in _locateAll_opencv(sprite_images['crate_resized.png'], get_screen(), confidence=0.8, grayscale=True):
            click(crate.left+crate.width/2, crate.top+crate.height/2)
            check_for_and_close_popup()

        for crate in _locateAll_opencv(sprite_images['crate1_resized.png'], get_screen(), confidence=0.8, grayscale=True):
            click(crate.left+crate.width/2, crate.top+crate.height/2)
            check_for_and_close_popup()

        for crate in _locateAll_opencv(sprite_images['crate4_resized.png'], get_screen(), confidence=0.8, grayscale=True):
            click(crate.left+crate.width/2, crate.top+crate.height/2)
            check_for_and_close_popup()

    except: return

def upgrades():
    click(UPGRADE)
    sleep(1)
    click(TOP_UPGRADE)
    check_for_and_close_popup()

def process_keys():
    if space_pressed:
        print("Goodbye!")
        exit()
    
    elif backspace_pressed:
        print("@@@!!! SESSION PAUSED !!!@@@")

        while 1:
            if enter_pressed:
                print("@@@!!! RESUMING SESSION !!!@@@")
                break

            sleep(0.1)

def main():
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
            for upgrade in _locateAll_opencv(sprite_images['upgrade_resized.png'], get_screen(), confidence=0.77, grayscale=True):
                print(upgrade)
                check_for_and_close_popup()

                station_location: Tuple = (upgrade.left+upgrade.width, upgrade.top+30*ZOOM)

                if station_location[1] > window_geometry[1]+window_geometry[3]-Y_OFFSET_UPGRADE_MENU*2: continue

                click(station_location)
                sleep(0.5)

                check_for_and_close_popup()
                process_keys()

                new_click_location: Tuple = (upgrade.left+upgrade.width, upgrade.top-Y_OFFSET_UPGRADE_MENU)
                screenshot = get_screen().convert('RGB')

                pixel_color = screenshot.getpixel(new_click_location)
                print(pixel_color)

                if pixel_color == (75, 189, 255) or pixel_color == (79, 190, 255):
                    # click the button once to see if there is a popup, if there is one quit, else press it 20 more times without checking for popup
                    click(new_click_location)
                            
                    if check_for_and_close_popup(): continue

                    for i in range(0, 20):
                        process_keys()
                        click(new_click_location)
                else:
                    for i in range(-MAX_CHECK_X, MAX_CHECK_X):
                        scan_pixel_location = (new_click_location[0]+i, new_click_location[1])

                        #pyg.moveTo(scan_pixel_location)
                        if screenshot.getpixel(scan_pixel_location) == (75, 189, 255) or screenshot.getpixel(scan_pixel_location) == (79, 190, 255):
                            
                            # click the button once to see if there is a popup, if there is one quit, else press it 20 more times without checking for popup
                            click(scan_pixel_location)
                            
                            if check_for_and_close_popup(): break

                            for i in range(0, 20):
                                process_keys()
                                click(scan_pixel_location)
                                
                            break

                check_for_and_close_popup()

            if MAX_SCROLLS > 0: scroll()

        except Exception as e:
            print(traceback.format_exc())
            print(e)
            check_for_and_close_popup()
            crates()
            if MAX_SCROLLS > 0: scroll()

if __name__ == "__main__":
    main()
