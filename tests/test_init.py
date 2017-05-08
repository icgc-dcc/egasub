from click.testing import CliRunner
from egasub.submission.init import truncate_string

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