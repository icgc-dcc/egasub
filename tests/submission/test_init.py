from click.testing import CliRunner
import click
from egasub.submission.init import init_workspace, truncate_string, make_dummy_dac, make_dummy_policy, initialize_dac_policy_study
from egasub.ega.entities import Dac, Policy, EgaEnums
import pytest
import mock
import __builtin__
#from fabric.api import run, settings, prompt


def test_init_function(ctx):
    runner = CliRunner()
    with runner.isolated_filesystem():
        #init_workspace(ctx,'test_account','test_password','test_token','PACA-CA')
        print ctx.obj
        #result = runner.invoke(main,['init','--ega_submitter_account','test_account','--ega_submitter_password','test_password','--icgc_id_service_token','test_token','--icgc_project_code','PACA-CA'])
        #assert not result.exception
        #assert os.path.isdir('.egasub')
        #assert os.path.isdir('.egasub/policy')
        #assert os.path.exists('.egasub/policy/ICGC_Policy.xml')
        #yaml_config_file = '.egasub/config.yaml'
        #assert os.path.exists(yaml_config_file)

        #yaml_config = yaml.load(file(yaml_config_file,'r'))
        #assert yaml_config['ega_submitter_account'] == "test_account"
        #assert yaml_config['ega_submitter_password'] == "test_password"
        #assert yaml_config['icgc_id_service_token'] == "test_token"
        #assert yaml_config['icgc_project_code'] == "PACA-CA"


def test_truncate_string():
    assert truncate_string("12345", 4) == "1234..."
    assert truncate_string("12345", 5) == "12345"

def test_make_dummy_dac():
    assert isinstance(make_dummy_dac(), Dac)

def test_make_dummy_policy():
    assert isinstance(make_dummy_policy(make_dummy_dac()), Policy)

def test_init_workspace(ctx, mock_server):
    runner = CliRunner()
    ctx.obj['SETTINGS']['ega_submitter_account'] = 'test_account'
    ctx.obj['SETTINGS']['ega_submitter_password'] = 'test_password'
    ctx.obj['EGA_ENUMS'] = EgaEnums()
    ctx.obj['SETTINGS']['ega_policy_id'] = 'test_id'


    #with pytest.raises(IOError):
    #init_workspace.input = lambda: '1'
    #with settings(prompts = {'Select an existing study by entering the line number or enter 0 to create a new study: ': '1'}):
        #run('apt-get update')
        #   run('apt-get upgrade')

    runner.invoke(init_workspace,['study_key', '1'])



    ctx.obj['SETTINGS']['ega_submitter_account'] = None
    ctx.obj['SETTINGS']['ega_submitter_password'] = None
    ctx.obj['SETTINGS']['ega_policy_id'] = None

def test_initialize_dac_policy_study(ctx):
    ctx.obj['SETTINGS']['ega_submitter_account'] = None
    ctx.obj['SETTINGS']['ega_submitter_password'] = None
    ctx.obj['SETTINGS']['ega_policy_id'] = None
    #initialize_dac_policy_study(ctx, )
    pass