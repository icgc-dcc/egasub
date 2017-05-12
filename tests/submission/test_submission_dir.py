from egasub.submission import init_submission_dir
import pytest

def test_init_submission_dir(ctx):
    ctx.obj['CURRENT_DIR_TYPE'] = None

    with pytest.raises(TypeError):
        init_submission_dir(ctx,[])

    ctx.obj['CURRENT_DIR_TYPE'] = "variation"

    with pytest.raises(IOError):
        init_submission_dir(ctx,["ssample"])

    assert ctx.obj['LOGGER'].warning.counter == 3

    init_submission_dir(ctx,[""])
    assert ctx.obj['LOGGER'].warning.counter == 4

    init_submission_dir(ctx,["sample_x"])
    assert ctx.obj['LOGGER'].warning.counter == 5

    with pytest.raises(IOError):
        init_submission_dir(ctx,["test_x.lane"])

    init_submission_dir(ctx,["sample"])
    assert ctx.obj['LOGGER'].warning.counter == 6

    init_submission_dir(ctx,["test_$"])
    assert ctx.obj['LOGGER'].warning.counter == 7

    with pytest.raises(IOError):
        init_submission_dir(ctx,["test-x"])

    assert ctx.obj['LOGGER'].warning.counter == 7

    init_submission_dir(ctx,["test x"])
    assert ctx.obj['LOGGER'].warning.counter == 8

    with pytest.raises(IOError):
        init_submission_dir(ctx,["4324_4324"])
    assert ctx.obj['LOGGER'].warning.counter == 8

    print ctx.obj['LOGGER'].warning.counter