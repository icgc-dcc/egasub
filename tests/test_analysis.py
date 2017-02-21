from egasub.ega.entities.analysis import Analysis
from egasub.ega.entities.file import File
from egasub.ega.entities.chromosome_reference import ChromosomeReference
from egasub.ega.entities.sample_reference import SampleReference
from egasub.ega.entities.attribute import Attribute

files = [File(32,'file name1','CheckSum1','UnencryptedChecksum1','md5'),
         File(33,'file name2','CheckSum2','UnencryptedChecksum2','md5')]
attributes = [Attribute('The tag 1','The value 1','an unit'),Attribute('The tag 2','The value 2','an unit')]
chromosome_references = [ChromosomeReference('the value1','the label2'),ChromosomeReference('the value2','the label2')]
sample_references = [SampleReference('a value 1','a label 1'),SampleReference('a value 2','a label 2')]

analysis = Analysis('an alias','a title','a description',3,sample_references,'analysis center','analysis date',3,files,attributes,
                    4,chromosome_references,[3,5],'a platform')

def test_title():
    assert 'a title' == analysis.title

def test_description():
    assert 'a description' == analysis.description

def test_study_id():
    assert 3 == analysis.study_id

def test_analysis_center():
    assert 'analysis center' == analysis.analysis_center

def test_analysis_date():
    assert 'analysis date' == analysis.analysis_date

def test_analysis_type_id():
    assert 3 == analysis.analysis_type_id

def test_genome_id():
    assert 4 == analysis.genome_id

def test_experiment_type_id():
    assert [3,5] == analysis.experiment_type_id

def test_platform():
    assert 'a platform' == analysis.platform

def test_files():
    assert files == analysis.files

def test_attributes():
    assert attributes == analysis.attributes

def test_chromosome_references():
    assert chromosome_references == analysis.chromosome_references

def test_sample_references():
    assert sample_references == analysis.sample_references

def test_alias():
    assert 'an alias' == analysis.alias

def test_to_dict():
    assert cmp(
    {
        'title' : 'a title',
        'description':'a description',
        'studyId':3,
        'sampleReferences' : map(lambda ref: ref.to_dict(), sample_references),
        'analysisDate' : 'analysis date',
        'analysisCenter' : 'analysis center',
        'analysisTypeId' : 3,
        'genomeId' : 4,
        'experimentTypeId' : [3,5],
        'platform' : 'a platform',
        'files' : map(lambda file: file.to_dict(), files),
        'attributes' : map(lambda attribute: attribute.to_dict(), attributes),
        'chromosomeReferences' : map(lambda ref: ref.to_dict(), chromosome_references),
        'alias' : 'an alias',
        'status': None
    }, analysis.to_dict()) == 0

