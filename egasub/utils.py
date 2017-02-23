import os
import re
import yaml
import ftplib
from click import echo
import logging
import datetime
from egasub.ega.entities import EgaEnums



def initialize_app(ctx):
    if not ctx.obj['WORKSPACE_PATH']:
        ctx.obj['LOGGER'].critical('Not in an EGA submission workspace! Please run "egasub init" to initiate an EGA workspace.')
        ctx.abort()

    # read the settings
    ctx.obj['SETTINGS'] = get_settings(ctx.obj['WORKSPACE_PATH'])
    if not ctx.obj['SETTINGS']:
        ctx.obj['LOGGER'].critical('Unable to read config file, or config file invalid!')
        ctx.abort()

    # figure out the current dir type, e.g., study, sample or analysis
    ctx.obj['CURRENT_DIR_TYPE'] = get_current_dir_type(ctx)

    if not ctx.obj['CURRENT_DIR_TYPE']:
        ctx.obj['LOGGER'].critical("You must run this command directly under a 'submission batch' directory named with this pattern: (unaligned|alignment|variation)\.([a-zA-Z0-9_\-]+). You can create 'submission batch' directories under the current workspace: %s" % ctx.obj['WORKSPACE_PATH'])
        ctx.abort()

    ctx.obj['EGA_ENUMS'] = EgaEnums()

def initialize_log(ctx, debug, info):
    logger = logging.getLogger('ega_submission')
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s")

    logger.setLevel(logging.DEBUG)

    if ctx.obj['WORKSPACE_PATH'] == None:
        logger = logging.getLogger('ega_submission')
        ch = logging.StreamHandler()
        if debug:
            ch.setLevel(logging.DEBUG)
        elif info:
            ch.setLevel(logging.INFO)
        logger.addHandler(ch)
        ctx.obj['LOGGER'] = logger
        return

    log_directory = os.path.join(ctx.obj['WORKSPACE_PATH'],".log")
    log_file = "%s.log" % re.sub(r'[-:.]', '_', datetime.datetime.utcnow().isoformat())
    ctx.obj['log_file'] = log_file
    log_file = os.path.join(log_directory, log_file)

    if not os.path.isdir(log_directory):
        os.mkdir(log_directory)

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)  # always set fh to debug
    fh.setFormatter(logFormatter)

    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("[%(levelname)-5.5s] %(message)s"))
    if debug:
        ch.setLevel(logging.DEBUG)
    elif info:
        ch.setLevel(logging.INFO)

    logger.addHandler(fh)
    logger.addHandler(ch)

    ctx.obj['LOGGER'] = logger

def find_workspace_root(cwd=os.getcwd()):
    searching_for = set(['.egasub'])
    last_root    = cwd
    current_root = cwd
    found_path   = None
    while found_path is None and current_root:
        for root, dirs, _ in os.walk(current_root):
            if not searching_for - set(dirs):
                # found the directories, stop
                if os.path.isfile(os.path.join(root, '.egasub', 'config.yaml')):
                    return root
                else:
                    return None
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
        settings = yaml.safe_load(f)

    return settings


def get_current_dir_type(ctx):
    workplace = ctx.obj['WORKSPACE_PATH']
    current_dir = ctx.obj['CURRENT_DIR']

    pattern = re.compile('^%s/(unaligned|alignment|variation)\.([a-zA-Z0-9_\-]+)$' % workplace)
    m = re.match(pattern, current_dir)
    if m and m.group(1):
        return m.group(1)

    return None


def file_pattern_exist(dirname, pattern):
    files = [f for f in os.listdir(dirname) if os.path.isfile(f)]
    for f in files:
        if re.match(pattern, f): return True

    return False


