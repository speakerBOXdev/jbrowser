from tag import *

class HTMLParser:
    def __init__(self, body):
        self.body = body
        self.unfinished = []

    def parse(self):
        out = []
        buffer = ""
        in_tag = False
        in_entity = False
        
        for c in self.body:
            if c == "<":
                in_tag = True
                if buffer: out.append(Text(buffer, None))
                buffer = ""
            elif c == ">":
                in_tag = False
                out.append(Element(buffer, None))
                buffer = ""
            elif c == "&":
                in_entity = True
            elif c == ";":
                in_entity = False
                out.append(Entity(buffer))
                buffer = ""
            else:
            #elif not in_tag:
                buffer+=c

        if not in_tag and buffer:
            out.append(Text(buffer, None))
        return out
