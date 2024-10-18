import re

class ModParser:
    def parse_item_details(self, item_text):
        """
        Extracts item rarity, name, and stack size from the item text.
        """
        rarity_match = re.search(r"Rarity: (.+)", item_text)
        name_match = re.search(r"Rarity: .+\n(.+)", item_text)
        stack_size_match = re.search(r"Stack Size: (\d+)/(\d+)", item_text)

        rarity = rarity_match.group(1) if rarity_match else None
        name = name_match.group(1) if name_match else None
        current_stack = int(stack_size_match.group(1)) if stack_size_match else None
        max_stack = int(stack_size_match.group(2)) if stack_size_match else None

        return {
            "rarity": rarity,
            "name": name,
            "current_stack": current_stack,
            "max_stack": max_stack
        }

    def normalize_mod(self, mod):
        """
        Normalizes mod descriptions by replacing value ranges and standardizing format.
        """
        mod = re.sub(r'\(?\d+-?\d*\)?%', '#%', mod)
        mod = re.sub(r'\+\(?\d+-?\d*\)?', '#', mod)
        return mod

    def extract_general_mod(self, mod_text):
        """
        Extracts a general version of the mod text by removing specific values.
        """
        # Remove any number ranges and specific values to create a general mod description
        general_mod = re.sub(r'\(?\d+-?\d*\)?%', '#%', mod_text)
        general_mod = re.sub(r'\(?\d+-?\d*\)?', '#', general_mod)
        return general_mod
    
    def get_item_rarity(self, item_text):
        """
        Returns the item rarity based on the parsed text.
        """
        rarity = re.search(r"Rarity: (.+)", item_text).group(1).strip()
        return rarity

    def get_open_affixes(self, item_text):
        """
        Returns bool if item has open affix and absent affixes based on the item text.
        """
        item_rarity = self.get_item_rarity(item_text)
        item_mods = self.parse_mods(item_text)

        # Count the prefixes and suffixes
        prefix_count = len([mod for mod in item_mods if mod["type"] == "prefix"])
        suffix_count = len([mod for mod in item_mods if mod["type"] == "suffix"])
        
        absent_affixes = []

        # Check based on rarity
        if item_rarity == "Magic":
            has_open_affix = prefix_count < 1 or suffix_count < 1
            if prefix_count < 1:
                absent_affixes.append("prefix")
            if suffix_count < 1:
                absent_affixes.append("suffix")
        elif item_rarity == "Rare":
            has_open_affix = prefix_count < 3 or suffix_count < 3
            if prefix_count < 3:
                absent_affixes.append("prefix")
            if suffix_count < 3:
                absent_affixes.append("suffix")
        else:
            has_open_affix = False
            
        print(f"Prefixes: {prefix_count}, Suffixes: {suffix_count}")
            
        return has_open_affix, absent_affixes
    
    def get_mod_tier(self, item_mods, mod_name):
        """
        Returns the tier of a specific mod from the item mods.
        """
        for mod in item_mods:
            if mod["mod"] == mod_name:
                return mod["tier"]
        return None
    
    def parse_mods(self, item_text):
        """
        Extracts and normalizes mods from the item text, including detailed information.
        """
        detailed_mods = []
        mod_matches = re.findall(r"{ (.+?) }\n(.+)", item_text)

        for mod in mod_matches:
            mod_data = {}

            # Determine if it's a prefix or suffix
            modifier_type = "prefix" if "Prefix" in mod[0] else "suffix"
            
            # Extract tier, tags, and value ranges if available
            tier_match = re.search(r"Tier: (\d+)", mod[0])
            tag_match = re.search(r"— (.+)", mod[0])
            range_match = re.search(r"(\d+)-(\d+)", mod[1])

            # Normalize the mod text and generalize it
            normalized_mod = self.normalize_mod(mod[1])
            general_mod = self.extract_general_mod(mod[1])

            mod_data["type"] = modifier_type
            mod_data["tier"] = int(tier_match.group(1)) if tier_match else None
            mod_data["tags"] = tag_match.group(1).split(", ") if tag_match else []
            mod_data["mod_value"] = normalized_mod
            mod_data["mod"] = general_mod  # This is the general form of the mod
            if range_match:
                mod_data["range"] = (int(range_match.group(1)), int(range_match.group(2)))

            detailed_mods.append(mod_data)

        return detailed_mods

    def compare_mods(self, item_mods, selected_mods):
        """
        Compares item mods with selected mods. Assumes selected_mods are in a cleaned, standardized format.
        """
        item_mods = [self.normalize_mod(mod["mod_value"]) for mod in item_mods]  # Use normalized mod_value for comparison
        cleaned_selected_mods = [self.normalize_mod(mod) for mod in selected_mods]

        for selected_mod in cleaned_selected_mods:
            if not any(selected_mod in mod for mod in item_mods):
                return False
        return True
