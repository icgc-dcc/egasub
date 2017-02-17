from egasub.ega.entities.submission import Submission
from egasub.ega.entities.submission_subset_data import SubmissionSubsetData

subset = SubmissionSubsetData([2,3],[5,2],[4,34],[54,1],[88,7],[1,3],[44,11],[2,11])
submission = Submission('a title', 'a description', subset)

def test_title():
    assert 'a title' == submission.title

def test_description():
    assert 'a description' == submission.description

def test_subsets():
    assert subset == submission.submission_subset
    
def test_to_dict():
        assert cmp(
        {
            'title' : 'a title',
            'description':'a description',
            'submissionSubset' : subset.to_dict()
        }, submission.to_dict()) == 0
