
class DatasetLink(object):
    def __init__(self,label,url):
        self.label = label
        self.url = url

    def to_dict(self):
        return {
            'label' : self.label,
            'url' : self.url
            }

    def to_xml(self):
        pass
    