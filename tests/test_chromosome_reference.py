from egasub.ega.entities.chromosome_reference import ChromosomeReference

reference = ChromosomeReference('the value','the label')

def test_value():
    assert 'the value' == reference.value

def test_label():
    assert 'the label' == reference.label

def to_dict():
    assert cmp({'value':'the value','label':'the label'}, reference.to_dict()) == 0