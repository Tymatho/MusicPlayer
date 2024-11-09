from models.MusicPlayer import MusicPlayer
from ttkthemes import ThemedTk

if __name__ == "__main__":
    root = ThemedTk()
    app = MusicPlayer(root)
    root.mainloop()