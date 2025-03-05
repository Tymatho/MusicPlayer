from enum import Enum
from utils.translator import _

GENERAL_FONT=("Helvetica", 12)

class MediaPlayerLabels(Enum):
    CURRENT_SONG_LABEL = ("current_song_label", _("Song: {current}/{total}"), GENERAL_FONT)
    VOLUME_LABEL = ("volume_label", _("Volume: {volume}%"), GENERAL_FONT)
    CURRENT_SONG_TIME = ("current_song_time", _("{current_time} / {total_time}"), GENERAL_FONT)
    
    @property
    def variable_name(self):
        return self.value[0]

    @property
    def text(self):
        return self.value[1]
    
    @property
    def font(self):
        return self.value[2]