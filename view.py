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
        
        self.counter = 0
    
    def render(self, model):
        
        self.update_panel_focuses(model)

        if model.reset_screen:
            self.engine.clear()
            terminal_size = os.get_terminal_size()
            width = terminal_size[0]
            height = terminal_size[1]
            self.engine.width = width
            self.engine.height = height
            model.reset_screen = False
            
        if not model.queue_only_view:
        
            library = model.panel_library.render(model, 
                                        x=0, 
                                        y=1, 
                                        width=self.engine.width // 2 - 1, 
                                        height=self.engine.height - 5
                                        )
            self.engine.string(library)
            
            queue = model.panel_queue.render(model,
                                        x=self.engine.width // 2 + 3,
                                        y=1,
                                        width=self.engine.width // 2 - 3,
                                        height=self.engine.height - 5
                                        )
            self.engine.string(queue)
            
            console = model.panel_console.render(model,
                                        x=0,
                                        y=self.engine.height - 2,
                                        width=self.engine.width // 2 - 1,
                                        height=2
                                        )
            self.engine.string(console)
            
            search = model.panel_search.render(model,
                                        x=self.engine.width // 2 + 3,
                                        y=self.engine.height - 2,
                                        width=self.engine.width // 2 - 3,
                                        height=2
                                        )
            self.engine.string(search)
        
        else:
            
            queue = model.panel_queue.render(model,
                                        x=1,
                                        y=1,
                                        width=self.engine.width - 1,
                                        height=self.engine.height - 1
                                        )
            self.engine.string(queue)
        
        self.engine.render()
        
        model.panel_library.full_update = False
        model.panel_queue.full_update = False
        model.panel_console.full_update = False
        model.panel_search.full_update = False
    
    def update_panel_focuses(self, model):
        model.panel_library.focused = False
        model.panel_queue.focused = False
        model.panel_console.focused = False
        model.panel_search.focused = False

        model.focused_panel.focused = True
    
    def start(self):
        self.engine.start()
        
    def quit(self):
        self.engine.quit()