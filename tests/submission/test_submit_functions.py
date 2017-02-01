import os, yaml
from egasub.ega.services import login,logout,prepare_submission, submit_obj
import pytest
import requests
from egasub.ega.entities.submission_subset_data import SubmissionSubsetData
from egasub.ega.entities.submission import Submission
from egasub.ega.entities.study import Study


def test_login_function(ctx, mock_server):
    # Login test
    ctx.obj['SETTINGS']['ega_submitter_account'] = 'account'
    ctx.obj['SETTINGS']['ega_submitter_password'] = 'password'
    login(ctx)
    assert ctx.obj['SUBMISSION']['sessionToken'] == "abcdefg"

def test_prepare_submission(ctx):    
    response = requests.post("%ssubmissions" % (ctx.obj['SETTINGS']['apiUrl']))
    
    subset = SubmissionSubsetData([2,3],[5,2],[4,34],[54,1],[88,7],[1,3],[44,11],[2,11])
    submission = Submission('a title', 'a description', subset)
    
    prepare_submission(ctx,submission)
    assert ctx.obj['SUBMISSION']['id'] == "12345"
    
def test_submit_obj(ctx):
    study = Study(
            "test_alias", # alias
            1, # studyTypeId
            'Short study name', # should take it from config
            'Study title', # should take it from config
            'Study abstract', # should take it from config
            None,  # ownTerm
            [],  # pubMedIds
            [],   # customTags
            None
        )
    submit_obj(ctx,study,"study")
        
def test_logout_function(ctx):
    logout(ctx)
    assert not 'sessionToken' in ctx.obj['SUBMISSION']