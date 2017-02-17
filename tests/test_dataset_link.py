from egasub.ega.entities.dataset_link import DatasetLink

link = DatasetLink('the label', 'http://www.example.com')

def test_label():
    assert 'the label' == link.label

def test_url():
    assert 'http://www.example.com' == link.url
    
def test_to_dict():
    assert cmp({'label':'the label','url':'http://www.example.com'}, link.to_dict()) == 0