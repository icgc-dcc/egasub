import unittest
from dac import Dac

class DacTest(unittest.TestCase):
    def test_to_dict(self):
        dac = Dac(
            'Dac title',
            [
                {
                    'contactName':'Contact #1',
                    'email':'contact1@example.com',
                    'organisation' : "Dac organisation",
                    'phoneNumber' : "(000) 000-0000"
                },
                {
                    'contactName':'Contact #2',
                    'email':'contact2@example.com',
                    'organisation' : "Dac organisation",
                    'phoneNumber' : "(000) 000-0000"
                },
                {
                    'contactName':'Contact #3',
                    'email':'contact3@example.com',
                    'organisation' : "Dac organisation",
                    'phoneNumber' : "(000) 000-0000"
                }
            ]
        )
        self.assertDictEqual(dac.to_dict(), d2, msg)
    
dac = Dac(
    'Dac title',
    [
        {
            'contactName':'Contact #1',
            'email':'contact1@example.com',
            'organisation' : "Dac organisation",
            'phoneNumber' : "(000) 000-0000"
        },
        {
            'contactName':'Contact #2',
            'email':'contact2@example.com',
            'organisation' : "Dac organisation",
            'phoneNumber' : "(000) 000-0000"
        },
        {
            'contactName':'Contact #3',
            'email':'contact3@example.com',
            'organisation' : "Dac organisation",
            'phoneNumber' : "(000) 000-0000"
        }
    ]
)

print dac.__dict__