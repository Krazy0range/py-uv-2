from platform import java_ver
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
    
    def render(self, model, x, y, width, height):
        self.string = ''
        self.string += self.esc.reset_all()
        
        if self.full_update:
            self.string += self.fill(x, y, width, height, self.esc.background_black())
            self.full_update = False
        
        self.string += self.esc.move(x+2, y+1)
        self.string += self.esc.background_black() + self.esc.foreground_red() + 'LIBRARY' + self.esc.reset_all()
        
        x += 2
        y += 3
        width -= 4
        height -= 4
        
        for i in range(len(model.mp3_files[:height+1])):
            j = i + model.scroll
            if j < 0: continue
            if j >= len(model.mp3_files): break
            mp3_file = model.mp3_files[j]
            song = mp3_file[:-4]
            self.string += self.esc.move(x, y + i)
            self.string += self.esc.background_red() if j == model.selected_song_index else self.esc.background_black()
            self.string += self.esc.foreground_red() if mp3_file in model.queue and j != model.selected_song_index else self.esc.foreground_white()
            self.string += f'{j}{self.tab(str(j))}{song}'
        
        self.string += self.esc.reset_all()
        return self.string


class Queue(Panel):
    
    def __init__(self):
        super().__init__()
        
    def render(self, model, x, y, width, height):
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
        
        mp3_files = model.queue[:height+1]
        
        for i, mp3_file in enumerate(mp3_files):
            song = mp3_file[:-4]
            self.string += self.esc.move(x, y + i)
            self.string += self.esc.background_red() if i == 0 else self.esc.background_black()
            self.string += str(i) + self.tab(str(i))
            self.string += song
        
        self.string += self.esc.move(x, y + len(mp3_files))
        self.string += self.esc.background_black()
        self.string += (' ' * width)
        
        self.string += self.esc.reset_all()
        return self.string


class Console(Panel):
    
    def __init__(self):
        super().__init__()
        
    def render(self, model, x, y, width, height):
        self.string = ''
        self.string += self.esc.reset_all()
        
        if self.full_update:
            self.string += self.fill(x, y, width, height, self.esc.background_black())
            self.full_update = False
            
        self.string += self.esc.move(x+2, y+1)
        self.string += self.esc.background_black()
        self.string += self.esc.foreground_red()
        self.string += model.console
        self.string += self.esc.background_red()
        self.string += ' '
        self.string += self.esc.background_black()
        self.string += ' ' * (width - len(model.console) - 3)
        
        self.string += self.esc.reset_all()
        return self.string