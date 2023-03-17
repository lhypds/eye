from time import sleep
import win32gui
import win32api
from pathlib import Path

import os
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())

def move_window_to_screen(hwnd, screen_number):
    if os.getenv("ENABLE") != "true": return
    
    # Get information about the screen(s)
    screens = win32api.EnumDisplayMonitors()
    print("Number of screens: {}".format(len(screens)))
    
    if screen_number >= len(screens):
        print("Invalid screen number")
        return

    # Get the dimensions of the target screen
    monitor_info = win32api.GetMonitorInfo(screens[screen_number][0])
    work_area = monitor_info["Work"]
    x, y, screen_width, screen_width = work_area
    
    # Get the original size of the window
    window_rect = win32gui.GetWindowRect(hwnd)
    window_width = window_rect[2] - window_rect[0]
    window_height = window_rect[3] - window_rect[1]
    
    # coordinate of the top left corner
    # relative for all monitors
    window_x = window_rect[0]  
    window_y = window_rect[1]

    # Move the window to the target screen
    win32gui.MoveWindow(hwnd, x, y, window_width, window_height, True)

def get_direction():
    f_path = Path("C:\\.keycache\\face_direction.txt")
    f_path.touch(exist_ok=True)
    f = open(f_path, "r")
    face_direction = f.read()
    f.close()
    return face_direction

# Get the handle of the active window
hwnd = win32gui.GetForegroundWindow()

face_direction = get_direction()
if face_direction == "->":
    move_window_to_screen(hwnd, 1)
    print("Move to right screen")
elif face_direction == "<-": 
    move_window_to_screen(hwnd, 0)
    print("Move to left screen")
else:
    print("No move")