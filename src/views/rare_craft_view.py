import tkinter as tk

class RareCraftTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Etichetă și buton pentru Magic Craft
        self.label = tk.Label(self, text="Magic Crafting Options")
        self.label.pack(pady=10)

        self.button = tk.Button(self, text="Start Magic Craft", command=self.start_magic_craft)
        self.button.pack(pady=10)

    def start_magic_craft(self):
        # Aici vei pune logica de craft magic (de exemplu, control mouse/tastatură)
        print("Magic Craft started!")
