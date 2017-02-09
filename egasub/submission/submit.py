import os
import sys
from click import echo

from ..ega.entities import Study, Submission, SubmissionSubsetData
from ..ega.services import login, logout, object_submission, query_by_id, \
                            prepare_submission, submit_submission
from ..exceptions import ImproperlyConfigured, EgaSubmissionError, EgaObjectExistsError, CredentialsError
from .submittable import Unaligned, Alignment, Variation
from .submitter import Submitter


def perform_submission(ctx, submission_dirs, dry_run=True):
    ctx.obj['LOGGER'].info("Login ...")
    
    try:
        login(ctx)
    except CredentialsError as error:
        ctx.obj['LOGGER'].critical(str(error))
        ctx.abort()

    ctx.obj['LOGGER'].info("Login success")
    submission = Submission('title', 'a description',SubmissionSubsetData.create_empty())
    prepare_submission(ctx, submission)

    #study_alias = ctx.obj['SETTINGS']['icgc_project_code']
    # need to set this up using 'init' command
    study_alias = ctx.obj['SETTINGS']['ega_study_alias']
    study = Study(
        study_alias, # alias
        8, # studyTypeId, Cancer Genomics
        'Short study name', # should take it from config
        'Study title', # should take it from config
        'Study abstract', # should take it from config
        None,  # ownTerm
        [],  # pubMedIds
        [],   # customTags
        None
    )
    object_submission(ctx, study, 'study', dry_run)
    ctx.obj['SETTINGS']['STUDY_ID'] = study.id

    # get class by string
    submission_type = ctx.obj['CURRENT_DIR_TYPE']
    Submittable_class = eval(submission_type.capitalize())

    submittables = []
    for submission_dir in submission_dirs:
        ctx.obj['LOGGER'].info("Start processing '%s'" % submission_dir)
        try:
            submittable = Submittable_class(submission_dir)
        except:
            ctx.obj['LOGGER'].error("Skip %s as it appears to be not a well formed submission directory." % submission_dir)
            continue

        submittable.local_validate(ctx.obj['EGA_ENUMS'])

        try:
            submittable.ftp_files_remote_validate('ftp.ega.ebi.ac.uk',ctx.obj['SETTINGS']['ega_submitter_account'],ctx.obj['SETTINGS']['ega_submitter_password'])
        except Exception, e:
            ctx.obj['LOGGER'].error("FTP file check error, please make sure data files uploaded to the EGA FTP server already.")
            continue

        for err in submittable.local_validation_errors:
            ctx.obj['LOGGER'].error("Local validation error(s) for submission dir '%s': %s" % (submittable.submission_dir,err))
            
        for err in submittable.ftp_file_validation_errors:
            ctx.obj['LOGGER'].error("FTP files remote validation error(s) for submission dir '%s': %s" % (submittable.submission_dir,err))

        # only process submittables at certain states and no local
        # validation error
        if not submittable.status == 'SUBMITTED' \
                and not submittable.local_validation_errors:
            submittables.append(submittable)
        elif submittable.status == 'SUBMITTED':
            ctx.obj['LOGGER'].info("Skip '%s' as it has already been submitted." % submittable.submission_dir)
        else:
            ctx.obj['LOGGER'].info("Skip '%s' as it failed validation, please check log for details." % submittable.submission_dir)

    if not submittables:
        ctx.obj['LOGGER'].warning('Nothing to submit.')
    else:
        if dry_run:
            ok_to_sub = [s.submission_dir for s in submittables]
            ctx.obj['LOGGER'].info("Dry run completed, items OK for submission: %s" % ",".join(ok_to_sub))
        else:
            submitter = Submitter(ctx)
            for submittable in submittables:
                submitter.submit(submittable)

    # TODO: submit submission, do we need this?

    ctx.obj['LOGGER'].info("Logging out the session")
    logout(ctx)


