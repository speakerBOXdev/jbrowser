class Element:
    def __init__(self, tag, parent):
        self.tag=tag
        self.children=[]
        self.parent=parent
        self.attr=[]
        if " " in self.tag:
            self.tag, attributes = self.tag.split(" ", 1)
            for attr in attributes.split():
                self.attr.append(attr)

class Text:
    def __init__(self, text, parent):
        self.text=text
        self.parent=parent

class Entity:
    def __init__(self, entity):
        self.entity=entity