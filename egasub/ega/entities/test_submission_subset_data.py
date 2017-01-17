import pytest
from submission_subset_data import SubmissionSubsetData

subsetData = SubmissionSubsetData([2,3],[5,2],[4,3],[5,1],[88,7],[11,3],[44,11],[66,11])

def test_analysis_ids():
    assert [2,3] == subsetData.analysis_ids
    
def test_dac_ids():
    assert [5,2] == subsetData.dac_ids
    
def test_dataset_ids():
    assert [4,3] == subsetData.dataset_ids
    
def test_experiment_ids():
    assert [5,1] == subsetData.experiment_ids
    
def test_policy_ids():
    assert [88,7] == subsetData.policy_ids
    
def test_run_ids():
    assert [11,3] == subsetData.run_ids
    
def test_sample_ids():
    assert [44,11] == subsetData.sample_ids
    
def test_study_ids():
    assert [66,11] == subsetData.study_ids
