class EscapeCodes:
    
    def __init__(self):
        
        # Clear
        
        self._clear = '\033[2J'
        
        # Cursor visibilty
        
        self._cursor_hide = '\033[?25l'
        self._cursor_show = '\033[?25h'
        
        # Movement
        
        # self._move_home = '\033[H' # not working
        self._move = '\033[{};{}H'
        self._move_up = '\033[{}A'
        self._move_down = '\033[{}B'
        self._move_right = '\033[{}C'
        self._move_left = '\033[{}D'
        
        # Colors / Styles
        
        self._reset_all = '\033[0m'
        self._reset_foreground_color = '\033[39m'
        self._reset_background_color = '\033[49m'
        
        self._bold_mode = '\033[1m'
        self._dim_mode = '\033[2m'
        self._italic_mode = '\033[3m'
        self._underline_mode = '\033[4m'
        self._blinking_mode = '\033[5m'
        self._reverse_mode  = '\033[7m'
        self._hidden_mode = '\033[8m'
        self._strikethrough_mode = '\033[9m'
        
        self._foreground_black = '\033[30m'
        self._foreground_red = '\033[31m'
        self._foreground_green = '\033[32m'
        self._foreground_yellow = '\033[33m'
        self._foreground_blue = '\033[34m'
        self._foreground_magenta = '\033[35m'
        self._foreground_cyan = '\033[36m'
        self._foreground_white = '\033[37m'
        
        self._background_black = '\033[40m'
        self._background_red = '\033[41m'
        self._background_green = '\033[42m'
        self._background_yellow = '\033[m3m'
        self._background_blue = '\033[44m'
        self._background_magenta = '\033[45m'
        self._background_cyan = '\033[46m'
        self._background_white = '\033[47m'
        
        self._foreground_code = '\033[38;5;{}m'
        self._background_code = '\033[48;5;{}m'
        
        self._foreground_rgb = '\033[38;2;{};{};{}m'
        self._background_rgb = '\033[48;2;{};{};{}m'
        
    # Clear
    
    def clear(self): return self._clear
    
    # Cursor Visibility
    
    def cursor_hide(self): return self._cursor_hide

    def cursor_show(self): return self._cursor_show
        
    # Movement
    
    def move_home(self): return self._move.format(0, 0)
        
    def move(self, x, y): return self._move.format(y, x)
    
    def move_up(self, x): return self._move_up.format(x)
    
    def move_down(self, x): return self._move_down.format(x)
    
    def move_right(self, x): return self._move_right.format(x)
    
    def move_left(self, x): return self._move_left.format(x)
    
    # Colors / Styles
    
    def reset_all(self): return self._reset_all
    
    def reset_foreground_color(self): return self._reset_foreground_color
    
    def reset_background_color(self): return self._reset_background_color
    
    def bold_mode(self): return self._bold_mode

    def dim_mode(self): return self._dim_mode

    def italic_mode(self): return self._italic_mode

    def underline_mode(self): return self._underline_mode

    def blinking_mode(self): return self._blinking_mode

    def reverse_mode(self): return self._reverse_mode

    def hidden_mode(self): return self._hidden_mode

    def strikethrough_mode(self): return self._strikethrough_mode
    
    def foreground_black(self): return self._foreground_black
    
    def foreground_red(self): return self._foreground_red

    def foreground_green(self): return self._foreground_green
    
    def foreground_yellow(self): return self._foreground_yellow
    
    def foreground_blue(self): return self._foreground_blue
    
    def foreground_magenta(self): return self._foreground_magenta
    
    def foreground_cyan(self): return self._foreground_cyan

    def foreground_white(self): return self._foreground_white
    
    def background_black(self): return self._background_black
    
    def background_red(self): return self._background_red
    
    def background_green(self): return self._background_green
    
    def background_yellow(self): return self._background_yellow
    
    def background_blue(self): return self._background_blue
    
    def background_magenta(self): return self._background_magenta
    
    def background_cyan(self): return self._background_cyan
    
    def background_white(self): return self._background_white
    
    def foreground_code(self, x): return self._foreground_code.format(x)
    
    def background_code(self, x): return self._background_code.format(x)
    
    def foreground_rgb(self, r, g, b): return self._foreground_rgb.format(r, g, b)
    
    def background_rgb(self, r, g, b): return self._background_rgb.format(r, g, b)