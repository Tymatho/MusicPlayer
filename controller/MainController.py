import tkinter as tk
from typing import List

# Spécifie qu'on importe un énum
from models.Song import SongColumns
from views.GraphicalManager import GraphicalManager
from views.graphical_components.buttons import MediaPlayerButtons

class MainController:
    def __init__(self, root, music_player):
        self.root = root
        self.music_player = music_player
        self.sort_direction = {}
        self.last_sorted_column = None
        self.last_sort_reverse = False

        self.init_window()

        self.graphics = GraphicalManager(root, self)
        self.update_song_table()

    def init_window(self):
        self.root.title("Music Player")
        self.root.geometry("600x400")

    def update_song_table(self):
        for item in self.graphics.get_tree().get_children():
            self.graphics.get_tree().delete(item)
        for song in self.music_player.get_mp3_files():
            self.graphics.get_tree().insert("", tk.END, values=(song.get_title(), song.get_path(), song.get_enable()))
        self.highlight_current_song()

    def set_button_state(self, buttons: List[tk.Button], state):
        for button in buttons:
            button.config(state=state)

    def update_buttons(self):
        if self.music_player.get_paused_state():
            self.set_button_state([self.graphics.get_buttons()[MediaPlayerButtons.PAUSE_BUTTON.variable_name]], tk.DISABLED)
            self.set_button_state([self.graphics.get_buttons()[MediaPlayerButtons.RESUME_BUTTON.variable_name]], tk.NORMAL)
        else:
            self.set_button_state([self.graphics.get_buttons()[MediaPlayerButtons.PAUSE_BUTTON.variable_name]], tk.NORMAL)
            self.set_button_state([self.graphics.get_buttons()[MediaPlayerButtons.RESUME_BUTTON.variable_name]], tk.DISABLED)
        if self.music_player.get_is_multi_music_played():
            self.set_button_state(
                [self.graphics.get_buttons()[MediaPlayerButtons.NEXT_BUTTON.variable_name],
                 self.graphics.get_buttons()[MediaPlayerButtons.PREVIOUS_BUTTON.variable_name],
                 self.graphics.get_buttons()[MediaPlayerButtons.PLAY_THIS_MUSIC_BUTTON.variable_name]]
                , tk.NORMAL)
        else:
            self.set_button_state(
                [self.graphics.get_buttons()[MediaPlayerButtons.NEXT_BUTTON.variable_name], 
                self.graphics.get_buttons()[MediaPlayerButtons.PREVIOUS_BUTTON.variable_name], 
                self.graphics.get_buttons()[MediaPlayerButtons.PLAY_THIS_MUSIC_BUTTON.variable_name]]
                , tk.DISABLED)

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
        for item in self.graphics.get_tree().get_children():
            self.graphics.get_tree().item(item, tags=())
        current_index = self.music_player.get_current_song_index()
        if 0 <= current_index < len(self.graphics.get_tree().get_children()):
            current_item = self.graphics.get_tree().get_children()[current_index]
            self.graphics.get_tree().item(current_item, tags=("highlighted"))
            self.graphics.get_tree().see(current_item)
        self.graphics.get_tree().tag_configure("highlighted", background="lightgreen")
    
    def toggle_enable(self, item: str):
        song_index = self.graphics.get_tree().index(item)
        if song_index != self.music_player.get_current_song_index():
            song = self.music_player.get_mp3_files()[song_index]
            song.set_enable(not song.get_enable())
            self.graphics.get_tree().item(item, values=(song.get_title(), song.get_path(), song.get_enable()))
        
    def toggle_enable_contextual_menu(self):
        for item in self.graphics.get_tree().selection():
            self.toggle_enable(item)
        
    def show_contextual_menu(self, event):
        try:
            if len(self.graphics.get_tree().get_children()) > 0 and len(self.graphics.get_tree().selection()) > 0:
                self.graphics.get_context_menu().tk_popup(event.x_root, event.y_root)
        finally:
            self.graphics.get_context_menu().grab_release()

    def select_all_items(self, event=None):
        for item in self.graphics.get_tree().get_children():
            self.graphics.get_tree().selection_add(item)
        return "break" #Empêche comportement par défaut du Ctrl+A
    
    def bind_treeview_enable(self, event):
        column = self.graphics.get_tree().identify_column(event.x)
        if column == f"#{SongColumns.ENABLE.id}" and self.music_player.get_is_multi_music_played():
            item = self.graphics.get_tree().selection()[0]
            self.toggle_enable(item)

    def get_tree(self):
        return self.graphics.get_tree()