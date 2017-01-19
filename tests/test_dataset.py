from egasub.ega.entities.dataset import Dataset
from egasub.ega.entities.dataset_link import DatasetLink
from egasub.ega.entities.attribute import Attribute

links = [DatasetLink('label 1','url1'),DatasetLink('label 2','url2')]
attributes = [Attribute('The tag 1','The value 1','an unit'),Attribute('The tag 2','The value 2','an unit')]


dataset = Dataset('an alias',[3,4,5],3,[6,1,4],[8,21,4],'a title',links,attributes)


def test_dataset_type_ids():
    assert [3,4,5] == dataset.dataset_type_ids
    
def test_policy_id():
    assert 3 == dataset.policy_id
    
def test_runs_references():
    assert [6,1,4] == dataset.runs_references
    
def test_analysis_references():
    assert [8,21,4] == dataset.analysis_references
    
def test_dataset_links():
    assert links == dataset.dataset_links
    
def test_attributes():
    assert attributes == dataset.attributes
    
def test_to_dict():
    assert cmp(
        {
            'title' : 'a title',
            'datasetTypeIds':[3,4,5],
            'policyId':3,
            'runsReferences' : [6,1,4],
            'analysisReferences' : [8,21,4],
            'datasetLinks' : map(lambda dataset_link: dataset_link.to_dict(), links),
            'attributes' : map(lambda attribute: attribute.to_dict(), attributes),
            'alias' : 'an alias'
        }, dataset.to_dict()) == 0
        
def test_alias():
    assert 'an alias' == dataset.alias