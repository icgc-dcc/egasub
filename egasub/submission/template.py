import os
from click import echo
from shutil import copyfile

def generate_template(ctx,sample_dir):
    if ctx.obj['CURRENT_DIR_TYPE'] == "alignment":
        file_name = "analysis.yaml"
    elif ctx.obj['CURRENT_DIR_TYPE'] == "unaligned":
        file_name = "experiment.yaml"
        
    src_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','..','resources',file_name)
    dest_file = os.path.join(sample_dir,file_name)
    
    if os.path.isfile(dest_file):
        echo("The directory %s already contains the file : %s" % (sample_dir, dest_file))
        ctx.abort()
            
    copyfile(src_file, dest_file)