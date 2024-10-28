import tkinter as tk
from typing import List

# Spécifie qu'on importe un énum
from models.Song import SongColumns
from views.GraphicalManager import GraphicalManager

class MainController:
    def __init__(self, root, music_player):
        self.root = root
        self.music_player = music_player
        self.sort_direction = {}
        self.last_sorted_column = None
        self.last_sort_reverse = False

        self.init_window()

        # Initialize GraphicalManager
        self.graphics = GraphicalManager(root, self)
        self.tree = self.graphics.get_tree()
        self.music_buttons = self.graphics.get_buttons()
        self.context_menu = self.graphics.get_context_menu()

        self.update_song_table()

    def init_window(self):
        self.root.title("Music Player")
        self.root.geometry("600x400")

    def bind_treeview_enable(self, event):
        column = self.tree.identify_column(event.x)
        if column == f"#{SongColumns.ENABLE.value}" and self.music_player.get_is_multi_music_played():
            item = self.tree.selection()[0]
            self.toggle_enable(item)

    def toggle_enable(self, item: str):
        song_index = self.tree.index(item)
        if song_index != self.music_player.get_current_song_index():
            song = self.music_player.get_mp3_files()[song_index]
            song.set_enable(not song.get_enable())
            self.tree.item(item, values=(song.get_title(), song.get_path(), song.get_enable()))
        
    def toggle_enable_contextual_menu(self):
        for item in self.tree.selection():
            self.toggle_enable(item)

    def update_song_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for song in self.music_player.get_mp3_files():
            self.tree.insert("", tk.END, values=(song.get_title(), song.get_path(), song.get_enable()))
        self.highlight_current_song()

    def set_button_state(self, buttons: List[tk.Button], state):
        for button in buttons:
            button.config(state=state)

    def update_buttons(self):
        if self.music_player.get_paused_state():
            self.set_button_state([self.music_buttons["pause_button"]], tk.DISABLED)
            self.set_button_state([self.music_buttons["resume_button"]], tk.NORMAL)
        else:
            self.set_button_state([self.music_buttons["pause_button"]], tk.NORMAL)
            self.set_button_state([self.music_buttons["resume_button"]], tk.DISABLED)
        if self.music_player.get_is_multi_music_played():
            self.set_button_state([self.music_buttons["next_button"], self.music_buttons["previous_button"], self.music_buttons["play_this_button"]], tk.NORMAL)
        else:
            self.set_button_state([self.music_buttons["next_button"], self.music_buttons["previous_button"], self.music_buttons["play_this_button"]], tk.DISABLED)

    def sort_column(self, col_name: str):
        reverse = self.sort_direction.get(col_name, False)
        if self.last_sorted_column == col_name and self.last_sort_reverse == reverse:
            return
        self.music_player.get_mp3_files().sort(
            key=lambda song: getattr(song, f"get_{col_name.lower()}")(),
            reverse=reverse
        )
        self.update_song_table()
        self.last_sorted_column = col_name
        self.last_sort_reverse = reverse
        self.sort_direction[col_name] = not reverse
        self.music_player.reset_current_song_index()

    def highlight_current_song(self):
        for item in self.tree.get_children():
            self.tree.item(item, tags=())
        current_index = self.music_player.get_current_song_index()
        if 0 <= current_index < len(self.tree.get_children()):
            current_item = self.tree.get_children()[current_index]
            self.tree.item(current_item, tags=("highlighted"))
            self.tree.see(current_item)
        self.tree.tag_configure("highlighted", background="lightgreen")

    def show_contextual_menu(self, event):
        try:
            if len(self.tree.get_children()) > 0 and len(self.tree.selection()) > 0:
                self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def select_all_items(self, event=None):
        for item in self.tree.get_children():
            self.tree.selection_add(item)
        return "break" #Empêche comportement par défaut du Ctrl+A

    def get_tree(self):
        return self.tree