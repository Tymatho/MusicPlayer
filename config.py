import os
from enum import Enum

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class Languages (Enum):
    SPANISH = "es"
    ENGLISH = "en"
    FRENCH = "fr"
    
DEFAULT_LANGUAGE = Languages.FRENCH.value