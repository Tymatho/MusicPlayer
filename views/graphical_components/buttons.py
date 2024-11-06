from enum import Enum
import tkinter as tk

class MediaPlayerButtons(Enum):
    FOLDER_MUSIC_BUTTON = ("folder_music_button", "Select Folder to Play", "load_multiple_music", tk.NORMAL)
    FILE_MUSIC_BUTTON = ("file_music_button", "Select Music File", "load_one_music", tk.NORMAL)
    PAUSE_BUTTON = ("pause_button", "Pause", "pause_music", tk.DISABLED)
    RESUME_BUTTON = ("resume_button", "Resume", "resume_music", tk.DISABLED)
    NEXT_BUTTON = ("next_button", "Next", "play_next_music", tk.DISABLED)
    PREVIOUS_BUTTON = ("previous_button", "Previous", "play_previous_music", tk.DISABLED)
    PLAY_THIS_MUSIC_BUTTON = ("play_this_button", "Play This Music", "play_this_music", tk.DISABLED)
    INCREASE_VOLUME_BUTTON = ("increase_button", "Increase Volume", "update_volume", 0.1, tk.NORMAL)
    DECREASE_VOLUME_BUTTON = ("decrease_button", "Decrease Volume", "update_volume", -0.1, tk.NORMAL)
    
    @property
    def variable_name(self):
        return self.value[0]

    @property
    def title(self):
        return self.value[1]
    
    def command(self, music_player):
        # Return the associated method. Example: music.player.load_multiple_music()
        if len(self.value) > 4:
            return lambda: getattr(music_player, self.value[2])(self.value[3])
        else:
            return lambda: getattr(music_player, self.value[2])()
    
    @property
    def is_enable(self):
        return self.value[-1]