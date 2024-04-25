import os
import cursor

from escapecodes import EscapeCodes

class RenderEngine:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.cursor_x = 0
        self.cursor_y = 0
        
        self.esc = EscapeCodes()
        
        self._string = ""
    
    def start(self):
        self.clear()
        cursor.hide()
        self.cursor_x, self.cursor_y = 0, 0
        print(self.esc.move_home())
    
    def quit(self):
        print(self.esc.reset_all(), end='')
        self.clear()
        cursor.show()
    
    def clear(self):
        print(self.esc.clear(), end='')
        os.system('cls')

    def string(self, string):
        self._string += string
        
    def render(self):
        self.string(self.esc.move_home())
        print(self._string)
    
    def add(self, x, y, char):
        self.string(self.esc.move(x + 1, y + 1) + char)
    
    def foreground_color(self, color):
        code = ''
        if color == 'black':
            code = self.esc.foreground_black()
        elif color == 'red':
            code = self.esc.foreground_red()
        elif color == 'green':
            code = self.esc.foreground_green()
        elif color == 'yellow':
            code = self.esc.foreground_yellow()
        elif color == 'blue':
            code = self.esc.foreground_blue()
        elif color == 'magenta':
            code = self.esc.foreground_magenta()
        elif color == 'cyan':
            code = self.esc.foreground_cyan()
        elif color == 'white':
            code = self.esc.foreground_white()
        self.string(code)
        
    def background_color(self, color):
        code = ''
        if color == 'black':
            code = self.esc.background_black()
        elif color == 'red':
            code = self.esc.background_red()
        elif color == 'green':
            code = self.esc.background_green()
        elif color == 'yellow':
            code = self.esc.background_yellow()
        elif color == 'blue':
            code = self.esc.background_blue()
        elif color == 'magenta':
            code = self.esc.background_magenta()
        elif color == 'cyan':
            code = self.esc.background_cyan()
        elif color == 'white':
            code = self.esc.background_white()
        self.string(code)