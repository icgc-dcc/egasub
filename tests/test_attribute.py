from egasub.ega.entities.attribute import Attribute

attribute = Attribute('The tag','The value','an unit')

def test_tag():
    assert 'The tag' == attribute.tag

def test_value():
    assert 'The value' == attribute.value

def test_unit():
    assert 'an unit' == attribute.unit
    
def test_to_dict():
    assert cmp({'tag':'The tag','value':'The value','unit':'an unit'}, attribute.to_dict()) == 0