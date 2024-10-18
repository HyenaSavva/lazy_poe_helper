import tkinter as tk
import pygetwindow as gw
from tkinter import ttk, messagebox
from controllers.file_manager import FileManager
from controllers.mod_parser import ModParser 
from controllers.craft_controllers.magic_craft_controller import MagicCraftController 

class MagicCraftTab(tk.PanedWindow):
    def __init__(self, parent):
        super().__init__(parent, orient="vertical")
        self.parent = parent

        self.prefix_count = 0
        self.suffix_count = 0

        # Initialize controllers
        self.magic_craft_controller = MagicCraftController()
        self.file_manager = FileManager()
        self.mod_parser = ModParser()

        # Variables and Data
        self.selected_mod_type = None
        self.mod_data = []

        # Create panes
        self.create_panes()
        self.load_mod_files()
        self.create_craft_button()
    
    def create_panes(self):
        """Create and add the panes."""
        self.pane_1 = ttk.Frame(self)
        self.add(self.pane_1)

        self.pane_2 = ttk.Frame(self)
        self.add(self.pane_2)

        # Create widgets in the panes
        self.create_mod_selection_section(self.pane_1)
        self.create_mod_table_section(self.pane_1, self.pane_2)
        
        # Set column widths after the UI is initialized
        self.after(500, self.set_column_widths)
        
    def create_mod_selection_section(self, parent):
        """Create mod selection combobox and search bar."""
        mod_type_frame = tk.Frame(parent)
        mod_type_frame.pack(anchor='w', padx=5, pady=5, fill='x')

        label = tk.Label(mod_type_frame, text="Mod Type", font=("Arial", 12))
        label.pack(side='left', padx=5, pady=5)

        # Mod file selection combobox
        self.mod_type_select = ttk.Combobox(mod_type_frame, state="readonly")
        self.mod_type_select.pack(side='right')
        self.mod_type_select.bind("<<ComboboxSelected>>", self.load_mods)

        # Search entry
        self.mod_search_var = tk.StringVar()
        self.mod_search_var.trace_add('write', self.filter_mods)
        search_entry = tk.Entry(parent, textvariable=self.mod_search_var)
        search_entry.pack(fill='x', padx=5, pady=5)
        
    def create_mod_table_section(self, pane_1, pane_2):
        """Create the table for mods and selected mods."""
        self.table_frame = ttk.Frame(pane_1)
        self.table_frame.pack(fill='both', expand=True)
        
        columns = ['Mod', 'Tag', 'iLvl', 'Weight']
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y", pady=5)

        # Mod tree view
        self.mod_tree = self.create_treeview(self.table_frame, columns, self.sort_mods_by_column, fill="both", expand=True)
        self.mod_tree.bind("<Double-1>", self.on_mod_double_click)

        # Selected mods tree view
        label = tk.Label(pane_2, text="Selected Mods", font=("Arial", 12))
        label.pack(anchor='w', padx=5, pady=5)
        self.selected_mod_tree = self.create_treeview(pane_2, columns, None, fill="both", expand=True)
        self.selected_mod_tree.bind("<Double-1>", self.remove_selected_mod)

    def create_treeview(self, parent, columns, sort_callback=None, **pack_options):
        """Create a reusable treeview."""
        tree = ttk.Treeview(parent, columns=columns, show='headings', yscrollcommand=self.scrollbar.set)
        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: sort_callback(c, tree) if sort_callback else None)
        tree.pack(pack_options)
        return tree

    def create_craft_button(self):
        """Create a button for starting the crafting process."""
        button_frame = ttk.Frame(self)
        button_frame.pack(side="bottom", fill="x", padx=5, pady=5)

        start_button = ttk.Button(button_frame, text="Start Craft", command=self.start_crafting)
        start_button.pack(side='left', padx=5, pady=5)

        check_functionality = ttk.Button(button_frame, text="Check Functionality", command=self.check_functionality)
        check_functionality.pack(side='left', padx=5, pady=5)
        
    def set_column_widths(self):
        """Set dynamic column widths based on treeview size."""
        mod_width = int(self.mod_tree.winfo_width() * 0.7)
        tag_width = int(self.mod_tree.winfo_width() * 0.15)
        remaining_width = int(self.mod_tree.winfo_width() * 0.15 / 2)
        
        # Set the column widths dynamically
        self.mod_tree.column('Mod', width=mod_width, stretch=False)
        self.mod_tree.column('Tag', width=tag_width, stretch=False)
        self.mod_tree.column('iLvl', width=remaining_width, stretch=False)
        self.mod_tree.column('Weight', width=remaining_width, stretch=False)

        self.selected_mod_tree.column('Mod', width=mod_width, stretch=False)
        self.selected_mod_tree.column('Tag', width=tag_width, stretch=False)
        self.selected_mod_tree.column('iLvl', width=remaining_width, stretch=False)
        self.selected_mod_tree.column('Weight', width=remaining_width, stretch=False)

    # Loaders and Updaters
    def load_mod_files(self):
        """Load mod file names into the combobox."""
        self.mod_files = self.file_manager.list_files()
        self.mod_type_select['values'] = self.mod_files
        self.mod_type_select.current(0)
        self.load_mods()

    def load_mods(self, event=None):
        """Load mods from the selected file."""
        try:
            selected_file = self.mod_type_select.get()
            self.selected_mod_type = 'prefix' if 'prefix' in selected_file.lower() else 'suffix' if 'suffix' in selected_file.lower() else None
            self.mod_data = self.file_manager.load_mods_from_file(selected_file)
            self.update_mod_tree(self.mod_data)
        except FileNotFoundError as e:
            messagebox.showerror("File Error", str(e))
            
    def update_mod_tree(self, mod_data):
        """Update the tree view with new mod data."""
        self.mod_tree.delete(*self.mod_tree.get_children())
        for mod in mod_data:
            self.mod_tree.insert('', tk.END, values=(mod['Mod'], mod['Tag'], mod['iLvl'], mod['Weight']))

    def filter_mods(self, *args):
        """Filter mods based on the search entry."""
        search_term = self.mod_search_var.get().lower()
        filtered_mods = [mod for mod in self.mod_data if search_term in mod['Mod'].lower() or search_term in mod['Tag'].lower()]
        self.update_mod_tree(filtered_mods)
            
    # Event Handlers
    def on_mod_double_click(self, event):
        """Handle mod selection on double-click."""
        selected_item = self.mod_tree.selection()
        if selected_item:
            mod_values = self.mod_tree.item(selected_item)['values']
            if not self.check_mod_limits(mod_values):
                return
            if self.check_duplicate_mod(mod_values):
                return
            self.selected_mod_tree.insert('', tk.END, values=mod_values)

    def remove_selected_mod(self, event):
        """Remove mod from selected mods."""
        selected_item = self.selected_mod_tree.selection()
        if selected_item:
            self.selected_mod_tree.delete(selected_item)

    def check_mod_limits(self, mod_values):
        """Check if mod limits are reached for prefixes or suffixes."""
        if self.selected_mod_type == 'prefix' and self.prefix_count >= 3:
            messagebox.showerror("Prefix Limit", "You can only have 3 prefixes.")
            return False
        elif self.selected_mod_type == 'suffix' and self.suffix_count >= 3:
            messagebox.showerror("Suffix Limit", "You can only have 3 suffixes.")
            return False
        return True

    def check_duplicate_mod(self, mod_values):
        """Check for duplicate mods in the selected mods list."""
        for item in self.selected_mod_tree.get_children():
            if self.selected_mod_tree.item(item)['values'] == mod_values:
                messagebox.showerror("Duplicate Mod", "This mod has already been added.")
                return True
        return False
    
    def sort_mods_by_column(self, column, treeview):
        """Sort mods by the selected column."""
        # Determine sort direction (toggle between ascending and descending)
        if hasattr(self, '_last_sort_column') and self._last_sort_column == column:
            self._sort_descending = not self._sort_descending
        else:
            self._sort_descending = False
        
        self._last_sort_column = column

        # Sort the mod data
        sorted_data = sorted(self.mod_data, 
                            key=lambda mod: mod[column].lower() if isinstance(mod[column], str) else mod[column],
                            reverse=self._sort_descending)

        # Clear and insert sorted mods
        treeview.delete(*treeview.get_children())
        for mod in sorted_data:
            treeview.insert('', tk.END, values=(mod['Mod'], mod['Tag'], mod['iLvl'], mod['Weight']))

    # Crafting Logic
    def get_item_mods(self):
        """Get selected mods from the tree view."""
        children = self.selected_mod_tree.get_children()
        return [self.selected_mod_tree.item(child)['values'][0] for child in children]
    
    def start_crafting(self):
        """Start the crafting process."""
        selected_mods = self.get_item_mods()
        if not selected_mods:
            messagebox.showerror("No Mods", "No mods selected for crafting.")
            return
        self.focus_poe_window()
        try:
            self.magic_craft_controller.start_magic_craft(selected_mods=selected_mods)
        except Exception as e:
            messagebox.showerror("Crafting Error", f"An error occurred during crafting: {str(e)}")
            
    def check_functionality(self):
        """Check functionality by focusing the window and testing the controller."""
        self.focus_poe_window()
        self.magic_craft_controller.check_functionality()

    def focus_poe_window(self):
        """Focus the Path of Exile window."""
        windows = gw.getWindowsWithTitle('Path of Exile')
        if windows:
            windows[0].activate()
