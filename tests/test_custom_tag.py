from egasub.ega.entities.custom_tag import CustomTag

tag = CustomTag('tag1', 'value1')

def test_tag():
    assert 'tag1' == tag.tag

def test_value():
    assert 'value1' == tag.value

def to_dict():
    assert cmp({'tag':'tag1','value':'value1'}, tag.to_dict()) == 0