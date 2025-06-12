class Tag:
    def __init__(self, tag):
        self.tag=tag
        if " " in self.tag:
            self.tag, attributes = self.tag.split(" ", 1)
        #print("Tag:{}".format(self.tag))

    

class Text:
    def __init__(self, text):
        self.text=text

class Entity:
    def __init__(self, entity):
        self.entity=entity