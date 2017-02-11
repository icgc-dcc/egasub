import os
from click import echo
from shutil import copyfile

def init_submission_dir(ctx, submission_dirs):
    submission_type = ctx.obj['CURRENT_DIR_TYPE']
    if submission_type in ("alignment", "variation"):
        file_name = "analysis.yaml"
    elif submission_type in ("unaligned"):
        file_name = "experiment.yaml"
    else:
        ctx.obj['LOGGER'].critical('You must be in one of the supported submission data type directory: unaligned, alignment or variation')
        ctx.abort()

    src_file = os.path.join(os.path.dirname(
                    os.path.realpath(__file__)),
                    'metadata_template',
                    submission_type,file_name
                )
    for d in submission_dirs:
        dest_file = os.path.join(d, file_name)

        if os.path.isfile(dest_file):
            ctx.obj['LOGGER'].warning("Skipping directory '%s', as it already contains the file: %s" % (d, file_name))
            continue

        copyfile(src_file, dest_file)
        ctx.obj['LOGGER'].info("Initialized folder '%s' with a metadata template '%s', please fill it out properly before performing submission." % (d, file_name))
