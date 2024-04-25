import os
import time

from renderengine import RenderEngine

class Main:
    
    def __init__(self):
        terminal_size = os.get_terminal_size()
        width = terminal_size[0]
        height = terminal_size[1]
        self.render = RenderEngine(width, height)
    
    def run(self):
        self.render.start()
        
        self.render.background_color('red')
        
        for x in range(self.render.width):
            for y in range(self.render.height):
                self.render.add(x, y, ' ')
        
        middle_x = self.render.width // 2
        middle_y = self.render.height // 2
        self.render.add(middle_x - 1, middle_y - 1, 'UV2')
        
        message1 = 'escapecode colors!!!'
        message2 = 'todo: add panels :)'
        self.render.add(middle_x - len(message1) // 2, middle_y + 1, message1)
        self.render.add(middle_x - len(message2) // 2, middle_y + 2, message2)
        
        self.render.render()
        
        input()
        
        self.render.quit()

if __name__ == '__main__':
    main = Main()
    main.run()