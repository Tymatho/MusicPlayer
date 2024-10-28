from models.MusicPlayer import MusicPlayer
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()