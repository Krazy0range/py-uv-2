import os
from random import shuffle
import mutagen
import json

class Model:
    
    def __init__(self, mp3_folder):
        self.mp3_folder = mp3_folder
        
        self.mp3_files = self.get_mp3s_raw()
        
        self.index_file = "index.json"
        self.index = self.load_index()
        self.refresh_index()
        
        self.showing_explicit_songs = False
        
        self.mp3_files = self.get_mp3s('filename')
        
        self.refresh_index()
        
        self.command = ''
        self.focus = 'console'
        self.console = ''
        self.search = ''
        
        # keep updated with controller.py's commands
        self.syntax_highlight_commands = [
            '9',
            '99',
            '900',
            '901',
            '902',
            '903',
            '910',
            '9100',
            '9101',
            '911',
            '80',
            '81',
            '82',
            '1',
            '11',
            '2',
            '3',
            '4',
            '40',
            '44',
            '5',
            '7',
            '77',
            '777',
            '0'
        ]
        
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
        
    def load_index(self):
        with open(self.index_file, 'r') as f:
            data = json.load(f)
            
            if 'songs' not in data:
                data['songs'] = {}
            
            if 'macros' not in data:
                data['macros'] = {}
            
            return data
    
    def save_index(self):
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f)
    
    def refresh_index(self):
        for mp3 in self.mp3_files:
            if mp3 not in self.index["songs"]:
                self.index['songs'][mp3] = {
                    'plays': 0,
                    'explicit': True
                }
        self.save_index()
    
    def reset_index(self):
        data = {
            "songs": {},
            "macros": {}
        }
        for mp3 in self.mp3_files:
            _data = {
                'plays': 0,
                'explicit': False
            }
            data['songs'][mp3] = _data
            
        with open(self.index_file, 'w') as f:
            json.dump(data, f)
    
    def load_mp3s(self, sort):
        self.mp3_files = self.get_mp3s(sort)
        
    def get_mp3s_raw(self):
        return os.listdir(self.mp3_folder)
    
    def get_mp3s(self, sort):
        files = []
        
        files = os.listdir(self.mp3_folder)
        
        if sort == 'random':
            shuffle(files)
            return files
        
        def sorter(file):
            audio = mutagen.File(f'{self.mp3_folder}/{file}', easy=True)
            string = ''
            if sort == 'filename':
                string += file
            elif sort == 'artist+album':
                string += f'{audio['artist']}{audio['album']}'
            elif sort == 'duration':
                string += str(audio.info.length)
            e_sort = ''
            if not self.showing_explicit_songs:
                e_sort = '0' if not self.index['songs'][file]['explicit'] else '1'
            string = e_sort + string
            return string
        
        files.sort(key=sorter)
        
        return files