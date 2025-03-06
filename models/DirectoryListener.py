from watchdog.events import FileSystemEventHandler
from models import MusicPlayer

class DirectoryListener(FileSystemEventHandler):
    
    def __init__(self, music_player: MusicPlayer):
        super().__init__()
        self.music_player = music_player
    
    def on_created(self, event):
        if self.__check_if_file_is_music(event):
            self.music_player.add_song_with_file_path(event.src_path)
            

    def on_deleted(self, event):
        if self.__check_if_file_is_music(event):
            self.music_player.remove_song_with_file_path(event.src_path)
            
    def on_moved(self, event):
        if self.__check_if_file_is_music(event):
            self.music_player.get_controller().update_song_table()
            
    #private method
    def __check_if_file_is_music(self, event):
        return (not event.is_directory) and (event.src_path.endswith("mp3"))