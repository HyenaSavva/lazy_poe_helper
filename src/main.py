import tkinter as tk
from tkinter import ttk
import pyautogui
from controllers.file_manager import FileManager
from views.magic_craft_view import MagicCraftTab
from views.rare_craft_view import RareCraftTab
import sv_ttk
import pywinstyles
import pystray
from pystray import MenuItem as item
from PIL import Image

class Sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#2F2F2F', width=40)
        self.pack_propagate(False)

class MainApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        file_manager = FileManager()

        # self.sidebar = Sidebar(self)
        # self.sidebar.pack(side="left", fill="y")

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        magic_tab = MagicCraftTab(notebook)
        notebook.add(magic_tab, text="Magic Craft")

        rare_tab = RareCraftTab(notebook)
        notebook.add(rare_tab, text="Rare Craft")

        sv_ttk.set_theme("dark", parent)

def minimize_to_tray(root):
    hide_window(root)
    create_tray_icon(root)

def hide_window(root):
    root.withdraw()

def show_window(icon, root):
    root.deiconify()
    icon.stop()

def on_closing(root, icon=None):
    if icon:
        icon.stop()
    root.destroy()

def create_tray_icon(root):
    icon_image = Image.open('assets/icon.ico').resize((24, 24))

    menu = (item('Open Application', lambda: show_window(icon, root)),
            item('Exit', lambda: on_closing(root, icon)))

    icon = pystray.Icon("PoE Helper", icon_image, "LazyCraft Helper", menu)
    icon.run()

def main():
    root = tk.Tk()
    
    root.wm_attributes("-topmost", 1)

    root.title("Crafting App")
    root.geometry("600x700")
    # root.resizable(0, 0)

    pyautogui.PAUSE = 0
    pywinstyles.change_header_color(root, color="#1c1c1c")

    MainApp(root).pack(expand=True, fill="both")
    
    # root.protocol("WM_DELETE_WINDOW", lambda: minimize_to_tray(root))

    root.mainloop()

if __name__ == "__main__":
    main()
