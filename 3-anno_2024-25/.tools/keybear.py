import sys
import os
import time
import threading
try:
    from pyautogui import *
except:
    print("PyAutoGui not found. Downloading...")
    import os
    os.system("pip install pyautogui")
    from pyautogui import *

try:
    from pynput import keyboard
except:
    print("PyAutoGui not found. Downloading...")
    import os
    os.system("pip install pynput")
    from pynput import keyboard

from pyautogui import write as typewrite
from pyautogui import typewrite as fast

# Global flag to interrupt typing and a reference to the typing thread.
stop_typing = False
typing_thread = None

def install_pyautogui():
    pass

def read_file(filepath):
    """
    Read file contents while ignoring decoding errors.
    Returns a list of lines.
    """
    try:
        with open(filepath, errors='ignore') as f:
            lines = f.readlines()
            f.seek(0)
            fi = f.read()
        return lines, fi
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def type_lines(lines):
    """
    Simulates typing each line character by character.
    If the global flag 'stop_typing' is set True, the function returns immediately.
    """
    global stop_typing
    for line in lines:
        for char in line:
            if stop_typing:
                print("Typing interrupted!")
                return
            typewrite(char)
    print("Finished typing file contents.")

def start_typing(lines):
    """
    Starts the type_lines function in a separate thread.
    Resets the stop flag and updates the global typing_thread reference.
    """
    global stop_typing, typing_thread
    stop_typing = False  # Reset the interruption flag
    
    # Create and start a new thread for typing.
    typing_thread = threading.Thread(target=type_lines, args=(lines,))
    typing_thread.start()

def on_press_factory(lines):
    """
    Returns on_press and on_release functions to control typing and exit.
    - Right Shift triggers typing all lines.
    - Right Control sets the stop flag for the ongoing typing.
    - Ctrl+V or Esc exits the program.
    """
    pressed_keys = set()

    def on_press(key):
        
        global stop_typing, typing_thread
        try:
            # Track pressed keys (convert char keys to their character representation).
            if hasattr(key, 'char'):
                pressed_keys.add(key.char)
            else:
                pressed_keys.add(key)
            
            # If Right Shift is pressed, start typing in a separate thread.
            if key == keyboard.Key.shift_r:
                # Only start typing if no typing thread is running or it has finished.
                if typing_thread is None or not typing_thread.is_alive():
                    print("Right Shift pressed. Starting to type file contents...")
                    start_typing(lines)
                else:
                    print("Typing is already in progress.")
            
            # If Right Ctrl is pressed, set the stop flag.
            if key == keyboard.Key.ctrl_r:
                stop_typing = True
                print("Right Control pressed. Stopping typing...")

            if key == keyboard.Key.alt_gr:
                print("fast type started")
                fast(fi)
                print("fast type finished")

            if key == keyboard.Key.esc:
                print("Esc pressed. Exiting...")
                exit(0)
                return False

        except Exception as e:
            print(f"Error in on_press: {e}")

    def on_release(key):
        try:
            if hasattr(key, 'char'):
                pressed_keys.discard(key.char)
            else:
                pressed_keys.discard(key)
        except Exception as e:
            print(f"Error in on_release: {e}")

    return on_press, on_release

install_pyautogui()

if len(sys.argv) != 2:
    print("Usage: python keybear.py <file>")
    sys.exit(1)
filepath = sys.argv[1]
if not os.path.isfile(filepath):
    print(f"File '{filepath}' does not exist.")
    exit(1)

lines, fi = read_file(filepath)
if not lines:
    print("File is empty or could not be read.")
    sys.exit(1)
print(f"Loaded {len(lines)} lines from '{filepath}'.")



on_press, on_release = on_press_factory(lines)
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


