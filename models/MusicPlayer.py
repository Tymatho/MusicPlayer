import tkinter as tk
import os
#Spécifie qu'on importe une classe
from models.Song import Song
from controller.MainController import MainController
#Spécifie qu'on importe un module
from tkinter import filedialog
from pygame import mixer

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        mixer.init()

        self.current_folder = None
        self.current_song_index = -1
        self.mp3_files = []
        #set est un tableau qui ne permet pas les doublons
        self.music_files_set = set()
        self.is_multi_music_played = False
        self.paused = False
        
        self.main_view = MainController(root, self)
        self.root.after(500, self.check_music_end)

    def fill_music_folder(self):
        if self.current_folder:
            stack = [self.current_folder]
            #tant que la pile n'est pas vide alors on continue de boucler dessus
            while stack:
                current_folder = stack.pop()
                try:
                    for file in os.listdir(current_folder):
                        full_path = os.path.join(current_folder, file)
                        if os.path.isdir(full_path):
                            stack.append(full_path)
                        elif file.endswith(".mp3"):
                            if file not in self.music_files_set:
                                self.mp3_files.append(Song(full_path, file))
                                self.music_files_set.add(file)
                except PermissionError:
                    continue
            self.main_view.update_song_table()

    def load_music(self, song: Song):
        mixer.music.load(song.get_path())
        self.root.title(f"Music Player - {song.get_title()}")

    def load_multiple_music(self):
        self.music_files_set.clear()
        self.current_folder = filedialog.askdirectory()
        if self.current_folder:
            self.fill_music_folder()
            self.is_multi_music_played = True
            self.reset_current_song_index()
            self.play_music()

    def load_one_music(self):
        self.music_files_set.clear()
        temp_song = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3 *.wav")])
        if temp_song:
            self.mp3_files = [Song(temp_song, os.path.basename(temp_song), True)]
            self.reset_current_song_index()
            self.is_multi_music_played = False
            self.main_view.update_song_table()
            self.play_music()

    def play_music(self):
        if self.mp3_files and 0 <= self.current_song_index < len(self.mp3_files):
            self.load_music(self.mp3_files[self.current_song_index])
            mixer.music.play()
            self.set_paused_state(False)
            self.main_view.update_buttons()
            self.main_view.highlight_current_song()

    def play_next_music(self):
        if not self.mp3_files:
            return
        self.current_song_index = (self.current_song_index + 1) % len(self.mp3_files)
        while not self.mp3_files[self.current_song_index].get_enable():
            self.current_song_index = (self.current_song_index + 1) % len(self.mp3_files)
            if self.current_song_index == 0:
                break
        self.play_music()

    def play_previous_music(self):
        if not self.mp3_files:
            return
        self.current_song_index = (self.current_song_index - 1) % len(self.mp3_files)
        while not self.mp3_files[self.current_song_index].get_enable():
            self.current_song_index = (self.current_song_index - 1) % len(self.mp3_files)
            if self.current_song_index == len(self.mp3_files) - 1:
                break
        self.play_music()

    def pause_music(self):
        mixer.music.pause()
        self.set_paused_state(True)
        self.main_view.update_buttons()

    def resume_music(self):
        mixer.music.unpause()
        self.set_paused_state(False)
        self.main_view.update_buttons()

    def play_this_music(self):
        selected_item = self.main_view.get_tree().selection()
        if selected_item:
            song_index = self.main_view.get_tree().index(selected_item[0])
            if self.current_song_index != song_index:
                self.current_song_index = song_index
                self.play_music()
    
    def check_music_end(self):
        if self.mp3_files:
            if not mixer.music.get_busy() and not self.paused:
                self.play_next_music()
        self.root.after(500, self.check_music_end)

    def set_paused_state(self, new_state: bool): self.paused = new_state
        
    def get_mp3_files(self): return self.mp3_files
    
    def is_paused(self): return self.paused
    
    def is_multi_music_played(self): return self.is_multi_music_played
    
    def reset_current_song_index(self): self.current_song_index = 0
        
    def get_current_song_index(self): return self.current_song_index