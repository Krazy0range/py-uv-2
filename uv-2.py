from view import View
from model import Model
from controller import Controller

class Main:
    
    def __init__(self):
        self.model = Model('C:/Users/Teo/Documents/uv-2/mp3s')
        self.view = View()
        self.controller = Controller()
    
    def run(self):
        try:
            
            self.view.start()
            while not self.model.quit:
                self.controller.update(self.model)
                self.view.render(self.model)
            self.view.quit()
            
        except KeyboardInterrupt:
            
            self.view.quit()

if __name__ == '__main__':
    main = Main()
    main.run()