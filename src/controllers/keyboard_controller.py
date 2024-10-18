import json
import time
import pyperclip
from pynput.keyboard import Controller as Keyboard
from pynput.keyboard import Key, Listener

class KeyboardController:
    def __init__(self):
        self.keyboard = Keyboard()
        self.pressed_keys = set()  # Store pressed keys
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        
        self.config = self.load_options()
        
        self.key_press_delay = self.config.get("execution_delays", {}).get("key_press_delay", 0.1)
        self.clipboard_copy_delay = self.config.get("execution_delays", {}).get("clipboard_copy_delay", 0.1)

    @staticmethod
    def load_options():
        try:
            with open("config/options.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: Options file not found. Using defaults.")
            return {}
    
    def on_press(self, key):
        try:
            self.pressed_keys.add(key)
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
        except AttributeError:
            pass

    def is_pressed(self, key):
        """Check if a specific key (like Key.f1) is currently pressed."""
        return key in self.pressed_keys

    def press_button(self, button):
        """Simulate pressing and releasing a key."""
        self.keyboard.press(button)
        self.keyboard.release(button)

    def get_ctrl_c(self):
        """Simulate pressing Ctrl + C and return clipboard data."""
        ctrl = Key.ctrl
        c = 'c'
        
        self.clipboard_clear()
        
        self.keyboard.press(ctrl)
        self.keyboard.press(c)
        time.sleep(self.key_press_delay)  # Use configurable delay
        self.keyboard.release(c)
        self.keyboard.release(ctrl)
        time.sleep(self.key_press_delay)

    def get_ctrl_alt_c(self):
        """Simulate pressing Ctrl + Alt + C."""
        ctrl = Key.ctrl
        alt = Key.alt
        c = 'c'

        self.clipboard_clear()
        
        self.keyboard.press(ctrl)
        self.keyboard.press(alt)
        self.keyboard.press(c)
        time.sleep(self.key_press_delay)
        self.keyboard.release(c)
        self.keyboard.release(alt)
        self.keyboard.release(ctrl)
        time.sleep(self.key_press_delay)

    def get_clipboard_data(self):
        """Retrieve data from the clipboard using pyperclip."""
        print("Getting clipboard data...")
        try:
            self.get_ctrl_alt_c()
            time.sleep(self.clipboard_copy_delay)  # Ensure the clipboard operation has completed
            return pyperclip.paste()
        except Exception as e:
            print(f"Error retrieving clipboard data: {e}")
            return None

    def clipboard_clear(self):
        """Clear the clipboard using pyperclip."""
        try:
            pyperclip.copy('')  # Clears the clipboard by copying an empty string
        except Exception as e:
            print(f"Error clearing clipboard: {e}")
