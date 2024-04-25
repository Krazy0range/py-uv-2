from escapecodes import EscapeCodes

class Settings:
    
    def __init__(self):
        
        self.esc = EscapeCodes()
        
        # Colors
        
        self.foreground_accent_color = self.esc.foreground_red()
        self.foreground_secondary_color = self.esc.foreground_code(242)
        self.foreground_tertiary_color = self.esc.foreground_code(245)
        
        self.background_accent_color = self.esc.background_red()
        self.foreground_secondary_color = self.esc.background_code(242)
        self.foreground_tertiary_color = self.esc.background_code(245)
        
        self.text_color = self.esc.foreground_white()
        
        self.cursor_color = self.esc.background_white()