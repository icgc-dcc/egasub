import os
import sys
import json
from click import echo

from ..ega.entities import Study, Submission, SubmissionSubsetData
from ..ega.services import login, logout, submit_obj, query_by_id, obj_type_to_endpoint, \
                            prepare_submission, submit_submission
from ..icgc.services import id_service
from ..exceptions import ImproperlyConfigured, EgaSubmissionError, EgaObjectExistsError, CredentialsError
from .submittable import Unaligned, Alignment, Variation
from .submitter import Submitter


def perform_submission(ctx, submission_dirs, dry_run=None):
    ctx.obj['LOGGER'].info("Login ...")
    
    try:
        login(ctx)
    except CredentialsError as error:
        ctx.obj['LOGGER'].critical(str(error))
        ctx.abort()
         

    ctx.obj['LOGGER'].info("Login success")
    submission = Submission('title', 'a description',SubmissionSubsetData.create_empty())
    prepare_submission(ctx, submission)

    # this seems not fit here, should be done elsewhere as a one time operation
    study_alias = ctx.obj['SETTINGS']['icgc_project_code']
    study = query_by_id(ctx, obj_type_to_endpoint('study'), study_alias, 'ALIAS')
    if not study:  # study does not exist on EGA side
        study = Study(
            study_alias, # alias
            1, # studyTypeId
            'Short study name', # should take it from config
            'Study title', # should take it from config
            'Study abstract', # should take it from config
            None,  # ownTerm
            [],  # pubMedIds
            [],   # customTags
            None
        )
        submit_obj(ctx, study, 'study')
        ctx.obj['SETTINGS']['STUDY_ID'] = study.id
    else:
        ctx.obj['SETTINGS']['STUDY_ID'] = study[0].get('id')

    ctx.obj['LOGGER'].info("Study alias: %s, study ID: %s" % (study_alias, ctx.obj['SETTINGS']['STUDY_ID']))
    # get class by string
    submission_type = ctx.obj['CURRENT_DIR_TYPE']
    Submittable_class = eval(submission_type.capitalize())

    # TODO: 
    #   collect all of the submittables,
    #   we will perform a quick local validation / status check
    #   on each of the submittables
    submittables = []
    for submission_dir in submission_dirs:
        try:
            submittable = Submittable_class(submission_dir)
        except:
            ctx.obj['LOGGER'].error("Skip %s as it appears to be not a well formed submission directory." % submission_dir)
            continue

        submittable.local_validate(ctx.obj['EGA_ENUMS'])
        
        try:
            submittable.ftp_files_remote_validate('ftp.ega.ebi.ac.uk',ctx.obj['SETTINGS']['ega_submitter_account'],ctx.obj['SETTINGS']['ega_submitter_password'])
        except Exception, e:
            ctx.obj['LOGGER'].error("FTP server error: %s",str(e))
            continue

        for err in submittable.local_validation_errors:
            ctx.obj['LOGGER'].error("Local validation error(s) for submission dir '%s': %s" % (submittable.submission_dir,err))
            
        for err in submittable.ftp_file_validation_errors:
            ctx.obj['LOGGER'].error("FTP files remote validation error(s) for submission dir '%s': %s" % (submittable.submission_dir,err))

        # only process submittables at certain states and no local
        # validation error
        exit()
        if submittable.status in ('NEW') \
                and not submittable.local_validation_errors:
            submittables.append(submittable)

    if not submittables:
        ctx.obj['LOGGER'].info('Nothing to submit.')

    submitter = Submitter(ctx)
    for submittable in submittables:
            submitter.submit(submittable, dry_run)

    # TODO: submit submission

    ctx.obj['LOGGER'].info("Logging out the session")
    logout(ctx)


