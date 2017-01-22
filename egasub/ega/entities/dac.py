
class Dac(object):
    
    def __init__(self, title, contacts):
        self.title = title
        self.contacts = contacts

        
    def to_dict(self):
        return {
            'title' : self.title,
            'contacts' :  map(lambda contact: contact.to_dict(), self.contacts)
        }


    def to_xml(self):
        pass
        