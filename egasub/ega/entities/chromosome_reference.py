
class ChromosomeReference(object):
    def __init__(self,value,label=None):
        self.value=value
        self.label=label

    def to_dict(self):
        return {
            'value' : self.value,
            'label' : self.label
            }

    def to_xml(self):
        pass