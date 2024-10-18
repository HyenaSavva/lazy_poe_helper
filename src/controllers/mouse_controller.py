import random
import time
import pyautogui
import pytweening
from controllers.keyboard_controller import KeyboardController
from pynput.keyboard import Key, Listener

class MouseController:
    def __init__(self, main_controller, duration=0.2):
        """
        MouseController pentru gestionarea mișcărilor mouse-ului și a altor funcții legate de mouse.
        """
        self.keyboard = KeyboardController()
        self.main_controller = main_controller  # Referință la controller-ul principal
        self.duration = duration
        pyautogui.PAUSE = 0  # Dezactivare pauză implicită între mișcări
        
    def check_stop_loop(self, stop_key):
        """
        Verifică dacă tasta de oprire a fost apăsată și oprește bucla.
        
        :param stop_key: Tasta configurată pentru oprirea buclei
        """
        def on_press(key):
            try:
                if key == Key[stop_key]:
                    self.main_controller.stop_loop = True
                    print(f"{stop_key} apăsată, oprind bucla.")
            except KeyError:
                print(f"Error: Tasta '{stop_key}' este invalidă.")
                
        listener = Listener(on_press=on_press)
        listener.start()

    def move(self, x, y, steps=30, variation=0, final_variation=2):
        start_x, start_y = pyautogui.position()

        points = [(pytweening.easeInOutQuad(i / steps), pytweening.easeInOutQuad(i / steps)) for i in range(steps + 1)]

        for i in range(steps):
            if self.main_controller.stop_loop:
                print("Mișcarea mouse-ului a fost oprită.")
                return  # Ieșire din funcție dacă loop-ul este oprit
            t = points[i][0] 
            new_x = start_x + t * (x - start_x) + random.uniform(-variation, variation)
            new_y = start_y + t * (y - start_y) + random.uniform(-variation, variation)

            pyautogui.moveTo(new_x, new_y)
            time.sleep(self.duration / steps) 

        final_x = x + random.uniform(-final_variation, final_variation)
        final_y = y + random.uniform(-final_variation, final_variation)
        pyautogui.moveTo(final_x, final_y)

    def click(self, button='left', delay=0.1):
        """
        Efectuează un click cu mouse-ul.
        
        :param button: Butonul de click ('left' sau 'right')
        """
        time.sleep(delay)
        pyautogui.click(button=button, duration=0.1)

    def right_click(self):
        """
        Efectuează un click dreapta.
        """
        self.click(button='right')

    def scroll(self, clicks=1):
        """
        Simulează derularea mouse-ului.
        
        :param clicks: Numărul de unități de derulare (poate fi negativ pentru a derula în jos)
        """
        pyautogui.scroll(clicks)
