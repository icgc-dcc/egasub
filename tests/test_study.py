from egasub.ega.entities.study import Study
from egasub.ega.entities.custom_tag import CustomTag

tags = [CustomTag('tag1','value1'),CustomTag('tag2','value2')]
study = Study('an alias',33,'Short name','the title','the abstract','own term',[1,2,3],tags,'my_study')

def test_study_type_id():
    assert 33 == study.study_type_id

def test_short_name():
    assert 'Short name' == study.short_name

def test_title():
    assert 'the title' == study.title

def test_study_abstract():
    assert 'the abstract' == study.study_abstract

def test_own_term():
    assert 'own term' == study.own_term
    
def test_pub_med_ids():
    assert [1,2,3] == study.pub_med_ids
    
def test_tags():
    assert tags == study.custom_tags
    
def test_to_dict():
        assert cmp(
        {
            'studyTypeId' : 33,
            'shortName':'Short name',
            'title':'the title',
            'studyAbstract' : 'the abstract',
            'ownTerm' : 'own term',
            'pubMedIds' : [1,2,3],
            'customTags' : map(lambda tag: tag.to_dict(), study.custom_tags),
            'alias' : 'an alias',
            'id': 'my_study'
        }, study.to_dict()) == 0
        
def test_alias():
    assert 'an alias' == study.alias