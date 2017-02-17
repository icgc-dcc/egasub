

class Contact(object):
    def __init__(self,contact_name,email,organisation,phone_number):
        self.contact_name = contact_name
        self.email = email
        self.organisation = organisation
        self.phone_number = phone_number

    def to_dict(self):
        return {
            'contactName' : self.contact_name,
            'email' : self.email,
            'organisation' : self.organisation,
            'phoneNumber' : self.phone_number
            }

    def to_xml(self):
        pass