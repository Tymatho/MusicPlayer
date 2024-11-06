import tkinter as tk
from tkinter import ttk
from controller import MainController
from models.Song import SongColumns
from .graphical_components.buttons import MediaPlayerButtons

class GraphicalManager:
    def __init__(self, root, controller: MainController):
        self.root = root
        self.init_window()
        self.controller = controller
        self.style = ttk.Style(root)
        self.style.theme_use("clam")
        self.create_buttons()
        self.create_song_table()
        self.create_contextual_menu()
        self.create_statements()
    
    def init_window(self):
        self.root.title("Music Player")
        self.root.geometry("800x400")

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
        frame = ttk.Frame(self.root)
        frame.pack(pady=20, fill=tk.BOTH, expand=True)
        song_columns=[]
        for column in SongColumns:
            song_columns.append(column.name)
        self.tree = ttk.Treeview(frame, columns=song_columns, show="headings", height=5)
        for column in SongColumns:
            #command=lambda name=column.name -> store the value to apply it to EACH iteration and not with the last value of the iteration
            self.tree.heading(column.name, text=column.name, command=lambda name=column.name: self.controller.sort_column(name))
            self.tree.column(column.name, width=column.width, stretch=column.width)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Control-a>", self.controller.select_all_items)
        self.tree.bind("<Double-1>", self.controller.bind_treeview_enable)
        self.tree.bind("<Button-3>", self.controller.show_contextual_menu)

    def create_contextual_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Toggle Enable", command=self.controller.toggle_enable_contextual_menu)
    
    def create_statements(self):
        self.bottom_toolbar = tk.Frame(self.root)
        self.bottom_toolbar.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.statements_label = {}
        
        volume_label = tk.Label(self.root, text=f"Volume: {self.controller.music_player.get_volume() * 100}%", font=("Helvetica", 12))
        volume_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        
        current_song_label = tk.Label(self.root, text=f"Song: 0/0", font=("Helvetica", 12))
        current_song_label.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)
        
        self.statements_label["volume_label"] = volume_label
        self.statements_label["current_song_label"] = current_song_label

    def get_tree(self):
        return self.tree

    def get_buttons(self):
        return self.buttons

    def get_context_menu(self):
        return self.context_menu