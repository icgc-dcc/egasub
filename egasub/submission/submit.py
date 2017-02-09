import os
import sys
from click import echo, prompt

from ..ega.entities import Study, Submission, SubmissionSubsetData, Dataset
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
    study_id = object_submission(ctx, study, 'study', dry_run)
    ctx.obj['SETTINGS']['STUDY_ID'] = study_id

    # get class by string
    submission_type = ctx.obj['CURRENT_DIR_TYPE']
    Submittable_class = eval(submission_type.capitalize())

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
        if submittable.status in ('NEW') \
                and not submittable.local_validation_errors:
            submittables.append(submittable)
            
    if not submittables:
        ctx.obj['LOGGER'].warning('Nothing to submit.')
        
    submitter = Submitter(ctx)
    for submittable in submittables:
        submitter.submit(submittable, dry_run)

    # TODO: submit submission

    ctx.obj['LOGGER'].info("Logging out the session")
    logout(ctx)
    
    
def submit_dataset(ctx, dry_run=True):
    ctx.obj['LOGGER'].info("Login ...")
    
    try:
        login(ctx)
    except CredentialsError as error:
        ctx.obj['LOGGER'].critical(str(error))
        ctx.abort()
        
    dataset_types = ctx.obj['EGA_ENUMS'].__dict__['_enums']['dataset_types']['response']['result']
    ids = [dataset['tag'] for dataset in dataset_types]
    values = [dataset['value'] for dataset in dataset_types]
    
    policy_id = ctx.obj['SETTINGS']['ega_policy_id']
    
    run_references = []
    not_submitted = []
    for sub_folder in os.listdir(ctx.obj['CURRENT_DIR']):
        sub_folder_path = os.path.join(ctx.obj['CURRENT_DIR'],sub_folder)
        run_file_log = os.path.join(sub_folder_path,'.status','run.log')
        status = submittable_status(run_file_log)
        if status[2] == 'SUBMITTED':
            run_references.append(status[1])  # 1 is alias, 0 is id
        else:
            not_submitted.append(sub_folder)

    if not_submitted:
        ctx.obj['LOGGER'].error("These samples have not been submitted yet: %s" % ','.join(not_submitted))
        logout(ctx)
        ctx.abort()

    for i in xrange(0,len(values)):
        print ids[i]+"\t- "+values[i]
    
    echo("-----------")
    while True:
        dataset_type_id = prompt("Select the dataset type: ")
        if dataset_type_id in ids:
            break

    # TODO: need to determine these values for the dataset
    dataset = Dataset(
                        'alias',
                        [dataset_type_id],
                        1,
                        run_references,
                        [],
                        'a title',
                        [],
                        []
                    )
    submission = Submission('Empty title', None, SubmissionSubsetData.create_empty())
    prepare_submission(ctx, submission)

    try:
        object_submission(ctx, dataset, 'dataset', dry_run)
    except Exception, err:
        ctx.obj['LOGGER'].error("Submitting dataset failed: %s" % err)
        logout(ctx)
        ctx.abort()

    ctx.obj['LOGGER'].info("Logging out the session")    
    logout(ctx)


def submittable_status(_file):
    try:
        with open(_file,'r') as f:
            for last in f:
                pass
        return last.strip().split('\t')
    except:
        return [None, None, None, None]

