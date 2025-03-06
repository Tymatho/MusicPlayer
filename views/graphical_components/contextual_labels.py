from enum import Enum
from utils.translator import _
from utils.config import GENERAL_FONT

class MediaPlayerContextualLabels(Enum):
    TOGGLE_ENABLE = ("toggle_enable", _("Toggle Enable"), GENERAL_FONT, "toggle_enable_contextual_menu")
    
    @property
    def variable_name(self):
        return self.value[0]

    @property
    def text(self):
        return self.value[1]
    
    @property
    def font(self):
        return self.value[2]
    
    def command(self, controller):
        return lambda: getattr(controller, self.value[3])()