import os
import time
import threading

from watchdog.observers import Observer
#Spécifie qu'on importe une classe
from models.Song import Song
from controller.MainController import MainController
#Spécifie qu'on importe un module
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
from models.DirectoryListener import DirectoryListener

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        mixer.init()
        mixer.music.set_volume(0.5)

        self.current_folder = None
        self.current_song_index = -1
        self.mp3_files = []
        #store only the song name. Example : "XXXX.mp3"
        self.music_files_set = set()
        self.paused = False
        
        self.main_controller = MainController(root, self)
        self.main_controller.update_statements_label()
        self.main_controller.update_current_song_time()
        
        self.event_handler = DirectoryListener(self)
        self.observer = Observer()
               
        self.root.after(500, self.check_music_end)

    def fill_music_folders(self):
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
                            song = Song(full_path, file, MP3(full_path).info.length)
                            self.add_song(song)
                except PermissionError:
                    continue
            self.main_controller.update_song_table()
        
    def fill_music_folder(self):
        if self.current_folder:
            for file in os.listdir(self.current_folder):
                full_path = os.path.join(self.current_folder, file)
                if file.endswith(".mp3"):
                    song = Song(full_path, file, MP3(full_path).info.length)
                    self.add_song(song)
            self.observer.schedule(self.event_handler, self.current_folder, recursive=False)  # Set recursive=True to watch subdirectories
            self.observer.start()
            self.main_controller.update_song_table()

    def load_music(self, song: Song):
        mixer.music.load(song.get_path())
        self.main_controller.graphics.update_window_title(song.get_title())

    def load_multiple_music(self):
        self.current_folder = filedialog.askdirectory()
        if self.current_folder:
            self.fill_music_folder()
            self.reset_current_song_index()
            self.play_music()

    def load_one_music(self):
        temp_song = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3")])
        if temp_song:
            self.music_files_set.clear()
            self.mp3_files = [Song(temp_song, os.path.basename(temp_song), MP3(temp_song).info.length, True)]
            self.reset_current_song_index()
            self.music_files_set.add(os.path.basename(temp_song))
            self.main_controller.update_song_table()
            self.play_music()

    def play_music(self):
        if self.mp3_files and 0 <= self.current_song_index < len(self.mp3_files):
            self.load_music(self.mp3_files[self.current_song_index])
            mixer.music.play()
            self.set_paused_state(False)
            self.main_controller.update_buttons()
            self.main_controller.highlight_current_song()
            self.main_controller.update_statements_label()
        
    def get_valid_song_index(self, index, step):
        if len(self.mp3_files) == 0:
            return -1
        new_index = (index + step) % len(self.mp3_files) #use of modulo to be in cycle of the len of the array
        while not self.mp3_files[new_index].get_enable():
            new_index = (new_index + step) % len(self.mp3_files)
            if new_index == index:
                break
        return new_index

    def play_next_music(self):
        if self.mp3_files:
            self.current_song_index = self.get_valid_song_index(self.current_song_index, 1)
            self.play_music()

    def play_previous_music(self):
        if self.mp3_files:
            self.current_song_index = self.get_valid_song_index(self.current_song_index, -1)
            self.play_music()

    def pause_music(self):
        if self.mp3_files and not self.paused:
            mixer.music.pause()
            self.set_paused_state(True)
            self.main_controller.update_buttons()

    def resume_music(self):
        if self.mp3_files and self.paused:
            mixer.music.unpause()
            self.set_paused_state(False)
            self.main_controller.update_buttons()

    def play_this_music(self):
        selected_item = self.main_controller.get_tree().selection()
        if selected_item:
            tree_index = self.main_controller.get_tree().index(selected_item[0])
            if self.current_song_index != tree_index:
                self.current_song_index = tree_index
                self.play_music()
                
    def update_volume(self, volume: float):
        if self.mp3_files:
            new_volume = round(max(0.0, min(1.0, mixer.music.get_volume() + volume)), 1) #get safe value for volume
            mixer.music.set_volume(new_volume)
            self.main_controller.update_statements_label()
            self.main_controller.update_buttons()
    
    def check_music_end(self):
        if self.mp3_files:
            if mixer.music.get_busy() and not self.paused:
                self.main_controller.update_current_song_time(mixer.music.get_pos() / 1000, self.get_mp3_files()[self.get_current_song_index()].get_duration())
            if not mixer.music.get_busy() and not self.paused:
                self.play_next_music()
        self.root.after(500, self.check_music_end)
        
    def add_song(self, song: Song) :
        if song.get_path() not in self.music_files_set:
            self.mp3_files.append(song)
            self.music_files_set.add(song.get_path())
            
    def add_song_with_file_path(self, song_path: str) :
        if song_path not in self.music_files_set and song_path.endswith("mp3"):
            time.sleep(0.5)   #File previously created so wait for the previous process to release the song
            song = Song(song_path, os.path.basename(song_path), MP3(song_path).info.length, True)
            self.mp3_files.append(song)
            self.music_files_set.add(song.get_path())
            self.main_controller.update_song_table()
            
    def remove_song(self, song: Song):
        if song.get_path() in self.music_files_set:
            self.mp3_files.remove(song)
            self.music_files_set.remove(song.get_path())
            
    def remove_song_with_file_path(self, song_path: str):
        if song_path in self.music_files_set:
            song_to_remove = next((song for song in self.mp3_files if song.path == song_path), None)
            self.mp3_files.remove(song_to_remove)
            self.music_files_set.remove(song_to_remove.get_path())
            self.main_controller.update_song_table()

    def set_paused_state(self, new_state: bool): self.paused = new_state
        
    def get_mp3_files(self): return self.mp3_files
    
    def get_paused_state(self): return self.paused
    
    def get_is_multi_music_played(self): return self.mp3_files and len(self.mp3_files) > 1
    
    def reset_current_song_index(self): self.current_song_index = 0
        
    def get_current_song_index(self): return self.current_song_index
    
    def get_volume(self): return mixer.music.get_volume()
    
    def get_controller(self): return self.main_controller