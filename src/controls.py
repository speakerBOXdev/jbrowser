
HSTEP, VSTEP = 12, 18
class ScrollBar:

    def __init__(self, thickness=5, color="#229", visible=True, direction="vertical"):
        self.thickness=thickness
        self.color=color
        self.visible=visible
        self.direction=direction
        assert self.direction in ["vertical", "horizontal"]
        
        if self.direction == "vertical":
            self.margin=(0, 15, 2, 15) # L, T, R, B
        elif self.direction == "horizontal":
            self.margin=(15, 0, 15, 2) # L, T, R, B
        
        self.scroll_y=0
        self.scroll_x=0

        self.window_size=(800, 600)
        self.max_size=(800,600)

    def update(self, window, max, scroll):
        self.window_size=window
        self.max_size=max
        self.scroll_x, self.scroll_y=scroll

        window_width, window_height=self.window_size
        max_x, max_y = self.max_size

        if self.direction == "vertical":
            self.visible=max_y > window_height
        elif self.direction == "horizontal":
            self.visible=max_x > window_width

    def draw(self, canvas):
        if self.visible != True:
            return
        
        l, t, r, b = self.margin

        window_width, window_height=self.window_size
        max_x, max_y = self.max_size

        if self.direction == "vertical":
            # Horizontal is fixed
            x0=window_width-self.thickness-r
            x1=window_width-r

            # Calculate percentages for vertical
            range=window_height-t-b
            max=max_y+VSTEP+VSTEP-window_height
            scroll_pct=self.scroll_y/max
            viewport_pct=window_height/max_y
            halfheight=range*viewport_pct/2
            
            y0=t+((range-halfheight)*scroll_pct)
            y1=y0+halfheight

        elif self.direction == "horizontal":
            # Calculate percentages for horizontal
            range=window_width-l-r
            max=max_x+HSTEP+HSTEP-window_width
            scroll_pct=self.scroll_x/max
            viewport_pct=window_width/max_x
            halfwidth=(range*viewport_pct)/2
            
            x0=l+(range-halfwidth)*scroll_pct
            x1=x0+halfwidth

            # Vertical is fixed
            y0=window_height-self.thickness-b
            y1=window_height-b
            

        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color)