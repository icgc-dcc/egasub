
from egasub.submission.init_submission_dir import init_submission_dir
import pytest

def test_alignment(ctx):
    submission_dirs = ['test_1','test_2']
    ctx.obj['CURRENT_DIR_TYPE'] = "alignme"
    ctx.obj['CURRENT_DIR_TYPE'] = "alignment"
    with pytest.raises(IOError):
        init_submission_dir(ctx,submission_dirs)

    submission_dirs = [""]
    init_submission_dir(ctx,submission_dirs)

def test_unaligned(ctx):
    submission_dirs = ['test_1','test_2']
    ctx.obj['CURRENT_DIR_TYPE'] = "unalign"
    ctx.obj['CURRENT_DIR_TYPE'] = "unaligned"
    with pytest.raises(IOError):
        init_submission_dir(ctx,submission_dirs)

    submission_dirs = [""]
    init_submission_dir(ctx,submission_dirs)
    
def test_variation(ctx):
    submission_dirs = ['test_1','test_2']
    ctx.obj['CURRENT_DIR_TYPE'] = "variati"
    
    ctx.obj['CURRENT_DIR_TYPE'] = "variation"
    with pytest.raises(IOError):
        init_submission_dir(ctx,submission_dirs)
        
    submission_dirs = [""]
    init_submission_dir(ctx,submission_dirs)