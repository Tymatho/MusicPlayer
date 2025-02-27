from watchdog.events import FileSystemEventHandler
from models import MusicPlayer

class DirectoryListener(FileSystemEventHandler):
    
    def __init__(self, music_player: MusicPlayer):
        super().__init__()
        self.music_player = music_player
    
    def on_created(self, event):
        if not event.is_directory:  # Check if it's not a directory
            print(f"File created: {event.src_path}")
            self.music_player.add_song_with_file_path(event.src_path)
            

    def on_deleted(self, event):
        if not event.is_directory:  # Check if it's not a directory
            print(f"File deleted: {event.src_path}")
            self.music_player.remove_song_with_file_path(event.src_path)