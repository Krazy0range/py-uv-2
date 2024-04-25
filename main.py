import os
import time

from escapecodes import EscapeCodes
from settings import Settings
from renderengine import RenderEngine

class Main:
    
    def __init__(self):
        terminal_size = os.get_terminal_size()
        width = terminal_size[0]
        height = terminal_size[1]
        
        self.esc = EscapeCodes()
        self.settings = Settings()
        
        self.render = RenderEngine(width, height)
    
    def run(self):
        self.render.start()
        
        self.intro_sequence()
        
        self.render.quit()

    def intro_sequence(self):
        
        self.render.string(self.settings.background_accent_color)
        
        for x in range(self.render.width):
            for y in range(self.render.height):
                self.render.add(x, y, ' ')
        
        middle_x = self.render.width // 2
        middle_y = self.render.height // 2
        title_x = middle_x - 1
        title_y = middle_y - 1
        
        self.render.render()
        
        time.sleep(1)
        
        self.render.string(self.settings.cursor_color)
        self.render.add(title_x, title_y, ' ')
        self.render.render()
        
        time.sleep(0.1)
        
        self.render.string(self.settings.background_accent_color)
        self.render.add(title_x, title_y, 'U')
        self.render.string(self.settings.cursor_color)
        self.render.add(title_x + 1, title_y, ' ')
        self.render.render()
        
        time.sleep(0.1)
        
        self.render.string(self.settings.background_accent_color)
        self.render.add(title_x + 1, title_y, 'V')
        self.render.string(self.settings.cursor_color)
        self.render.add(title_x + 2, title_y, ' ')
        self.render.render()
        
        time.sleep(0.1)
        
        self.render.string(self.settings.background_accent_color)
        self.render.add(title_x + 2, title_y, '2')
        self.render.string(self.settings.cursor_color)
        self.render.add(title_x + 3, title_y, ' ')
        self.render.render()
        
        time.sleep(0.5)
        
        self.render.string(self.settings.background_accent_color)
        self.render.add(title_x + 3, title_y, ' ')
        self.render.render()
        
        input()

if __name__ == '__main__':
    main = Main()
    main.run()