from click import echo
from click import prompt
import os
import yaml
import shutil
import click


def init_workspace(ctx,ega_submitter_account=None,ega_submitter_password=None,icgc_id_service_token=None,icgc_project_code=None):
    echo('')
    echo('Initalizing EGA submission workspace...')
    echo('Note: information collected below will be stored in')
    echo('      \'.egasub/config.yaml\' which can be edited later.')
    echo('')
    
    #Ask user input for config.yaml
    if not ega_submitter_account:
        ega_submitter_account = prompt("Enter your EGA submitter account", default='')
    if not ega_submitter_password:
        ega_submitter_password = prompt("Enter your EGA submitter password", default='', hide_input=True)
    if not icgc_id_service_token:
        icgc_id_service_token = prompt("Enter your ICGC ID service token", default='')
    if not icgc_project_code:
        icgc_project_code = prompt("Enter your ICGC project code", default='')
        
    yaml_info = {
        'ega_submitter_account': ega_submitter_account,
        'ega_submitter_password': ega_submitter_password,
        'icgc_id_service_token': icgc_id_service_token,
        'icgc_project_code': icgc_project_code
        }
    
    current_dir = ctx.obj['CURRENT_DIR']
    egasub_dir = os.path.join(current_dir,'.egasub')
    script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    
    if os.access(current_dir, os.W_OK):
        os.mkdir(egasub_dir)
        
        policy_dir = os.path.join(egasub_dir,'policy')
        
        with open(os.path.join(egasub_dir,'config.yaml'),'w') as outfile:
            yaml.safe_dump(yaml_info,outfile,default_flow_style=False)
            
        shutil.copytree(os.path.join(script_dir,"ega","data","policy"),policy_dir)
        echo('EGA submission workspace initialized')
        
    else:
        echo('Permission denied on directory '+current_dir)