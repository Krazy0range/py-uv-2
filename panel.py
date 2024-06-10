from escapecodes import EscapeCodes


class Panel:
    
    def __init__(self):
        self.esc = EscapeCodes()
        self.string = ''
        self.full_update = True
    
    def fill(self, x, y, width, height, bg):
        string = bg
        for i in range(height + 1):
            string += self.esc.move(x, y + i)
            string += ' ' * (width + 1)
        return string
    
    def tab(self, string):
        return ' ' * (8 - len(string))

    def render(self, model, x, y, width, height):
        pass


class Library(Panel):
    
    def __init__(self):
        super().__init__()
        self.selected_index = 0
        self.scroll = 0
        self.scroll_height = 0
    
    def render(self, model, x, y, width, height):
        focused = model.focused_panel == self
        
        self.scroll_height = height - 4
        
        self.string = ''
        self.string += self.esc.reset_all()
        
        if self.full_update:
            self.string += self.fill(x, y, width, height, self.esc.background_black())
            self.full_update = False
        
        self.string += self.esc.move(x+3, y+1)
        self.string += self.esc.background_black() + self.esc.foreground_red() + 'LIBRARY' + self.esc.reset_all()
        
        x += 3
        y += 3
        width -= 4
        height -= 4
        
        i_off = 0
        
        for i in range(len(model.mp3_files)):
            j = i + self.scroll
            if j < 0: continue
            if j >= len(model.mp3_files): break
            if i - i_off > height: break
            mp3_file = model.mp3_files[j]
            if not model.showing_explicit_songs and model.index['songs'][mp3_file]['explicit']:
                continue
            song = mp3_file[:-4]
            if model.search.lower() not in song.lower():
                i_off += 1
                continue
            selected = j == self.selected_index
            self.string += self.esc.move(x, y + i - i_off)
            self.string += self.esc.background_red() if selected and focused else self.esc.background_black()
            self.string += self.esc.foreground_red() if mp3_file in model.queue and not (selected and focused) else self.esc.foreground_white()
            self.string += f'{j}{self.tab(str(j))}{song}'[:width-1]
            if model.index['songs'][mp3_file]['explicit']:
                self.string += self.esc.move(x + 5, y + i - i_off)
                self.string += self.esc.background_black() if not (selected and focused) else ''
                self.string += self.esc.foreground_red() if not (selected and focused) else ''
                self.string += 'E'
                self.string += self.esc.reset_all()
        
        self.string += self.esc.reset_all()
        return self.string


class Queue(Panel):
    
    def __init__(self):
        super().__init__()
        self.selected_index = 0
        self.scroll = 0
        self.scroll_height = 0
        
    def render(self, model, x, y, width, height):
        focused = model.focused_panel == self
        
        self.scroll_height = height - 4
        
        self.string = ''
        self.string += self.esc.reset_all()
        
        if self.full_update:
            self.string += self.fill(x, y, width, height, self.esc.background_black())
            self.full_update = False
        
        self.string += self.esc.move(x+2, y+1)
        self.string += self.esc.background_black() + self.esc.foreground_red() + 'QUEUE' + self.esc.reset_all()
        
        x += 2
        y += 3
        width -= 4
        height -= 4
        
        mp3_files = model.queue
        
        # for i, mp3_file in enumerate(mp3_files):
        for i in range(len(mp3_files)):
            j = i + self.scroll
            if j < 0: continue
            if j >= len(mp3_files): break
            if i > height: break
            mp3_file = mp3_files[j]
            song = mp3_file[:-4]
            self.string += self.esc.move(x, y + i)
            self.string += self.esc.background_red() if j == self.selected_index and focused else self.esc.background_black()
            self.string += str(j) + self.tab(str(j))
            self.string += song[:width-9]
        
        self.string += self.esc.move(x, y + min(len(mp3_files), height+1))
        self.string += self.esc.background_black()
        self.string += (' ' * width)
        
        self.string += self.esc.reset_all()
        return self.string


class Console(Panel):
    
    def __init__(self):
        super().__init__()
        
    def render(self, model, x, y, width, height):
        focused = model.focused_panel == self
        
        self.string = ''
        self.string += self.esc.reset_all()
        
        if self.full_update:
            self.string += self.fill(x, y, width, height, self.esc.background_black())
            self.full_update = False
            
        self.string += self.esc.move(x+3, y+1)
        self.string += self.esc.background_black()
        self.string += self.esc.foreground_red()
        self.string += self.enhance_console(model)
        if focused:
            self.string += self.esc.background_red()
            self.string += ' '
        self.string += self.esc.background_black()
        self.string += ' ' * (width - len(model.console) - 4)
        
        self.string += self.esc.reset_all()
        return self.string
    
    def enhance_console(self, model):
        enhanced = ''
        command_built = ''
        
        def command_part():
            for command in model.syntax_highlight_commands:
                if command[0:len(command_built)] == command_built:
                    return True
            return False
        
        for char in model.console:
            if char != '+' and not char.isalpha():
                command_built += char
            else:
                command_built = ''
            
            if char == '+':
                enhanced += self.esc.dim_mode()
                enhanced += self.esc.foreground_white()
            elif command_part():
                enhanced += self.esc.foreground_yellow()
            else:
                enhanced += self.esc.foreground_red()
                
            enhanced += char
            
            if char == '+':
                enhanced += self.esc.reset_all()
                enhanced += self.esc.background_black()
        
        return enhanced


class Search(Panel):
    
    def __init__(self):
        super().__init__()
        
    def render(self, model, x, y, width, height):
        focused = model.focused_panel == self
        
        self.string = ''
        self.string += self.esc.reset_all()
        
        if self.full_update:
            self.string += self.fill(x, y, width, height, self.esc.background_black())
            self.full_update = False
            
        self.string += self.esc.move(x+2, y+1)
        self.string += self.esc.background_black()
        self.string += self.esc.foreground_red()
        self.string += model.search
        if focused:
            self.string += self.esc.background_red()
            self.string += ' '
        self.string += self.esc.background_black()
        self.string += ' ' * (width - len(model.search) - 4)
        
        self.string += self.esc.reset_all()
        return self.string