
from egasub.utils import initialize_app, initialize_log, get_current_dir_type, get_settings, find_workspace_root

import pytest
import os

def test_initialize_app(ctx, mock_server):
    with pytest.raises(KeyError):
        initialize_app(ctx)

    #ctx.obj['WORKSPACE_PATH'] = "tests/data/workspace/"
    #ctx.obj['CURRENT_DIR'] = 'tests/data/workspace/'
    #ctx.obj['WORKSPACE_PATH']['SETTINGS'] =

    #with pytest.raises(Exception):
    #    initialize_app(ctx)

    #ctx.obj['CURRENT_DIR'] = ""

def test_initialize_log(ctx):
    ctx.obj['WORKSPACE_PATH'] = None
    initialize_log(ctx, True, "info")
    ctx.obj['WORKSPACE_PATH'] = "tests/data/workspace/"
    initialize_log(ctx, True, "info")

def test_get_current_dir_type(ctx):
    #ctx.obj['CURRENT_DIR'] = None
    #ctx.obj['WORKSPACE_PATH'] = None
    with pytest.raises(KeyError):
        get_current_dir_type(ctx)

    ctx.obj['WORKSPACE_PATH'] = ""

    with pytest.raises(KeyError):
        get_current_dir_type(ctx)

    ctx.obj['CURRENT_DIR'] = ""
    print get_current_dir_type(ctx)
    assert get_current_dir_type(ctx) == None

    workspace = "test"
    ctx.obj['WORKSPACE_PATH'] = workspace

    ctx.obj['CURRENT_DIR'] = "%s/alignment.20170115" % workspace
    assert get_current_dir_type(ctx) == "alignment"

    ctx.obj['CURRENT_DIR'] = "%s/alignment.test" % workspace
    assert get_current_dir_type(ctx) == "alignment"

    ctx.obj['CURRENT_DIR'] = "%s/unaligned.test" % workspace
    assert get_current_dir_type(ctx) == "unaligned"

    ctx.obj['CURRENT_DIR'] = "%s/variation.test" % workspace
    assert get_current_dir_type(ctx) == "variation"

    ctx.obj['CURRENT_DIR'] = "%s/variations.test" % workspace
    assert get_current_dir_type(ctx) == None


def test_get_settings():
    assert get_settings("") == None
    settings = get_settings("tests/data/workspace")

    assert settings['ega_submitter_account'] == "dummy-account"
    assert settings['icgc_id_service_token'] == 'fake-token'
    assert settings['ega_submitter_password'] == 'change-me'
    assert settings['icgc_project_code'] == 'PACA-CA'
    assert settings['ega_submitter_account'] != "dummy-test"
    assert settings['icgc_id_service_token'] != 'fake-test'
    assert settings['ega_submitter_password'] != 'change-test'
    assert settings['icgc_project_code'] != 'PACA-TEST'

def test_find_workspace_root():
    workspace_root = "tests/data/workspace"
    assert find_workspace_root() == None
    assert find_workspace_root(workspace_root) == workspace_root
    assert find_workspace_root(os.path.join(workspace_root,"test")) == workspace_root