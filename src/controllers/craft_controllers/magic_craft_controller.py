import json
import time
from controllers.keyboard_controller import KeyboardController
from controllers.mouse_controller import MouseController
from controllers.mod_parser import ModParser

class MagicCraftController:
    def __init__(self):
        # Load configurations
        self.config = self.load_options()
        self.stash_items_positions = self.load_items_positions()
        
        # Load options
        self.stop_key = self.config.get("stop_key", "f3")  # Default is F3
        self.max_retries = self.config.get("max_retries", 3) 
        self.currency_block = self.config.get("currency_block_size", [42, 42])
        self.item_block = self.config.get("item_block_size", [84, 166])
        self.clipboard_copy_delay = self.config.get("execution_delays", {}).get("clipboard_copy_delay", 0.1)
        mouse_speed = self.config.get("mouse_speed", 0.24)
        
        # Load item positions
        self.orb_of_scouring = self.stash_items_positions['main_currency'][8]['position']
        self.orb_of_augmentation = self.stash_items_positions['main_currency'][2]['position']
        self.orb_of_alteration = self.stash_items_positions['main_currency'][3]['position']
        self.orb_of_transmutation = self.stash_items_positions['main_currency'][1]['position']
       
        # Calculate item center
        item_block_center = [self.item_block[0] / 2, self.item_block[1] / 2]
        item_position = self.stash_items_positions['item_slot']['position']
        
        # Calculate currency center
        self.currency_block_center = [self.currency_block[0] / 2, self.currency_block[1] / 2]
        self.item_center = [item_position[0] + item_block_center[0], item_position[1] + item_block_center[1]]
        
        # Initialize controllers
        self.keyboard = KeyboardController()
        self.mouse = MouseController(self, mouse_speed) # mouse_speed
        self.mod_parser = ModParser()
        
        # Stop loop logic
        self.item_data = None
        self.selected_mods = []
        self.stop_loop = False
        self.mouse.check_stop_loop(self.stop_key)
        
        self.currency_names = {
            tuple(self.orb_of_scouring): "Orb of Scouring",
            tuple(self.orb_of_augmentation): "Orb of Augmentation",
            tuple(self.orb_of_alteration): "Orb of Alteration",
            tuple(self.orb_of_transmutation): "Orb of Transmutation",
        }

    @staticmethod
    def load_items_positions():
        with open("config/stash.json", "r") as file:
            return json.load(file)
    
    @staticmethod
    def load_options():
        try:
            with open("config/options.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: Options file not found. Using defaults.")
            return {}

    def check_item_mods(self):
        # Copy the item text
        item = self.keyboard.get_clipboard_data()
        if not item:
            return None
        
        item_mods = self.mod_parser.parse_mods(item)
        item_rarity = self.mod_parser.get_item_rarity(item)
        match_found = self.mod_parser.compare_mods(item_mods, self.selected_mods)
        
        return { "item": item, "mods": item_mods, "rarity": item_rarity, "match_found": match_found }

    def start_magic_craft(self, selected_mods):
        self.selected_mods = selected_mods
        self.stop_loop = False
        retry_count = 0
        
        # Start crafting loop
        self.mouse.move(self.item_center[0], self.item_center[1])
        
        self.item_data = self.check_item_mods()
        
        if not self.item_data:
            return False

        if self.item_data["rarity"] == "Normal":
                self.apply_currency(self.orb_of_transmutation, self.item_center)
                
        if self.item_data["rarity"] == "Rare":
            self.apply_currency(self.orb_of_scouring, self.item_center)
            self.apply_currency(self.orb_of_transmutation, self.item_center)
        
        while retry_count < self.max_retries and self.item_data and not self.stop_loop:
            [open_affix, affix] = self.mod_parser.get_open_affixes(self.item_data["item"])

            if self.item_data["match_found"]:
                break
            
            # Dacă există un affix liber, aplicăm Orb of Augmentation
            if open_affix:
                self.apply_currency(self.orb_of_augmentation, self.item_center)

                if self.item_data["match_found"]:
                    print('Crafting successful - mods match found.')
                    break

            # Dacă nu există affix liber, aplicăm Orb of Alteration și verificăm din nou
            else:
                self.apply_currency(self.orb_of_alteration, self.item_center)

            retry_count += 1
            print(f"Retrying crafting... ({retry_count}/{self.max_retries})")

        if self.item_data and self.item_data["match_found"]:
            print("Mods match! Crafting successful.")
            return True
        
        print("Max retries reached or no matching mods found.")
        return False

    # def check_functionality(self):
    #     item_clipboard_example = """
        
    #     Item Class: Jewels
    #     Rarity: Magic
    #     Flaming Cobalt Jewel of Atrophy
    #     --------
    #     Item Level: 84
    #     --------
    #     { Prefix Modifier "Flaming" (Tier: 1) — Damage, Elemental, Fire }
    #     16(14-16)% increased Fire Damage
    #     { Suffix Modifier "of Atrophy" (Tier: 1) — Damage, Chaos }
    #     +6(6-8)% to Chaos Damage over Time Multiplier
    #     --------
    #     Place into an allocated Jewel Socket on the Passive Skill Tree. Right click to remove from the Socket.
    #     Place into an allocated Jewel Socket on the Passive Skill Tree. Right click to remove from the Socket.

    #     """
    #     self.mouse.move(self.item_center[0], self.item_center[1])
    #     [open_affix, affix] = self.mod_parser.get_open_affixes(item_clipboard_example)
        
    def apply_currency(self, currency_position, item_position):
        if self.stop_loop:
            return
        
        currency_center = [currency_position[0] + self.currency_block_center[0], currency_position[1] + self.currency_block_center[1]]
        
        self.mouse.move(currency_center[0], currency_center[1])
        self.mouse.right_click()

        self.mouse.move(item_position[0], item_position[1])
        self.mouse.click()
        
        currency_name = self.currency_names.get(tuple(currency_position), "Unknown Currency")
        print(f"Applied {currency_name} to item at position {item_position}.")
        time.sleep(self.clipboard_copy_delay)  # Adjust the time if needed
        self.item_data = self.check_item_mods()
