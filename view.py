import os

from escapecodes import EscapeCodes
from settings import Settings
from renderengine import RenderEngine

from panel import Library
from panel import Queue
from panel import Console
from panel import Search

class View:
    
    def __init__(self):
        terminal_size = os.get_terminal_size()
        width = terminal_size[0]
        height = terminal_size[1]
        
        self.esc = EscapeCodes()
        self.settings = Settings()
        self.engine = RenderEngine(width, height)
        
        self.library = Library()
        self.queue = Queue()
        self.console = Console()
        self.search = Search()
        
        self.counter = 0
    
    def render(self, model):
        
        self.library.full_update = model.library_full_update
        self.queue.full_update = model.queue_full_update
        self.console.full_update = model.console_full_update
        self.search.full_update = model.console_full_update # makeshift fix but should work fine
        
        if model.reset_screen:
            self.engine.clear()
            terminal_size = os.get_terminal_size()
            width = terminal_size[0]
            height = terminal_size[1]
            self.engine.width = width
            self.engine.height = height
        
        model.library_full_update = False
        model.queue_full_update = False
        model.console_full_update = False
        model.reset_screen = False
        
        library = self.library.render(model, 
                                      x=2, 
                                      y=1, 
                                      width=self.engine.width // 2 - 2, 
                                      height=self.engine.height - 5
                                      )
        self.engine.string(library)
        
        queue = self.queue.render(model,
                                    x=self.engine.width // 2 + 3,
                                    y=1,
                                    width=self.engine.width // 2 - 3,
                                    height=self.engine.height - 5
                                    )
        self.engine.string(queue)
        
        console = self.console.render(model,
                                      x=2,
                                      y=self.engine.height - 2,
                                      width=self.engine.width // 2 - 2,
                                      height=2
                                      )
        self.engine.string(console)
        
        search = self.search.render(model,
                                    x=self.engine.width // 2 + 3,
                                    y=self.engine.height - 2,
                                    width=self.engine.width // 2 - 3,
                                    height=2
                                    )
        self.engine.string(search)
        
        self.engine.render()
    
    def start(self):
        self.engine.start()
        
    def quit(self):
        self.engine.quit()