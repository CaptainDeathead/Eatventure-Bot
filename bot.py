import traceback
from plyer import notification
from PIL import Image, ImageGrab
from os import remove, path, _exit
from vncdotool import api
from imageUtils import _locateAll_opencv
from pynput import keyboard
from time import sleep
from typing import Tuple
from data import *

client = api.connect(PHONE_IP_ADDRESS, timeout=3.0)

def get_screen() -> Image:
    client.captureScreen('shot.png')

    while not path.exists("shot.png"):
        sleep(0.01)

    with Image.open("shot.png") as image:
        image_copy = image.copy()

    remove("shot.png")

    return image_copy

extenalally_managed: bool = False
paused: bool = False
off: bool = False

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
RENOVATION_UPGRADE_MIDPOINT = (int(RENOVATION_UPGRADE_MIDPOINT[0]*ZOOM + window_geometry[0]), int(RENOVATION_UPGRADE_MIDPOINT[1]*ZOOM + window_geometry[1]))
RENOVATION_UPGRADE = (int(RENOVATION_UPGRADE[0]*ZOOM + window_geometry[0]), int(RENOVATION_UPGRADE[1]*ZOOM + window_geometry[1]))
RENOVATE_BUTTON = (int(RENOVATE_BUTTON[0]*ZOOM + window_geometry[0]), int(RENOVATE_BUTTON[1]*ZOOM + window_geometry[1]))
OPEN_BUTTON = (int(OPEN_BUTTON[0]*ZOOM + window_geometry[0]), int(OPEN_BUTTON[1]*ZOOM + window_geometry[1]))
EXPLINATION_MARK_OFFSET = int(EXPLINATION_MARK_OFFSET*ZOOM)
NO_GO_BOTTOM_Y = int(NO_GO_BOTTOM_Y*ZOOM)
NO_GO_TOP_Y = int(NO_GO_TOP_Y*ZOOM)

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

    if y > NO_GO_BOTTOM_Y or y < NO_GO_TOP_Y:
        print("Attempted to click in one of the no-go zone's")
        return

    client.mouseMove(int(x - window_geometry[0]), int(y - window_geometry[1]))
    client.mousePress(1)

    sleep(0.05)

def click_no_verify(*args) -> None:
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

    client.mouseMove(MIDDLE_X, start_y)
    client.mouseDown(1)

    step: int = 50

    if target_y < start_y: step = -50
    
    for y in range(start_y, target_y, step):
        client.mouseMove(MIDDLE_X, y)
        sleep(0.05)

    client.mouseUp(1)

    scrolls_left -= 1

    if scrolls_left <= 0:
        scrolls_left = MAX_SCROLLS
        scroll_down = not scroll_down

def check_for_and_close_popup(done_once: bool = False) -> bool: # returns true if a popup is found (checks for popups twice to be sure)
    try:
        found_popup = False

        for popup in _locateAll_opencv(sprite_images['big_cross_resized.png'], get_screen(), confidence=POPUP_CONFORDENCE, grayscale=True):
            found_popup = True
            click_no_verify(popup.left+popup.width/ZOOM/2, popup.top+popup.height/ZOOM/2)
            if not done_once: check_for_and_close_popup(True)
            break

        return found_popup

    except: return False

def check_for_and_close_explaination():
    try:
        for mark in _locateAll_opencv(sprite_images['explination_mark_resized.png'], get_screen(), confidence=EXPLINATION_CONFORDENCE, grayscale=True):
            y_pos: int = mark.top+EXPLINATION_MARK_OFFSET
            for i in range(-MAX_CHECK_X, MAX_CHECK_X):
                if ImageGrab.grab().getpixel((mark.left+i, y_pos)) == (255, 255, 255):
                    click(mark.left+i, y_pos)
                    break

            check_for_and_close_popup()
    except: return

def crates():
    try:
        for crate in _locateAll_opencv(sprite_images['crate_resized.png'], get_screen(), confidence=CRATES_CONFORDENCE, grayscale=True):
            click(crate.left+crate.width/2, crate.top+crate.height/2)
            check_for_and_close_popup()

        for crate in _locateAll_opencv(sprite_images['crate1_resized.png'], get_screen(), confidence=CRATES_CONFORDENCE, grayscale=True):
            click(crate.left+crate.width/2, crate.top+crate.height/2)
            check_for_and_close_popup()

        for crate in _locateAll_opencv(sprite_images['crate4_resized.png'], get_screen(), confidence=CRATES_CONFORDENCE, grayscale=True):
            click(crate.left+crate.width/2, crate.top+crate.height/2)
            check_for_and_close_popup()

    except: return

def upgrades():
    click_no_verify(UPGRADE)
    for _ in range(10):
        sleep(0.25)
        click_no_verify(TOP_UPGRADE)
    check_for_and_close_popup()

def check_renovation() -> bool:
    screenshot = get_screen()

    for renovate_upgrade in _locateAll_opencv(sprite_images["renovate_upgrade_resized.png"], screenshot, confidence=RENOVATE_UPGRADE_CONFORDENCE, grayscale=True):
        if renovate_upgrade.top + renovate_upgrade.height < NO_GO_BOTTOM_Y: continue
        if renovate_upgrade.left < 46*ZOOM or renovate_upgrade.left > 70*ZOOM: continue

        print("Renovating...")
        notification.notify(title="Eatventure-Bot: Renovating...", message="Sit tight while we move to a new restraunt / city!")
        click_no_verify(renovate_upgrade.left, renovate_upgrade.top + renovate_upgrade.height)
        click_no_verify(RENOVATION_UPGRADE)
        sleep(1)
        click_no_verify(RENOVATE_BUTTON)
        sleep(8)
        for _ in range(5): click_no_verify(OPEN_BUTTON)

        return True
    
    return False

def process_keys() -> None:
    global paused
    global off

    if space_pressed:
        client.disconnect()

        print("Goodbye!")
        notification.notify(title="Eatventure-Bot: Goodbye...", message="Thanks for using the bot!")       

        if extenalally_managed:
            off = True
            return
        else: _exit(0)
    
    elif backspace_pressed:
        print("@@@!!! SESSION PAUSED !!!@@@")
        notification.notify(title="Eatventure-Bot: Session Paused...", message="You can resume anytime by pressing 'f9'")

        paused = True

        while 1:
            if enter_pressed:
                print("@@@!!! RESUMING SESSION !!!@@@")
                notification.notify(title="Eatventure-Bot: Resuming Session...", message="You can pause anytime by pressing 'f7'")
                
                paused = False                    
                break

            sleep(0.1)

def step_bot():
    if off: return
    process_keys()
    try:
        check_for_and_close_explaination()
        upgrades()
        crates()

        renovating: bool = check_renovation()
        if renovating: return

        for upgrade in _locateAll_opencv(sprite_images['upgrade_resized.png'], get_screen(), confidence=STATION_UPGRADES_CONFORDENCE, grayscale=True):
            print(upgrade)
            check_for_and_close_popup()

            station_location: Tuple = (upgrade.left+upgrade.width, upgrade.top+30*ZOOM)

            if station_location[1] > window_geometry[1]+window_geometry[3]-Y_OFFSET_UPGRADE_MENU*2: continue

            click(station_location)
            sleep(0.5)

            check_for_and_close_popup()
            process_keys()
            if off: return

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
                    if off: return
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
                            if off: return
                            click(scan_pixel_location)
                            
                        break

            check_for_and_close_popup()

        if MAX_SCROLLS > 0: scroll()

    except Exception as e:
        print(traceback.format_exc())

        check_for_and_close_popup()
        crates()

        if MAX_SCROLLS > 0: scroll()

def main(run: bool = True):
    global extenalally_managed
    global client

    try: client.disconnect()
    except: pass

    extenalally_managed = not run
    client = api.connect(PHONE_IP_ADDRESS)

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)

    listener.start()

    while run:
        bot_status: int | None = step_bot()

if __name__ == "__main__":
    main()