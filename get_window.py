from Xlib import display
from data import PHONE_WINDOW

def get_scrcpy_window_geometry():
    # connect to the x server
    d = display.Display()
    
    # get the root window
    root = d.screen().root
    
    # get all windows
    window_list = root.get_full_property(d.intern_atom('_NET_CLIENT_LIST'), 0).value
    
    for window_id in window_list:
        window = d.create_resource_object('window', window_id)
        
        # get the window name
        window_name = window.get_wm_name()
        
        if window_name and PHONE_WINDOW in window_name:
            geometry = window.get_geometry()
            translated_coords = window.translate_coords(root, 0, 0)
            return abs(translated_coords.x), abs(translated_coords.y), geometry.width, geometry.height
    
    raise Exception("No window found! Try changing PHONE_WINDOW in data and try again.")
    return None

if __name__ == "__main__":
    geometry = get_scrcpy_window_geometry()
    print(geometry)