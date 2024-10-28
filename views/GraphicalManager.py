import tkinter as tk
from tkinter import ttk
from controller import MainController

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
        self.buttons = {
            "folder_music_button": self.create_button(toolbar, "Select Folder to Play", self.controller.music_player.load_multiple_music),
            "music_button": self.create_button(toolbar, "Select Music", self.controller.music_player.load_one_music),
            "pause_button": self.create_button(toolbar, "Pause", self.controller.music_player.pause_music, state=tk.DISABLED),
            "resume_button": self.create_button(toolbar, "Resume", self.controller.music_player.resume_music, state=tk.DISABLED),
            "next_button": self.create_button(toolbar, "Next", self.controller.music_player.play_next_music, state=tk.DISABLED),
            "previous_button": self.create_button(toolbar, "Previous", self.controller.music_player.play_previous_music, state=tk.DISABLED),
            "play_this_button": self.create_button(toolbar, "Play This Music", self.controller.music_player.play_this_music, state=tk.DISABLED)
        }

    def create_button(self, parent, text: str, command, state=tk.NORMAL):
        button = tk.Button(parent, text=text, command=command, state=state)
        button.pack(side=tk.LEFT, padx=5)
        return button

    def create_song_table(self):
        self.tree = ttk.Treeview(self.root, columns=("Title", "Path", "Enable"), show="headings", height=5)
        self.tree.heading("Title", text="Title", command=lambda: self.controller.sort_column("Title"))
        self.tree.heading("Path", text="Path", command=lambda: self.controller.sort_column("Path"))
        self.tree.heading("Enable", text="Enable", command=lambda: self.controller.sort_column("Enable"))

        self.tree.column("Title", width=150, stretch=True)
        self.tree.column("Path", width=300, stretch=True)
        self.tree.column("Enable", width=50, stretch=True)

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