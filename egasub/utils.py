import os
import re
import yaml
import glob
import ftplib
from click import echo
from egasub.ega.entities.file import File



def initialize_app(ctx):
    if not ctx.obj['WORKSPACE_PATH']:
        echo('Error: not in an EGA submission workspace! Please run "egasub init" to initiate an EGA workspace.', err=True)
        ctx.abort()
    else:
        echo('Info: workspace is \'%s\'' % ctx.obj['WORKSPACE_PATH'])

    # read the settings
    ctx.obj['SETTINGS'] = get_settings(ctx.obj['WORKSPACE_PATH'])
    if not ctx.obj['SETTINGS']:
        echo('Error: unable to read config file, or config file invalid!', err=True)
        ctx.abort()

    # figure out the current dir type, e.g., study, sample or analysis
    ctx.obj['CURRENT_DIR_TYPE'] = get_current_dir_type(ctx)
    echo('Info: submission data type is \'%s\'' % ctx.obj['CURRENT_DIR_TYPE'])
    if not ctx.obj['CURRENT_DIR_TYPE']:
        echo('Error: the current working directory does not associate with any supported EGA data types: unaligned|alignment|variation', err=True)
        ctx.abort()


def find_workspace_root(cwd=os.getcwd()):
    searching_for = set(['.egasub'])
    last_root    = cwd
    current_root = cwd
    found_path   = None
    while found_path is None and current_root:
        for root, dirs, _ in os.walk(current_root):
            if not searching_for - set(dirs):
                # found the directories, stop
                return root
            # only need to search for the current dir
            break

        # Otherwise, pop up a level, search again
        last_root    = current_root
        current_root = os.path.dirname(last_root)

        # stop if it's already reached os root dir
        if current_root == last_root: break

    return None


def get_settings(wspath):
    config_file = os.path.join(wspath, '.egasub', 'config.yaml')
    if not os.path.isfile(config_file):
        return None

    with open(config_file, 'r') as f:
        settings = yaml.load(f)

    return settings


def get_current_dir_type(ctx):
    workplace = ctx.obj['WORKSPACE_PATH']
    current_dir = ctx.obj['CURRENT_DIR']

    pattern = re.compile('%s/(unaligned|alignment|variation)\.' % workplace)
    m = re.match(pattern, current_dir)
    if m and m.group(1):
        return m.group(1)

    return None


def file_pattern_exist(dirname, pattern):
    files = [f for f in os.listdir(dirname) if os.path.isfile(f)]
    for f in files:
        if re.match(pattern, f): return True

    return False


def ftp_files(path, ctx):
    host = ctx.obj['SETTINGS']['ftp_server']
    _, user, passwd = ctx.obj['AUTH'].split('%20') if len(ctx.obj['AUTH'].split('%20')) == 3 else ('', '', '')

    ftp = ftplib.FTP(host, user, passwd)

    files = []
    try:
        files = ftp.nlst(path)
    except ftplib.error_perm, resp:
        echo('Error: unable to connect to FTP server.', err=True)
        ctx.abort()

    return files

