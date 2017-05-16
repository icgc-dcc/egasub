from egasub.submission.submit import submittable_status, submit_dataset, perform_submission
from egasub.ega.services import logout
from egasub.ega.entities.ega_enums import EgaEnums
import pytest
import os
import shutil
from egasub.submission.submittable import Unaligned

def test_submittable_status():
    assert submittable_status("fail") == None
    assert submittable_status("tests/submission/test_submit.py") == ['']

def test_perform_submission(ctx, mock_server):

    ctx.obj['SETTINGS']['ega_submitter_account'] = 'test_account'
    ctx.obj['SETTINGS']['ega_submitter_password'] = 'test_password'
    ctx.obj['SETTINGS']['ega_policy_id'] = 'test_id'
    ctx.obj['CURRENT_DIR'] = os.path.join('tests/data/workspace/Unaligned.20170110/ssample_y')
    ctx.obj['CURRENT_DIR_TYPE'] = "unaligned"
    ctx.obj['EGA_ENUMS'] = EgaEnums()
    ctx.obj['log_file'] = 'tests/data/workspace/unaligned.20170110/ssample_y/.status'
    
    #perform_submission(ctx, '///')

    initial_directory = os.getcwd()
    os.chdir('tests/data/workspace/unaligned.20170110/')

    unaligned = Unaligned('ssample_y')

    unaligned.record_object_status('sample', True, "test", "test")

    with pytest.raises(Exception):
        perform_submission(ctx, ['ssample_y'])

    shutil.rmtree(os.path.join(os.getcwd(), 'ssample_y/.status'))
    os.chdir(initial_directory)


def test_submit_dataset(ctx, mock_server):
    #with pytest.raises(AttributeError):
        #submit_dataset(ctx)

    #with pytest.raises(AttributeError):
    #submit_dataset(ctx)

    ctx.obj['SETTINGS']['ega_submitter_account'] = None
    ctx.obj['SETTINGS']['ega_submitter_password'] = None
    ctx.obj['SETTINGS']['ega_policy_id'] = None
    ctx.obj['CURRENT_DIR'] = None
    ctx.obj['EGA_ENUMS'] = None






