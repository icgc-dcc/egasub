from egasub.ega.entities.submission_subset_data import SubmissionSubsetData

subset_data = SubmissionSubsetData([2,3],[5,2],[4,3],[5,1],[88,7],[11,3],[44,11],[66,11])

def test_analysis_ids():
    assert [2,3] == subset_data.analysis_ids

def test_dac_ids():
    assert [5,2] == subset_data.dac_ids

def test_dataset_ids():
    assert [4,3] == subset_data.dataset_ids

def test_experiment_ids():
    assert [5,1] == subset_data.experiment_ids

def test_policy_ids():
    assert [88,7] == subset_data.policy_ids

def test_run_ids():
    assert [11,3] == subset_data.run_ids

def test_sample_ids():
    assert [44,11] == subset_data.sample_ids

def test_study_ids():
    assert [66,11] == subset_data.study_ids

def test_to_dict():
        assert cmp(
        {
            'analysisIds' : [2,3],
            'dacIds':[5,2],
            'datasetIds' : [4,3],
            'experimentIds' : [5,1],
            'policyIds' : [88,7],
            'runIds' : [11,3],
            'sampleIds' : [44,11],
            'studyIds' : [66,11]
        }, subset_data.to_dict()) == 0
        