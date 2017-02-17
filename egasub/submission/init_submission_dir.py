import os
import re
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
        d = d.rstrip('/')
        if not re.match(r'^[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+){0,1}$', d):
            ctx.obj['LOGGER'].warning("Skipping directory '%s'. Submission directory should be named as <sample alias> or <sample alias>.<lane label>, sample alias and lane label may only contain letter, digit, underscore (_) or dash (-)" % d)
            continue

        if d.upper().startswith('SA'):  # we may want to make this configurable to allow it turned off for non-ICGC submitters
            ctx.obj['LOGGER'].warning("Skipping directory '%s'. Submission directory can not start with 'SA' or 'sa', this is reserved for ICGC DCC." % d)
            continue

        if d.upper().startswith('EGA'):
            ctx.obj['LOGGER'].warning("Skipping directory '%s'. Submission directory can not start with 'EGA' or 'ega', this is reserved for EGA." % d)
            continue

        dest_file = os.path.join(d, file_name)

        if os.path.isfile(dest_file):
            ctx.obj['LOGGER'].warning("Skipping directory '%s', as it already contains the file: %s" % (d, file_name))
            continue

        copyfile(src_file, dest_file)
        ctx.obj['LOGGER'].info("Initialized folder '%s' with a metadata template '%s', please fill it out properly before performing submission." % (d, file_name))
