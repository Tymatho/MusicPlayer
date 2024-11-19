import tkinter as tk
from tkinter import ttk
from controller import MainController
from models.Song import SongColumns
from controller.binds import AppBinds
from .graphical_components.buttons import MediaPlayerButtons
from .graphical_components.labels import MediaPlayerLabels

class GraphicalManager:
    def __init__(self, root, controller: MainController):
        self.root = root
        self.init_window()
        self.controller = controller
        root.set_theme("black")
        self.create_buttons()
        self.create_song_table()
        self.create_contextual_menu()
        self.create_statements()
    
    def init_window(self):
        self.root.title("Music Player")
        self.root.geometry("800x400")
        try:
            self.root.iconbitmap("./music_player.ico")
        except Exception:
            pass

    def create_buttons(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.buttons = {button.variable_name: self.create_button(toolbar, button.title, button.command(self.controller.music_player), button.is_enable) 
                for button in MediaPlayerButtons}

    def create_button(self, parent, text: str, command, state=tk.NORMAL):
        button = tk.Button(parent, text=text, command=command, state=state)
        button.pack(side=tk.LEFT, padx=5)
        return button

    def create_song_table(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=20, fill=tk.BOTH, expand=True)
        song_columns=[column.name for column in SongColumns]
        self.tree = ttk.Treeview(frame, columns=song_columns, show="headings", height=5)
        for column in SongColumns:
            #command=lambda name=column.name -> store the value to apply it to EACH iteration and not with the last value of the iteration
            self.tree.heading(column.name, text=column.name, command=lambda name=column.name: self.controller.sort_column(name))
            self.tree.column(column.name, width=column.width, stretch=column.width)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for binding in AppBinds:
            match binding.parent:
                case "treeview":
                    self.tree.bind(binding.control, binding.command(self.controller))
                case "root":
                    self.root.bind(binding.control, binding.command(self.controller))
        
    def create_contextual_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Toggle Enable", command=self.controller.toggle_enable_contextual_menu)
    
    def create_statements(self):
        self.bottom_toolbar = tk.Frame(self.root)
        self.bottom_toolbar.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.statements_label = {label.variable_name: self.create_label(self.root, label.default_text, label.font) for label in MediaPlayerLabels}
        self.statements_label[MediaPlayerLabels.VOLUME_LABEL.variable_name].place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        self.statements_label[MediaPlayerLabels.CURRENT_SONG_LABEL.variable_name].place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

    def create_label(self, parent, text, font):
        label = tk.Label(parent, text=text, font=font)
        label.pack(side=tk.LEFT, padx=5)
        return label

    def update_window_title(self, song_title: str):
        self.root.title(f"Music Player - {song_title}")

    def get_tree(self): return self.tree

    def get_buttons(self): return self.buttons

    def get_context_menu(self): return self.context_menu