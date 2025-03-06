from enum import Enum
from utils.translator import _

class Song:
    def __init__(self, path: str, title: str, duration: float, enable: bool = True):
        self.path = path
        self.title = title
        self.duration = duration
        self.enable = enable

    def get_path(self): return self.path

    def get_title(self): return self.title
    
    def get_duration(self): return self.duration

    def get_enable(self): return self.enable

    def set_enable(self, enable): self.enable = enable
    
class SongColumns(Enum):
    TITLE = (1,"Title", _("Title"), 150, True)
    PATH = (2, "Path", _("Path"), 500, True)
    DURATION = (3,"Duration", _("Duration"), 30, True)
    ENABLE = (4, "Enable", _("Enable"), 30, True)

    @property
    def id(self):
        return self.value[0]
    
    @property
    def name(self):
        return self.value[1]

    @property
    def text(self):
        return self.value[2]
    
    @property
    def width(self):
        return self.value[3]
    
    @property
    def stretch(self):
        return self.value[4]