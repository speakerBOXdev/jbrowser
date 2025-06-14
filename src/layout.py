import tkinter
from tag import *

HSTEP, VSTEP = 12, 18
WIDTH = 800
FONTS = {}
class Layout:
    def __init__(self, nodes):
        self.title="BROWSER"
        self.display_list = []
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.fontsize=14

        self.line = []
        self.istitle=False
        self.recurse(nodes)
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
        
        self.line.append((self.cursor_x, word, font))
        self.cursor_x+= w + sw
        
    def recurse(self, tree):
        if isinstance(tree, Text):
            if self.istitle:
                self.title=tree.text
                return
            for word in tree.text.split():
                self.word(word)
        else:
            self.open_tag(tree.tag)
            for child in tree.children:
                self.recurse(child)
            self.close_tag(tree.tag)

    def open_tag(self, tag):
        if tag=="i":
            self.style="italic"
        elif tag == "b": self.weight="bold"
        elif tag == "em": self.weight="bold"
        elif tag == "small": self.fontsize -= 2
        elif tag == "big": self.fontsize += 4
        elif tag == "h1": self.flush(); self.cursor_y+=VSTEP; self.fontsize+=6
        elif tag == "br": self.flush()
        elif tag == "div": self.flush()
        elif tag == "title":self.istitle=True
    def close_tag(self, tag):
        if tag=="i":
            self.style="roman"
        elif tag == "i": self.style="roman"
        elif tag == "b": self.weight="normal"
        elif tag == "em": self.weight="normal"
        elif tag == "small": self.fontsize += 2
        elif tag == "big": self.fontsize -= 4
        elif tag == "h1": self.fontsize-=6;self.flush(); self.cursor_y+=VSTEP
        elif tag == "div": self.flush(); self.cursor_y+=VSTEP
        elif tag == "p": self.flush(); self.cursor_y+=VSTEP
        elif tag == "li": self.flush(); self.cursor_y+=VSTEP
        elif tag == "title":self.istitle=False
        