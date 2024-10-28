class Song:
    def __init__(self, path, title, enable=True):
        self.path = path
        self.title = title
        self.enable = enable

    def get_path(self): return self.path

    def get_title(self): return self.title

    def get_enable(self): return self.enable

    def set_enable(self, enable): self.enable = enable