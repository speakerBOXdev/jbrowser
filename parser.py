from tag import *
SELF_CLOSING_TAGS = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]

class HTMLParser:
    def __init__(self, body: str):
        self.body = body
        self.unfinished = []
        self.HEAD_TAGS = [
            "base", "basefont", "bgsound", "noscript",
            "link", "meta", "title", "style", "script",
        ]


    def parse(self):
        text = ""
        in_tag = False
        is_comment = False
        for c in self.body:
            if c == "<":
                if is_comment:
                    continue
                in_tag = True
                if text: self.add_text(text)
                text = ""
            elif c == ">":
                if is_comment: 
                    if text.endswith("--"):
                        is_comment= False
                        text = ""
                    continue
                in_tag = False
                self.add_tag(text)
                text = ""
            else:
                text += c
                if text=="!--":
                    is_comment=True

        if not is_comment and not in_tag and text:
            self.add_text(text)
        return self.finish()
    
    def add_text(self, text: str):
            if text.isspace(): return
            self.implicit_tags(None)
            parent = self.unfinished[-1]
            node = Text(text, parent)
            parent.children.append(node)
    
    def add_tag(self, tag: str):
        if tag.startswith("!"): return
        tag, attributes = self.get_attributes(tag)
        self.implicit_tags(tag)
        if tag.startswith("/"):
            if len(self.unfinished) == 1: return
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
            print("node {} is now closed by {} in parent {}".format(node.tag, tag, parent.tag))
        elif tag in SELF_CLOSING_TAGS:
            parent = self.unfinished[-1]
            node = Element(tag, attributes, parent)
            parent.children.append(node)
        else:
            parent = self.unfinished[-1] if self.unfinished else None
            self.handle_nested(tag, parent)    
            node = Element(tag, attributes, parent)
            self.unfinished.append(node)

    def handle_nested(self, tag: str, parent):
        if parent == None:
            return
        if tag == "p" and parent.tag == "p":
            self.add_tag("/p")
        if tag == "li" and parent.tag == "li":
            self.add_tag("/li")

    def get_attributes(self, text: str):
        parts = text.split()
        tag = parts[0].casefold()
        attributes = {}
        for attrpair in parts[1:]:
            if "=" in attrpair:
                key, value = attrpair.split("=", 1)
                attributes[key.casefold()] = value
                if len(value) > 2 and value[0] in ["'", "\""]:
                    value = value[1:-1]
            else:
                attributes[attrpair.casefold()] = ""
        return tag, attributes
    
    def finish(self):
        if not self.unfinished:
            self.implicit_tags(None)
        while len(self.unfinished) > 1:
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        return self.unfinished.pop()
    
    def implicit_tags(self, tag: str):
        while True:
            open_tags = [node.tag for node in self.unfinished]
            if open_tags == [] and tag != "html":
                self.add_tag("html")
            elif open_tags == ["html"] and tag not in ["head", "body", "/html"]:
                if tag in self.HEAD_TAGS:
                    self.add_tag("head")
                else:
                    self.add_tag("body")
            elif open_tags == ["html", "head"] and tag not in ["/head"] + self.HEAD_TAGS:
                self.add_tag("/head")
            else:
                break