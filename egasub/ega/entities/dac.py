
class Dac(object):
    def __init__(self, title, contacts, alias=None, id_=None):
        self.title = title
        self.contacts = contacts
        self.alias = alias
        self.id = id_

    def to_dict(self):
        return {
            'title' : self.title,
            'contacts' :  map(lambda contact: contact.to_dict(), self.contacts),
            'alias': self.alias
        }

    def to_xml(self):
        pass
        