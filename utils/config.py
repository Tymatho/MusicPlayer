import os
from enum import Enum
import platform
import locale

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Languages (Enum):
    SPANISH = "es"
    ENGLISH = "en"
    FRENCH = "fr"
    
current_locale = locale.getdefaultlocale()[0]
DEFAULT_LANGUAGE = current_locale.split('_')[0]

CURRENT_PLATFORM = platform.system()