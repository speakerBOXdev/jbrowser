import tkinter
from tag import *

HSTEP, VSTEP = 12, 18
WIDTH = 800
FONTS = {}
class Layout:
    def __init__(self, tokens):
        self.display_list = []

        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.fontsize=14

        self.line = []

        for tok in tokens:
            self.token(tok)
        self.flush()

    def flush(self):
        if not self.line: return
        metrics = [font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent
        self.cursor_x = HSTEP
        self.line = []

    def get_font(self, size, weight, style):
        key = (size, weight, style)
        if key not in FONTS:
            font = tkinter.font.Font(size=size, weight=weight,
                slant=style)
            label = tkinter.Label(font=font)
            FONTS[key] = (font, label)
        return FONTS[key][0]

    def word(self, word):
        font = self.get_font(self.fontsize, self.weight, self.style)
        sw=font.measure(" ")
        w = font.measure(word)
        cursor_x=self.cursor_x + w + sw
        if cursor_x > WIDTH - HSTEP:
            self.flush()
        
        self.line.append((self.cursor_x, word, font))
        self.cursor_x+= w + sw
        
    def entity(self, entity):
        font = self.get_font(self.fontsize, self.weight, self.style)
        sw=font.measure(" ")
        entityVal=self.get_entity_val(entity)
        w = font.measure(entityVal)
        
        cursor_x=self.cursor_x + w + sw
        if cursor_x > WIDTH - HSTEP:
            self.flush()

        self.display_list.append((self.cursor_x, self.cursor_y, entityVal, font))
        self.cursor_x+= w + sw
        
        
    def token(self, tok):
        if isinstance(tok, Text):
            for word in tok.text.split():
                self.word(word)
        # if isinstance(tok, Entity):
        #     self.entity(tok.entity)
        elif isinstance(tok, Tag):
            if tok.tag == "i": self.style="italic"
            elif tok.tag == "/i": self.style="roman"
            elif tok.tag == "b": self.weight="bold"
            elif tok.tag == "/b": self.weight="normal"
            elif tok.tag == "em": self.weight="bold"
            elif tok.tag == "/em": self.weight="normal"
            elif tok.tag == "small": self.fontsize -= 2
            elif tok.tag == "/small": self.fontsize += 2
            elif tok.tag == "big": self.fontsize += 4
            elif tok.tag == "/big": self.fontsize -= 4
            elif tok.tag == "br": 
                self.flush()
            elif tok.tag == "br/": 
                self.flush()
            elif tok.tag == "br /": 
                self.flush()
            elif tok.tag == "div": 
                self.flush()
            elif tok.tag == "/div": 
                self.flush()
                self.cursor_y+=VSTEP
            elif tok.tag == "/p":
                self.flush()
                self.cursor_y+=VSTEP
            elif tok.tag == "/li":
                self.flush()
                self.cursor_y+=VSTEP