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

def test_to_xml():
    assert attribute.to_xml() == '<TAG>The tag</TAG>\n<VALUE>The value</VALUE>\n<UNIT>an unit</UNIT>\n'

def test_from_dict():
    a = attribute.from_dict(attribute.to_dict())
    assert attribute.to_xml() == a.to_xml()
    assert attribute.tag == a.tag
    assert attribute.value == a.value
    assert attribute.unit == a.unit