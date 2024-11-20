import gettext
from pathlib import Path
from utils.config import PROJECT_ROOT, DEFAULT_LANGUAGE

class Translate:
    def __init__(self, locale_dir: str, default_language: str = "en", domain: str = "app"):
        self.locale_dir = Path(locale_dir)
        self.default_language = default_language
        self.domain = domain
        self.translation = self.load_translation(default_language)
        self._ = self.translation.gettext

    def load_translation(self, language: str):
        return gettext.translation(
            self.domain,
            localedir=self.locale_dir,
            languages=[language],
            fallback=True
        )

    def set_language(self, language: str):
        self.translation = self.load_translation(language)
        self._ = self.translation.gettext
        DEFAULT_LANGUAGE = language

    def gettext(self, message: str):
        return self._(message)

translator = Translate(f"{PROJECT_ROOT}/locals", default_language=DEFAULT_LANGUAGE)
_ = translator.gettext  # Alias pratique pour les traductions
