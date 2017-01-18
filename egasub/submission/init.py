from click import echo
from click import prompt
import os
import yaml
import shutil

def init_workspace(ctx):
    username = prompt("Enter your EGA username")
    password = prompt("Enter your EGA password",hide_input=True)
    current_dir = ctx.obj['CURRENT_DIR']
    yaml_info = {'username':username,'password':password}
    
    if os.access(current_dir, os.W_OK):
        with open(os.path.join(current_dir,'config.yaml'),'w') as outfile:
            yaml.safe_dump(yaml_info,outfile,default_flow_style=False)
            
        DATA_PATH = os.path.join(current_dir, "icgc", "services")
        print DATA_PATH
        print current_dir
        shutil.copy(DATA_PATH,current_dir)
    
    exit()
    echo('Initalizing EGA submission workspace...')