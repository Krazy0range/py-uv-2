import os
from random import shuffle
import mutagen

class Model:
    
    def __init__(self, mp3_folder):
        self.mp3_folder = mp3_folder
        
        self.mp3_files = self.get_mp3s('filename')
        
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
    
    def load_mp3s(self, sort):
        self.mp3_files = self.get_mp3s(sort)
    
    def get_mp3s(self, sort):
        files = []
        
        files = os.listdir(self.mp3_folder)
        
        if sort == 'random':
            shuffle(files)
            return files
        
        def sorter(file):
            audio = mutagen.File(f'{self.mp3_folder}/{file}', easy=True)
            if sort == 'filename':
                return file
            elif sort == 'artist+album':
                return f'{audio['artist']}{audio['album']}'
            elif sort == 'duration':
                return audio.info.length
        
        files.sort(key=sorter)
        
        return files