from egasub.ega.services import login,logout,prepare_submission, query_by_id, api_url, query_by_type, _obj_type_to_endpoint, object_submission, register_obj,validate_obj, _validate_submit_obj, update_obj, delete_obj, submit_submission
import pytest
import requests
from egasub.ega.entities.submission_subset_data import SubmissionSubsetData
from egasub.ega.entities.submission import Submission
from egasub.exceptions import CredentialsError
from egasub.submission.submittable import Unaligned, Variation
import os


def test_login_function(ctx, mock_server):
    with pytest.raises(CredentialsError):
        login(ctx)

    ctx.obj['SETTINGS']['ega_submitter_account'] = 'test_account'

    with pytest.raises(CredentialsError):
        login(ctx)

    ctx.obj['SETTINGS']['ega_submitter_password'] = 'test_password'

    assert login(ctx) is None
    assert not ctx.obj['SUBMISSION']['sessionToken'] == None
    assert ctx.obj['SUBMISSION']['sessionToken'] == "abcdefg"

def test_prepare_submission(ctx):
    requests.post("%ssubmissions" % (ctx.obj['SETTINGS']['apiUrl']))

    subset = SubmissionSubsetData([2,3],[5,2],[4,34],[54,1],[88,7],[1,3],[44,11],[2,11])
    submission = Submission('a title', 'a description', subset)

    assert prepare_submission(ctx,submission) is None
    assert ctx.obj['SUBMISSION']['id'] == "12345"

def test_api_url(ctx):
    assert api_url(ctx) == "http://example.com/"
    del ctx.obj['SETTINGS']['apiUrl']
    assert api_url(ctx) == "https://ega.crg.eu/submitterportal/v1/"
    ctx.obj['SETTINGS']['apiUrl'] = "http://example.com/"

def test_query_by_id(ctx, mock_server):
    result = query_by_id(ctx,'sample','sample_alias','ALIAS')
    assert result[0].get('id') == '12345'

    result = query_by_id(ctx,'study','test_alias','ALIAS')
    assert result[0].get('id') == '12345'

    result = query_by_id(ctx,'dataset','dataset_alias','ALIAS')
    assert result[0].get('id') == '12345'

    result = query_by_id(ctx,'policy','policy_alias','ALIAS')
    assert result[0].get('id') == '12345'

def test_query_by_type(ctx, mock_server):
    result = query_by_type(ctx, 'sample', "SUBMITTED")
    assert result[0].get('id') == '12345'

    result = query_by_type(ctx, 'study', "SUBMITTED")
    assert result[0].get('id') == '12345'

    result = query_by_type(ctx, 'dataset', "SUBMITTED")
    assert result[0].get('id') == '12345'

    result = query_by_type(ctx, 'policy', "SUBMITTED")
    assert result[0].get('id') == '12345'

def test_obj_type_to_endpoint():
    assert _obj_type_to_endpoint("dataset") == "datasets"
    assert _obj_type_to_endpoint("sample") == "samples"
    assert _obj_type_to_endpoint("policy") == "policies"

    with pytest.raises(Exception):
        _obj_type_to_endpoint("test")

def test_logout_function(ctx):
    logout(ctx)

    with pytest.raises(KeyError):
        logout(ctx)

    assert not 'sessionToken' in ctx.obj['SUBMISSION']

def test_register_obj(ctx):
    current = os.getcwd()
    os.chdir(os.path.join(current, 'tests/data/workspace/submittable'))
    ctx.obj['SUBMISSION']['id'] = "12345"
    ctx.obj['SUBMISSION']['sessionToken'] = "sdfsd"
    register_obj(ctx, Unaligned('test_u').sample, 'sample')
    os.chdir(current)

def test_submit_submission(ctx):
    current = os.getcwd()
    os.chdir(os.path.join(current,'tests/data/workspace/submittable'))
    ctx.obj['SUBMISSION']['id'] = "12345"
    ctx.obj['SUBMISSION']['sessionToken'] = "sdfsd"
    assert submit_submission(ctx, Unaligned('test_u').sample) is None
    #ctx.obj['SUBMISSION']['id'] = None
    os.chdir(current)

# def test_validate_submit_obj(ctx):
#     current = os.getcwd()
#     os.chdir(os.path.join(os.getcwd(), 'tests/data/workspace/submittable/'))
#     variation = Variation('test_v')
#     variation.id = 555
#     _validate_submit_obj(ctx, variation, 'analysis','submit')
#     pass
#     os.chdir(current)