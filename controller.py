import msvcrt
import ctypes
from just_playback import Playback

# TODO
# TODO add selection looping instead of just capping at ends
# TODO   will require some good refactoring to code efficiently
# TODO   so good motivation to refactor lol
# TODO
# TODO very poggers
# TODO

class Controller:
    
    def __init__(self):
        self.playback = Playback()
        self.playback_file = ''
    
    def get_key(self):
        
        def getkey():
            c1 = msvcrt.getch()
            if c1 in (b'\x00', b'\xe0'):
                c2 = msvcrt.getch()
                return {b'H': 'up', 
                        b'P': 'down',
                        b'M': 'right',
                        b'K': 'left',
                        b'\x8d': 'ctrl-up',
                        b'\x91': 'ctrl-down',
                        b't': 'ctrl-right',
                        b's': 'ctrl-left',
                        b'G': 'home',
                        b'O': 'end'
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
            model.queue.pop(0)
            model.panel_queue.full_update = True
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
        
        elif key == 'home':
            
            self.cycle_focuses_backwards(model)
        
        elif key == 'end' or key == '\t':
            
            self.cycle_focuses(model)

        elif model.focused_panel == model.panel_library:
            
            self.handle_library_keys(model, key)

        elif model.focused_panel == model.panel_queue:
            
            self.handle_queue_keys(model, key)
        
        elif model.focused_panel == model.panel_console:
            
            command = self.handle_console_keys(model, key)
        
        elif model.focused_panel == model.panel_search:
            
            self.handle_search_keys(model, key)
        
        model.command = command

    def handle_search_keys(self, model, key):
        if key == '\r':
            pass
            
        elif key == '\x08' or key == '.':
            if len(model.search) > 0:
                model.search = model.search[:-1]
                model.panel_library.full_update = True
            
        elif key is not None:
            model.search += key
            model.panel_library.full_update = True

    def handle_console_keys(self, model, key):
        if key == '\r':
                command = model.console
                model.console = ''
                
        elif key == '\x08' or key == '.':
            if len(model.console) > 0:
                model.console = model.console[:-1]

        elif key is not None:
            model.console += key
        return command

    def handle_queue_keys(self, model, key):
        if key == '\r':
            del model.queue[model.panel_queue.selected_index]
            model.panel_queue.full_update = True
            if model.panel_queue.selected_index == 0:
                self.playback.stop()
                if len(model.queue) > 0:
                    if self.playback_file != model.queue[0]:
                        self.playback_file = model.queue[0]
                        self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
                    self.playback.play()
            elif model.panel_queue.selected_index == len(model.queue):
                model.panel_queue.selected_index -= 1
                
        elif key == 'up':
            if model.panel_queue.selected_index > 0:
                model.panel_queue.selected_index -= 1
                    
                if model.panel_queue.selected_index >= len(model.queue):
                    model.panel_queue.selected_index = len(model.queue) - 1
                    
                if model.panel_queue.selected_index < model.panel_queue.scroll:
                    model.panel_queue.scroll = model.panel_queue.selected_index
                    model.panel_queue.full_update = True
            
        elif key == 'down':
            if model.panel_queue.selected_index < len(model.queue) - 1:
                model.panel_queue.selected_index += 1
                    
                if model.panel_queue.selected_index >= len(model.queue):
                    model.panel_queue.selected_index = len(model.queue) - 1
                    
                if model.panel_queue.selected_index > model.panel_queue.scroll + model.panel_queue.scroll_height:
                    model.panel_queue.scroll = model.panel_queue.selected_index - model.panel_queue.scroll_height
                    model.panel_queue.full_update = True

        elif key == 'ctrl-up':
            if model.panel_queue.selected_index > 0:
                i, j = model.panel_queue.selected_index, model.panel_queue.selected_index - 1
                model.queue[j], model.queue[i] = model.queue[i], model.queue[j]

                    # copied from above, needs to be refactored
                    
                model.panel_queue.selected_index -= 1
                    
                if model.panel_queue.selected_index >= len(model.queue):
                    model.panel_queue.selected_index = len(model.queue) - 1
                    
                if model.panel_queue.selected_index < model.panel_queue.scroll:
                    model.panel_queue.scroll = model.panel_queue.selected_index
                    
                model.panel_queue.full_update = True
            
        elif key == 'ctrl-down':
            if model.panel_queue.selected_index < len(model.queue) - 1:
                i, j = model.panel_queue.selected_index, model.panel_queue.selected_index + 1
                model.queue[j], model.queue[i] = model.queue[i], model.queue[j]

                    # copied from above, needs to be refactored
                    
                model.panel_queue.selected_index += 1
                    
                if model.panel_queue.selected_index >= len(model.queue):
                    model.panel_queue.selected_index = len(model.queue) - 1
                    
                if model.panel_queue.selected_index < model.panel_queue.scroll:
                    model.panel_queue.scroll = model.panel_queue.selected_index
                    
                model.panel_queue.full_update = True

    def handle_library_keys(self, model, key):
        if key == '\r':
            model.queue.append(model.mp3_files[model.panel_library.selected_index])
            if len(model.queue) == 1:
                if self.playback_file != model.queue[0]:
                    self.playback_file = model.queue[0]
                    self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
                self.playback.play()
                
        elif key == 'up':
            if model.panel_library.selected_index > 0:
                search_songs = []
                search_songs_local_index = 0
                    
                if not model.search:
                    model.panel_library.selected_index -= 1
                else:
                    songs = list(enumerate(model.mp3_files))
                    search_songs = list(filter(lambda x: model.search.lower() in x[1].lower(), songs))
                    if len(search_songs) > 0:
                        next_index = search_songs[0][0]
                        for j, (i, song) in enumerate(search_songs):
                            if i < model.panel_library.selected_index:
                                next_index = i
                                search_songs_local_index = j
                            else: break
                        model.panel_library.selected_index = next_index
                    
                if model.panel_library.selected_index >= len(model.mp3_files):
                    model.panel_library.selected_index = len(model.mp3_files)
                    
                if model.panel_library.selected_index < model.panel_library.scroll:
                    model.panel_library.scroll = model.panel_library.selected_index
                    model.panel_library.full_update = True
            
        elif key == 'down':
            if model.panel_library.selected_index < len(model.mp3_files) - 1:
                search_songs = []
                search_songs_local_index = 0
                    
                if not model.search:
                    model.panel_library.selected_index += 1
                else:
                    songs = list(enumerate(model.mp3_files))
                    search_songs = list(filter(lambda x: model.search.lower() in x[1].lower(), songs))
                    if len(search_songs) > 0:
                        next_index = search_songs[-1][0]
                        for j, (i, song) in enumerate(search_songs):
                            if i > model.panel_library.selected_index:
                                next_index = i
                                search_songs_local_index = j
                                break
                        model.panel_library.selected_index = next_index
                    
                if model.panel_library.selected_index >= len(model.mp3_files):
                    model.panel_library.selected_index = len(model.mp3_files) - 1                   
                    
                if not model.search:
                    if model.panel_library.selected_index > model.panel_library.scroll + model.panel_library.scroll_height:
                        model.panel_library.scroll = model.panel_library.selected_index - model.panel_library.scroll_height
                        model.panel_library.full_update = True
                else:
                    if search_songs_local_index > model.panel_library.scroll_height:
                        model.panel_library.scroll = search_songs[search_songs_local_index - model.panel_library.scroll_height][0]
                        model.panel_library.full_update = True

    def cycle_focuses(self, model):
        if model.focused_panel == model.panel_library:
            model.focused_panel = model.panel_queue

        elif model.focused_panel == model.panel_queue:
            model.focused_panel = model.panel_console

        elif model.focused_panel == model.panel_console:
            model.focused_panel = model.panel_search

        elif model.focused_panel == model.panel_search:
            model.focused_panel = model.panel_library

    def cycle_focuses_backwards(self, model):
        if model.focused_panel == model.panel_library:
            model.focused_panel = model.panel_search
            
        elif model.focused_panel == model.panel_search:
            model.focused_panel = model.panel_console
            
        elif model.focused_panel == model.panel_console:
            model.focused_panel = model.panel_queue
            
        elif model.focused_panel == model.panel_queue:
            model.focused_panel = model.panel_library
    
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
            model.reset_screen = True
            model.panel_library.full_update = True
            model.panel_queue.full_update = True
            model.panel_console.full_update = True
            model.panel_search.full_update = True
        
        # sort by filename
        elif command == '900':
            model.load_mp3s('filename')
            model.panel_library.full_update = True
        
        # sort by artist+album
        elif command == '901':
            model.load_mp3s('artist+album')
            model.panel_library.full_update = True
        
        # sort by duration
        elif command == '902':
            model.load_mp3s('duration')
            model.panel_library.full_update = True
        
        # sort randomly
        elif command == '903':
            model.load_mp3s('random')
            model.panel_library.full_update = True
        
        # toggle showing explicit songs
        elif command == '910':
            model.showing_explicit_songs = not model.showing_explicit_songs
            model.load_mp3s('filename')
            model.panel_library.full_update = True
        
        # set showing explicit songs to false
        elif command == '9100':
            if model.showing_explicit_songs:
                model.showing_explicit_songs = False
                model.load_mp3s('filename')
                model.panel_library.full_update = True
        
        # set showing explicit songs to true
        elif command == '9101':
            if not model.showing_explicit_songs:
                model.showing_explicit_songs = True
                model.load_mp3s('filename')
                model.panel_library.full_update = True
        
        # toggle a song's explicitness
        elif command == '911':
            mp3 = model.mp3_files[model.panel_library.selected_index]
            model.index['songs'][mp3]['explicit'] = not model.index['songs'][mp3]['explicit']
            model.save_index()
            model.load_mp3s('filename')
            model.panel_library.full_update = True
            
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
                model.panel_library.scroll = min(n, len(model.mp3_files) - 1)
                model.panel_library.full_update = True
        
        # add selected song
        elif command == '4':
            model.queue.append(model.mp3_files[model.panel_library.selected_index])
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
            model.queue.insert(1, model.mp3_files[model.panel_library.selected_index])
            model.panel_queue.full_update = True
        
        # skip
        elif command == '7':
            self.playback.stop()
            if len(model.queue) > 0:
                model.queue.pop(0)
                model.panel_queue.full_update = True
            if len(model.queue) > 0:
                if self.playback_file != model.queue[0]:
                    self.playback_file = model.queue[0]
                    self.playback.load_file(f'{model.mp3_folder}/{model.queue[0]}')
                self.playback.play()
        
        # clear queue except for currently playing song
        elif command == '77':
            if len(model.queue) > 0:
                model.queue = [model.queue[0]]
                model.panel_queue.full_update = True
        
        # clear entire queue
        elif command == '777':
            if len(model.queue) > 0:
                self.playback.stop()
                model.queue = []
                model.panel_queue.full_update = True
        
        # select song
        elif len(command) > 1 and command[0] == '0':
            number = command[1:]
            if number.isnumeric():
                number = int(number)
                if number >= -1 and number < len(model.mp3_files):
                    model.panel_library.selected_index = number
    
    def title_terminal(self, model):
        title = ''
        if len(model.queue) > 0:
            title = 'uv-2: ' + model.queue[0][:-4]
        else:
            title = 'uv-2'
        
        ctypes.windll.kernel32.SetConsoleTitleW(title)