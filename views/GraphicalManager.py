import tkinter as tk
from tkinter import ttk
from controller import MainController
from models.Song import SongColumns
from .graphical_components.buttons import MediaPlayerButtons

class GraphicalManager:
    def __init__(self, root, controller: MainController):
        self.root = root
        self.controller = controller
        self.style = ttk.Style(root)
        self.style.theme_use("clam")
        self.create_buttons()
        self.create_song_table()
        self.create_contextual_menu()

    def create_buttons(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.buttons = {}
        for button in MediaPlayerButtons:
            self.buttons[button.variable_name] = self.create_button(toolbar, button.title, button.command(self.controller.music_player), button.is_enable)
        
    def create_button(self, parent, text: str, command, state=tk.NORMAL):
        button = tk.Button(parent, text=text, command=command, state=state)
        button.pack(side=tk.LEFT, padx=5)
        return button

    def create_song_table(self):
        self.tree = ttk.Treeview(self.root, columns=(SongColumns.TITLE.name, SongColumns.PATH.name, SongColumns.ENABLE.name), show="headings", height=5)
        for column in SongColumns:
            self.tree.heading(column.name, text=column.name, command=lambda: self.controller.sort_column(column.name))
            self.tree.column(column.name, width=column.width, stretch=column.width)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Control-a>", self.controller.select_all_items)
        self.tree.bind("<Double-1>", self.controller.bind_treeview_enable)
        self.tree.bind("<Button-3>", self.controller.show_contextual_menu)

    def create_contextual_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Toggle Enable", command=self.controller.toggle_enable_contextual_menu)

    def get_tree(self):
        return self.tree

    def get_buttons(self):
        return self.buttons

    def get_context_menu(self):
        return self.context_menu