import pytest

from egasub.ega.entities.dac import Dac
from egasub.ega.entities.contact import Contact

contacts = [Contact('name 1','email 1','organisation 1','000-0000'),Contact('name 2','email 2',' organisation 2','000-0000')]
dac = Dac('a title',contacts)

def test_title():
    assert 'a title' == dac.title
    
def test_contacts():
        assert cmp(
        {
            'title' : 'a title',
            'contacts' : map(lambda contact: contact.to_dict(), contacts)
        }, dac.to_dict()) == 0
