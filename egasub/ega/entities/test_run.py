import pytest
from run import Run
from file import File

files = [File(1,'file name 1','checksum1','unencryptedchecksum1','md5'),File(2,'file name 2','checksum2','unencryptedchecksum2','md5')]
run = Run(3,2,5,files)

def test_sample_id():
    assert 3 == run.sample_id
    
def test_run_file_type_id():
    assert 2 == run.run_file_type_id
    
def test_experiment_id():
    assert 5 == run.experiment_id
    
def test_files():
    assert files == run.files
    
def test_to_dict():
        assert cmp(
        {
            'sampleId' : 3,
            'runFileTypeId':2,
            'experimentId':5,
            'files' : map(lambda file: file.to_dict(), files)
        }, run.to_dict()) == 0
    