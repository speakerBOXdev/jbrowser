class Element:
    def __init__(self, tag: str, attributes, parent):
        self.tag=tag
        self.attributes=attributes
        self.children=[]
        self.parent=parent
        
    def __repr__(self):
        return "<" + self.tag + ">"

class Text:
    def __init__(self, text, parent):
        self.text=text
        self.parent=parent
        self.children=[]
    def __repr__(self):
        return repr(self.text)

class Entity:
    def __init__(self, entity):
        self.entity=entity

class Script:
    def __init__(self):
        self.script = ""