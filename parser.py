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
            "base", "basefont", "bgsound", "noin_scriptin_script",
            "link", "meta", "title", "style", "script",
        ]
        self.NON_NESTING_TAGS= [ "p", "li"]
        self.scripts = []
        self.state = HTMLParserState()

    def parse(self) -> Element:
        text = ""
        self.state.reset()

        for c in self.body:
            if c == "<":
                if self.state.in_comment:
                    continue
                #if self.state.in_script: text+=c
                if text: 
                    if self.state.in_script: self.add_script(text + c)
                    else: self.add_text(text)
                text = ""
            elif c == ">":
                if self.state.in_comment: 
                    if text.endswith("--"):
                        self.state.in_comment= False
                        text = ""
                    continue
                
                if text == "script":
                    self.state.in_script=True
                    self.add_tag(text)
                    text = ""
                    self.scripts.append(Script())
                    continue
                elif text == "/script":
                    self.state.in_script=False
                    last=self.scripts[-1]
                    script=last.script.strip('<')
                    self.scripts[-1].script=script
                    
                if self.state.in_script: self.add_script(text + c)
                else: self.add_tag(text)
                text = ""
            else:
                text += c
                if text=="!--":
                    self.state.in_comment=True

        if not self.state.in_comment and not self.state.in_tag and text:
            self.add_text(text)
        result = self.finish()
        self.print_scripts()
        return result
    
    def print_scripts(self):
        scripts_length=len(self.scripts)
        print("Found {} scripts.".format(scripts_length))
        if scripts_length == 0: return

        for s in self.scripts:
            print(s.script)

    def add_text(self, text: str):
            if text.isspace(): return
            self.implicit_tags(None)
            parent = self.unfinished[-1]
            node = Text(text, parent)
            parent.children.append(node)
    
    def add_script(self, text: str):
        current = self.scripts[-1]
        current.script+=text
        pass

    def add_tag(self, tag: str):
        if tag.startswith("!"): return
        tag, attributes = self.get_attributes(tag)
        self.implicit_tags(tag)
        if tag.startswith("/"):
            self.add_tag_closed(tag)
        elif tag in SELF_CLOSING_TAGS:
            self.add_tag_closed_self(tag, attributes)
        else:
            self.add_tag_open(tag, attributes)

    def add_tag_open(self, tag: str, attributes):
        parent = self.unfinished[-1] if self.unfinished else None
        self.handle_nested(tag, parent)    
        node = Element(tag, attributes, parent)
        self.unfinished.append(node)
        #print("node {} is now open in parent {}".format(node.tag, tag, parent.tag))
        print("node {} is now open".format(node.tag, tag))
        if tag == "script": self.state.in_script=True

    def add_tag_closed_self(self, tag: str, attributes):
        parent = self.unfinished[-1]
        node = Element(tag, attributes, parent)
        parent.children.append(node)
        print("node {} is now closed by self".format(node.tag, tag))
        if tag == "/script": self.state.in_script=False

    def add_tag_closed(self, tag):
        if len(self.unfinished) == 1: return
        node = self.unfinished.pop()
        parent = self.unfinished[-1]
        parent.children.append(node)
        #print("node {} is now closed by {} in parent {}".format(node.tag, tag, parent.tag))
        print("node {} is now closed by {}".format(node.tag, tag))

    def handle_nested(self, tag: str, parent):
        if parent == None:
            return
        if tag in self.NON_NESTING_TAGS and parent.tag == tag:
            self.add_tag("/{}".format(tag))

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
    
    def finish(self) -> Element:
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



class HTMLParserState:
    def __init__(self):
        self._in_tag = False
        self._in_comment = False
        self._in_script = False

    @property
    def in_tag(self):
        return self._in_tag

    @in_tag.setter
    def in_tag(self, value: bool):
        self._in_tag = value

    @property
    def in_comment(self):
        return self._in_comment
    
    @in_comment.setter
    def in_comment(self, value: bool):
        self._in_comment = value

    @property
    def in_script(self):
        return self._in_script
    
    @in_script.setter
    def in_script(self, value: bool):
        #if self._in_script == value: return
        print("changing - in_script:{} -> {}".format(self._in_script, value))
        self._in_script = value
        print("changed - in_script:{}".format(self._in_script))

    def reset(self):
        self.in_tag = False
        self.in_comment = False
        self.in_script = False