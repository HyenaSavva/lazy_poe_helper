# lazy_poe_helper ✨⚒

**lazy_poe_helper** is a Python-based tool designed to simplify item parsing and mod filtering for Path of Exile (PoE). Whether you're analyzing item mods, searching for specific affixes, or checking for open prefixes/suffixes, this tool is here to save you time and effort! 📊💪

## Features 🛠✨
- **Item Parsing**: Extract item rarity, name, stack sizes, and mods with precision.
- **Mod Normalization**: Standardizes mod values (e.g., ranges like `1-3%` become `#%`).
- **Hybrid Mod Detection**: Handles multi-line hybrid mods as a single mod (e.g., "(3-5)% chance to Freeze, (12-16)% increased Freeze Duration").
- **Open Affix Detection**: Quickly identify open prefixes and suffixes based on item rarity.
- **Advanced Filtering**: Support for:
   - **AND** filtering: All selected mods must be present.
   - **COUNT** filtering: Match at least `n` mods from the selected list.

## Installation 🛠🌏
1. Ensure **Python 3.8+** is installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lazy_poe_helper.git
   cd lazy_poe_helper
   ```
3. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

## Usage 🛠
You can use the tool to parse and filter item mods by running the script and providing the item text.

### Example
Given the following **item text**:
```
Rarity: Rare
Icefang's Conqueror
Stack Size: 1/10
{ Prefix, Tier: 1 } Adds (12-16) to (20-25) Cold Damage to Attacks
{ Suffix, Tier: 2 } (3-5)% chance to Freeze, (12-16)% increased Freeze Duration on Enemies
```

#### Parsing Mods
```python
from lazy_poe_helper import ModParser

item_text = """Rarity: Rare
Icefang's Conqueror
Stack Size: 1/10
{ Prefix, Tier: 1 } Adds (12-16) to (20-25) Cold Damage to Attacks
{ Suffix, Tier: 2 } (3-5)% chance to Freeze, (12-16)% increased Freeze Duration on Enemies
"""

parser = ModParser()
parsed_mods = parser.parse_mods(item_text)
print(parsed_mods)
```
#### Filtering Mods
```python
selected_mods = [
    "Adds # to # Cold Damage to Attacks",
    "(3-5)% chance to Freeze, (12-16)% increased Freeze Duration"
]

is_match = parser.compare_mods(parsed_mods, selected_mods, filter_type="and")
print(is_match)  # True
```

#### Detecting Open Affixes
```python
has_open, absent_affixes = parser.get_open_affixes(item_text)
print(has_open)         # True
print(absent_affixes)   # ['prefix', 'suffix']
```

## Supported Filters 💡
1. **AND Filtering**: All selected mods must match an item's mods.
2. **COUNT Filtering**: Define a minimum number of mods to match:
   ```python
   is_match = parser.compare_mods(parsed_mods, selected_mods, filter_type="count", count=2)
   ```

## Why Use This? ⚡
- Saves you time manually checking mods.
- Handles complex mod scenarios (hybrids, tiers, affix types).
- Ideal for PoE players who want to automate item evaluation.

## Contributing 🤝
Contributions are welcome! Feel free to open issues or submit pull requests:
- **Report bugs**: Open an issue describing the problem.
- **Enhancements**: Suggest improvements or new features!

## License 🌐
This project is licensed under the **MIT License**.

---

Enjoy slaying monsters and trading smarter in Wraeclast! 🌟⚒

✨ *Stay lazy, automate everything!* 😴

