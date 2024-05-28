import msvcrt
import ctypes
from just_playback import Playback

class Controller:
    
    def __init__(self):
        self.playback = Playback()
        self.playback_file = ''
    
    def get_key(self):
        
        def getkey():
            c1 = msvcrt.getch()
            if c1 in (b'\x00', b'\xe0'):
                c2 = msvcrt.getch()
                if c2 == '[':
                    c3 = msvcrt.getch()
                    return arrows.get(c3, ' ')
                return {b'H': 'up', 
                        b'P': 'down',
                        b'M': 'right',
                        b'K': 'left'
                        }.get(c2, c1 + c2)
            else:
                return chr(ord(c1))
            
        # return chr(ord(msvcrt.getch())) if msvcrt.kbhit() else None
        # return chr(ord(getkey())) if msvcrt.kbhit() else None
        return getkey() if msvcrt.kbhit() else None
    
    def update(self, model):
        self.handle_keys(model)
        self.handle_commands(model)
        self.handle_queue(model)
        self.title_terminal(model)
        
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
    
    def handle_keys(self, model):
        key = self.get_key()
        
        command = ''
        
        if not key:
            pass
        
        elif key == 'up':
            model.selected_song_index -= 1
        
        elif key == 'down':
            model.selected_song_index += 1
        
        elif key == '\t':
            if model.focus == 'console':
                model.focus = 'search'
            elif model.focus == 'search':
                model.focus = 'console'
        
        elif model.focus == 'console':
            
            if key == '\r':
                if len(model.console) > 0:
                    command = model.console
                    model.console = ''
                else:
                    model.queue.append(model.mp3_files[model.selected_song_index])
                    if len(model.queue) == 1:
                        if self.playback_file != model.queue[0]:
                            self.playback_file = model.queue[0]
                            self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
                        self.playback.play()
                
            elif key == '\x08' or key == '.':
                if len(model.console) > 0:
                    model.console = model.console[:-1]

            elif key is not None:
                model.console += key
        
        elif model.focus == 'search':
            
            if key == '\r':
                pass
            
            elif key == '\x08' or key == '.':
                if len(model.search) > 0:
                    model.search = model.search[:-1]
                    model.library_full_update = True
            
            elif key is not None:
                model.search += key
                model.library_full_update = True
        
        model.command = command
    
    def handle_commands(self, model):
        # when defining macros don't split the plusses
        if len(model.command) > 2 and model.command[:2] == '81':
            self.handle_command(model, model.command)
        else:
            commands = model.command.split('+')
            for command in commands:
                self.handle_command(model, command)

    def handle_command(self, model, command):
        
        if not command:
            return
        
        # Bruh idk ;-;
        
        # quit
        if command == '9':
            model.quit = True
        
        # rerender
        elif command == '99':
            model.library_full_update = True
            model.queue_full_update = True
            model.console_full_update = True
            model.reset_screen = True
        
        # sort by filename
        elif command == '900':
            model.load_mp3s('filename')
            model.library_full_update = True
        
        # sort by artist+album
        elif command == '901':
            model.load_mp3s('artist+album')
            model.library_full_update = True
        
        # sort by duration
        elif command == '902':
            model.load_mp3s('duration')
            model.library_full_update = True
        
        # sort randomly
        elif command == '903':
            model.load_mp3s('random')
            model.library_full_update = True
        
        # toggle showing explicit songs
        elif command == '910':
            model.showing_explicit_songs = not model.showing_explicit_songs
            model.load_mp3s('filename')
            model.library_full_update = True
        
        # set showing explicit songs to false
        elif command == '9100':
            if model.showing_explicit_songs:
                model.showing_explicit_songs = False
                model.load_mp3s('filename')
                model.library_full_update = True
        
        # set showing explicit songs to true
        elif command == '9101':
            if not model.showing_explicit_songs:
                model.showing_explicit_songs = True
                model.load_mp3s('filename')
                model.library_full_update = True
        
        # toggle a song's explicitness
        elif command == '911':
            mp3 = model.mp3_files[model.selected_song_index]
            model.index['songs'][mp3]['explicit'] = not model.index['songs'][mp3]['explicit']
            model.save_index()
            model.load_mp3s('filename')
            model.library_full_update = True
            
        # run macro
        elif len(command) == 3 and command[:2] == '80':
            param = command[2]
            if param.isalpha():
                if param in model.index['macros']:
                    model.console = model.index['macros'][param]
        
        # save macro
        elif len(command) > 3 and command[:2] == '81':
            param0 = command[2]
            if param0.isalpha():
                param1 = command[3:]
                model.index['macros'][param0] = param1
                model.save_index()
        
        # delete macro
        elif len(command) == 3 and command[:2] == '82':
            param = command[2]
            if param.isalpha():
                if param in model.index['macros']:
                    del model.index['macros'][param]
                    model.save_index()
                    
        # pause
        elif command == '1':
            self.playback.pause()
        
        # resume
        elif command == '11':
            self.playback.resume()
        
        # seek
        elif len(command) > 1 and command[0] == '2':
            n = command[1:]
            if n.isnumeric():
                n = int(n)
                self.playback.seek(n)
        
        # scroll
        elif len(command) > 1 and command[0] == '3':
            n = command[1:]
            if n.isnumeric():
                n = int(n)
                model.scroll = min(n, len(model.mp3_files) - 1)
                model.library_full_update = True
        
        # add selected song
        elif command == '4':
            model.queue.append(model.mp3_files[model.selected_song_index])
            if len(model.queue) == 1:
                if self.playback_file != model.queue[0]:
                    self.playback_file = model.queue[0]
                    self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
                self.playback.play()
        
        # select song and add it
        elif len(command) > 2 and command[:2] == '40':
            number = command[2:]
            if number.isnumeric():
                number = int(number)
                if number >= -1 and number < len(model.mp3_files):
                    model.queue.append(model.mp3_files[number])
                    if len(model.queue) == 1:
                        if self.playback_file != model.queue[0]:
                            self.playback_file = model.queue[0]
                            self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
                        self.playback.play()
        
        # add all
        elif command == '44':
            for song in model.mp3_files:
                model.queue.append(song)
            if len(model.queue) == len(model.mp3_files):
                if self.playback_file != model.queue[0]:
                    self.playback_file = model.queue[0]
                    self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
                self.playback.play()

        # insert
        elif command == '5':
            model.queue.insert(1, model.mp3_files[model.selected_song_index])
            model.queue_full_update = True
        
        # skip
        elif command == '7':
            self.playback.stop()
            if len(model.queue) > 0:
                model.queue_prev.append(model.queue.pop(0))
                model.queue_full_update = True
            if len(model.queue) > 0:
                if self.playback_file != model.queue[0]:
                    self.playback_file = model.queue[0]
                    self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
                self.playback.play()
        
        # clear queue except for currently playing song
        elif command == '77':
            if len(model.queue) > 0:
                model.queue = [model.queue[0]]
                model.queue_full_update = True
        
        # clear entire queue
        elif command == '777':
            if len(model.queue) > 0:
                self.playback.stop()
                model.queue = []
                model.queue_full_update = True
        
        # select song
        elif len(command) > 1 and command[0] == '0':
            number = command[1:]
            if number.isnumeric():
                number = int(number)
                if number >= -1 and number < len(model.mp3_files):
                    model.selected_song_index = number
    
    def title_terminal(self, model):
        title = ''
        if len(model.queue) > 0:
            title = 'uv-2: ' + model.queue[0][:-4]
        else:
            title = 'uv-2'
        
        ctypes.windll.kernel32.SetConsoleTitleW(title)