from enum import Enum

GENERAL_FONT=("Helvetica", 12)

class MediaPlayerLabels(Enum):
    CURRENT_SONG_LABEL = ("current_song_label", f"Song: 0/0", GENERAL_FONT)
    VOLUME_LABEL = ("volume_label", f"Volume: 50%", GENERAL_FONT)
    
    @property
    def variable_name(self):
        return self.value[0]

    @property
    def default_text(self):
        return self.value[1]
    
    @property
    def font(self):
        return self.value[2]