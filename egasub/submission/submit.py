import os
import sys
import json
from click import echo

from ..ega.entities import Study, Submission, SubmissionSubsetData

from ..ega.services import login, logout, submit_obj, \
                            prepare_submission, submit_submission

from ..icgc.services import id_service
from ..exceptions import ImproperlyConfigured, EgaSubmissionError, EgaObjectExistsError, CredentialsError

from .submittable import Unaligned, Alignment, Variation
from .submitter import Submitter


def perform_submission(ctx, submission_dirs, dry_run=None):
    echo("Login ...")
    
    try:
        login(ctx)
    except CredentialsError as error:
        print "An error occured: " + str(error)
        sys.exit(1) # exit with non-zero code

    echo("Login success")
    submission = Submission('title', 'a description',SubmissionSubsetData.create_empty())
    prepare_submission(ctx, submission)

    # this seems not fit here, should be done elsewhere as a one time operation
    study = Study(
            ctx.obj['SETTINGS']['icgc_project_code'], # alias
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

    # get class by string
    submission_type = ctx.obj['CURRENT_DIR_TYPE']
    Submittable_class = eval(submission_type.capitalize())

    # TODO: 
    #   collect all of the submittables,
    #   we will perform a quick local validation / status check
    #   on each of the submittables
    submittables = []
    for submission_dir in submission_dirs:
        submittable = Submittable_class(submission_dir)
        
        submittable.local_validate(ctx.obj['EGA_ENUMS'])
        echo(" Local validation error(s) for %s: \n  %s" % (submittable.sample.alias,
                "\n  ".join([json.dumps(err) for err in submittable.local_validation_errors]) \
                       if submittable.local_validation_errors else "none")
            )

        # only process submittables at certain states and no local
        # validation error
        if submittable.status in ('NEW') \
                and not submittable.local_validation_errors:
            submittables.append(submittable)

    if not submittables:
        echo('Nothing to submit.')

    submitter = Submitter(ctx)
    for submittable in submittables:
            submitter.submit(submittable, dry_run)

    # TODO: submit submission

    echo("Logging out the session")
    logout(ctx)
    echo("")


