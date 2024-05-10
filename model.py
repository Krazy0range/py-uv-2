import os
import mutagen

class Model:
    
    def __init__(self, mp3_folder):
        self.mp3_folder = mp3_folder
        
        self.mp3_files = self.get_mp3s()
        
        self.command = ''
        self.console = ''
        
        self.quit = False
        
        self.selected_song_index = -1

        self.queue = []
        self.queue_prev = []
        
        self.clear_queue_prev = False
        self.clear_queue_prev_len = 0
        self.clear_queue = False
        self.clear_queue_len = 0
        
        self.scroll = 0
        
        self.library_full_update = True
        self.queue_full_update = True
        self.console_full_update = True
        self.reset_screen = False
    
    def get_mp3s(self):
        files = []
        
        files = os.listdir(self.mp3_folder)
        
        def sorter(file):
            audio = mutagen.File(f'{self.mp3_folder}/{file}', easy=True)
            return f'{audio['artist']}{audio['album']}'
        
        files.sort(key=sorter)
        
        return files