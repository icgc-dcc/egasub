
class CustomTag(object):
    def __init__(self,tag, value):
        self.tag=tag
        self.value=value

    def to_dict(self):
        return {
            'tag' : self.tag,
            'value' : self.value
            }

    def to_xml(self):
        pass