import os
import csv

class FileManager:
    def __init__(self, directory="mod_files"):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def load_mods_from_file(self, filename):
        filepath = os.path.join(self.directory, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filename} not found in {self.directory}")
        
        mods = []
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                mods.append(row)
        return mods
    
    def save_mods_to_file(self, filename, mod_data):
        filepath = os.path.join(self.directory, filename)
        with open(filepath, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ["Mod", "Tag", "Tier", "iLvl", "Weight", "Prefix%", "Weight%"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for mod in mod_data:
                writer.writerow(mod)
    
    def list_files(self):
        return [f for f in os.listdir(self.directory) if f.endswith(".csv")]
