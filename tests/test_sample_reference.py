from egasub.ega.entities.sample_reference import SampleReference

reference = SampleReference('a value','a label')

def test_value():
    assert 'a value' == reference.value

def test_label():
    assert 'a label' == reference.label
    
def test_to_dict():
    assert cmp({'value':'a value','label':'a label'}, reference.to_dict()) == 0 