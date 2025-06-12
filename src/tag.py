class Tag:
    def __init__(self, tag):
        self.tag=tag
        self.attr=[]
        if " " in self.tag:
            self.tag, attributes = self.tag.split(" ", 1)
            for attr in attributes.split():
                self.attr.append(attr)

class Text:
    def __init__(self, text):
        self.text=text

class Entity:
    def __init__(self, entity):
        self.entity=entity