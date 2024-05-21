import msvcrt
from just_playback import Playback

class Controller:
    
    def __init__(self):
        self.playback = Playback()
        self.playback_file = ''
    
    def get_key(self):
        return chr(ord(msvcrt.getch())) if msvcrt.kbhit() else None
    
    def update(self, model):
        model.command = self.handle_console(model)
        self.handle_command(model)
        self.handle_queue(model)
        
    def handle_queue(self, model):
        if len(model.queue) == 0:
            return
        
        if self.playback_file != model.queue[0]:
            self.playback_file = model.queue[0]
            self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
            self.playback.play()
        
        if self.playback.curr_pos >= self.playback.duration:
            model.queue_prev.append(model.queue.pop(0))
            model.queue_full_update = True
            if len(model.queue) > 0:
                if self.playback_file != model.queue[0]:
                    self.playback_file = model.queue[0]
                    self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
                self.playback.play()
    
    def handle_console(self, model):
        key = self.get_key()
        
        command = ''
        
        if not key:
            return command
        
        if key == '\r':
            command = model.console
            model.console = ''
            
        elif key == '\x08' or key == '.':
            if len(model.console) > 0:
                model.console = model.console[:-1]

        elif key is not None:
            model.console += key
        
        return command

    def handle_command(self, model):
        
        if not model.command:
            return
        
        # Bruh idk ;-;
        
        # quit
        if model.command == '9':
            model.quit = True
        
        # rerender
        elif model.command == '99':
            model.library_full_update = True
            model.queue_full_update = True
            model.console_full_update = True
            model.reset_screen = True
        
        # sort by filename
        elif model.command == '900':
            model.load_mp3s('filename')
            model.library_full_update = True
        
        # sort by artist+album
        elif model.command == '901':
            model.load_mp3s('artist+album')
            model.library_full_update = True
        
        # sort by duration
        elif model.command == '902':
            model.load_mp3s('duration')
            model.library_full_update = True
        
        # sort randomly
        elif model.command == '903':
            model.load_mp3s('random')
            model.library_full_update = True
        
        # toggle showing explicit songs
        elif model.command == '910':
            model.showing_explicit_songs = not model.showing_explicit_songs
            model.load_mp3s('filename')
            model.library_full_update = True
        
        # toggle explicit
        elif model.command == '911':
            mp3 = model.mp3_files[model.selected_song_index]
            model.index['songs'][mp3]['explicit'] = not model.index['songs'][mp3]['explicit']
            model.save_index()
            model.load_mp3s('filename')
            model.library_full_update = True
                    
        # pause
        elif model.command == '1':
            self.playback.pause()
        
        # resume
        elif model.command == '11':
            self.playback.resume()
        
        # seek
        elif len(model.command) > 1 and model.command[0] == '2':
            n = model.command[1:]
            if n.isnumeric():
                n = int(n)
                self.playback.seek(n)
        
        # scroll
        elif len(model.command) > 1 and model.command[0] == '3':
            n = model.command[1:]
            if n.isnumeric():
                n = int(n)
                model.scroll = min(n, len(model.mp3_files) - 1)
                model.library_full_update = True
        
        # add
        elif model.command == '4':
            model.queue.append(model.mp3_files[model.selected_song_index])
            if len(model.queue) == 1:
                if self.playback_file != model.queue[0]:
                    self.playback_file = model.queue[0]
                    self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
                self.playback.play()
        
        # add all
        elif model.command == '44':
            for song in model.mp3_files:
                model.queue.append(song)
            if len(model.queue) == len(model.mp3_files):
                if self.playback_file != model.queue[0]:
                    self.playback_file = model.queue[0]
                    self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
                self.playback.play()

        # insert
        elif model.command == '5':
            model.queue.insert(1, model.mp3_files[model.selected_song_index])
            model.queue_full_update = True
        
        # skip
        elif model.command == '7':
            self.playback.stop()
            if len(model.queue) > 0:
                model.queue_prev.append(model.queue.pop(0))
                model.queue_full_update = True
            if len(model.queue) > 0:
                if self.playback_file != model.queue[0]:
                    self.playback_file = model.queue[0]
                    self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
                self.playback.play()
        
        # clear queue
        elif model.command == '77':
            model.clear_queue = True
            model.clear_queue_len = len(model.queue) + len(model.queue_prev)
            model.queue = [model.queue[0]]
            model.queue_full_update = True
        
        # select song
        elif len(model.command) > 1 and model.command[0] == '0':
            number = model.command[1:]
            if number.isnumeric():
                number = int(model.command[1:])
                if number >= -1 and number < len(model.mp3_files):
                    model.selected_song_index = number