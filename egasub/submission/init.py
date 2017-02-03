from click import echo
from click import prompt
import os
import yaml
import shutil
import click
import logging


def init_workspace(ctx,ega_submitter_account=None,ega_submitter_password=None,icgc_id_service_token=None,icgc_project_code=None):
    ctx.obj['LOGGER'].info('Initalizing EGA submission workspace...')
    ctx.obj['LOGGER'].info('Note: information collected below will be stored in')
    ctx.obj['LOGGER'].info('      \'.egasub/config.yaml\' which can be edited later.')
    
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
    
    ctx.obj['LOGGER'].info("EGA and ICGC credentials collected")
    
    current_dir = ctx.obj['CURRENT_DIR']
    egasub_dir = os.path.join(current_dir,'.egasub')
    script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    
    if os.access(current_dir, os.W_OK):
        os.mkdir(egasub_dir)
        ctx.obj['LOGGER'].info("Creation of .egasub directory")
        
        policy_dir = os.path.join(egasub_dir,'policy')
        
        with open(os.path.join(egasub_dir,'config.yaml'),'w') as outfile:
            yaml.safe_dump(yaml_info,outfile,default_flow_style=False)
            
        ctx.obj['LOGGER'].info("Credentials added to .egasub/config.yaml file")
            
        shutil.copytree(os.path.join(script_dir,"ega","data","policy"),policy_dir)
        ctx.obj['LOGGER'].info('EGA submission workspace initialized')
        
    else:
        ctx.obj['LOGGER'].critical('Permission denied on directory '+current_dir)