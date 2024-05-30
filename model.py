import os
from random import shuffle
import mutagen
import json

from panel import Library, Queue, Console, Search

class Model:
    
    def __init__(self, mp3_folder, index_file):
        self.mp3_folder = mp3_folder
        
        self.mp3_files = self.get_mp3s_raw()
        
        self.index_file = index_file
        self.index = self.load_index()
        self.refresh_index()
        
        self.showing_explicit_songs = False
        
        self.mp3_files = self.get_mp3s('filename')
        
        self.refresh_index()
        
        self.command = ''
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
        
        self.reset_screen = False
        
        self.panel_library = Library()
        self.panel_queue = Queue()
        self.panel_console = Console()
        self.panel_search = Search()
        
        self.focused_panel = self.panel_library
        
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
            return string
        
        if not self.showing_explicit_songs:
            files = list(filter(lambda x: not self.index['songs'][x]['explicit'], files))
            
        files.sort(key=sorter)
        
        return files