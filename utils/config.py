import os
from enum import Enum
import platform
import locale

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Languages (Enum):
    SPANISH = ("es", "Español")
    ENGLISH = ("en", "English")
    FRENCH = ("fr", "Français")
    
    @property
    def language_code(self):
        return self.value[0]
    
    @property
    def language_name(self):
        return self.value[1]
    
current_locale = locale.getdefaultlocale()[0]
DEFAULT_LANGUAGE = current_locale.split('_')[0]

# retrieve language name with language code
# next(langue.language_name for langue in Languages if langue.language_code == DEFAULT_LANGUAGE)

CURRENT_PLATFORM = platform.system()

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 500

GENERAL_FONT=("Helvetica", 12)