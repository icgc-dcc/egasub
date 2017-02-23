from egasub.ega.entities.contact import Contact

contact = Contact('contact name','contact email','Name of organisation','000-0000')

def test_contact_name():
    assert 'contact name' == contact.contact_name

def test_email():
    assert 'contact email' == contact.email

def test_organisation():
    assert 'Name of organisation' == contact.organisation

def test_phone_number():
    assert '000-0000' == contact.phone_number

def test_to_dict():
    assert cmp({
        'contactName':'contact name',
        'email':'contact email',
        'organisation':'Name of organisation',
        'phoneNumber':'000-0000'},
       contact.to_dict()) == 0