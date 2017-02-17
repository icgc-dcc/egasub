from egasub.ega.entities.experiment import Experiment

experiment = Experiment('an alias','The title of the experiment',2,4,3,5,'Description of the design','Library name','Library construction protocol',3,4,5,1022,3000,22)
experiment_to_dict = {
        'title' : 'The title of the experiment',
        'instrumentModelId' : 2,
        'librarySourceId' : 4,
        'librarySelectionId' : 3,
        'libraryStrategyId' : 5,
        'designDescription' : 'Description of the design',
        'libraryName' : 'Library name',
        'libraryConstructionProtocol' : 'Library construction protocol',
        'libraryLayoutId' : 3,
        'pairedNominalLength' : 4,
        'pairedNominalSdev' : 5,
        'sampleId' : 1022,
        'studyId' : 3000,
        'alias' : 'an alias',
        'id' : 22,
        'status': None
    }

def test_title():
    assert 'The title of the experiment' == experiment.title

def test_instrument_model_id():
    assert 2 == experiment.instrument_model_id
    
def test_library_source_id():
    assert 4 == experiment.library_source_id
    
def test_library_selection_id():
    assert 3 == experiment.library_selection_id
    
def test_library_strategy_id():
    assert 5 == experiment.library_strategy_id
    
def test_design_description():
    assert 'Description of the design' == experiment.design_description
    
def test_library_name():
    assert 'Library name' == experiment.library_name
    
def test_library_construction_protocol():
    assert 'Library construction protocol' == experiment.library_construction_protocol
    
def test_library_layout_id():
    assert 3 == experiment.library_layout_id
    
def test_paired_nominal_length():
    assert 4 == experiment.paired_nominal_length
    
def test_paired_nominal_sdev():
    assert 5 == experiment.paired_nominal_sdev
    
def test_sample_id():
    assert 1022 == experiment.sample_id
    
def test_study_id():
    assert 3000 == experiment.study_id
    
def test_to_dict():
    assert cmp(experiment_to_dict, experiment.to_dict()) == 0
    
def test_alias():
    assert 'an alias' == experiment.alias
    
def test_id():
    assert 22 == experiment.id
    