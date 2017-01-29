import os
from click import echo

from ..ega.entities import Study, Sample, Analysis, Run, Experiment, \
                            File, Submission, Attribute, SubmissionSubsetData

from ..ega.services import login, logout, submit_obj, prepare_submission, \
                            submit_sample, submit_analysis,\
                            submit_experiment, submit_run, \
                            submit_submission

from ..icgc.services import id_service
from ..exceptions import ImproperlyConfigured, EgaSubmissionError, EgaObjectExistsError, CredentialsError

from .submittable import Unaligned, Alignment, Variation


def perform_submission_old(ctx, submission_dirs):
    echo("Login...")
    
    try:
        login(ctx)
    except CredentialsError as error:
        print "An error occured: " +str(error)
        sys.exit(1) # exit with non-zero code
        
    echo("Login success")
    submission = Submission('title', 'a description',SubmissionSubsetData.create_empty())
    prepare_submission(ctx, submission)

    if ctx.obj['CURRENT_DIR_TYPE'] == "unaligned":
        experiment_ids = []
        run_ids = []
        sample_ids = []
        
        for submission_dir in submission_dirs:
            metadata = os.path.join(ctx.obj['CURRENT_DIR'],submission_dir,"experiment.yaml")
            
            experiment = Experiment.load_from_yaml(ctx,metadata)
            sample = Sample.load_from_yaml(ctx,metadata)
            run = Run.load_from_yaml(ctx,metadata)
            
            experiment.sample_id = sample.id
            submit_experiment(ctx,experiment)
            
            run.sample_id = sample.id
            run.experiment_id = experiment.id
            submit_run(ctx,run)
            
            experiment_ids.append(experiment.id)
            run_ids.append(run.id)
            sample_ids.append(sample.id)
            
        submission.submission_subset.experiment_ids = experiment_ids
        submission.submission_subset.run_ids = run_ids
        submission.submission_subset.sample_ids = sample_ids
        
        submit_submission(ctx,submission)
    elif ctx.obj['CURRENT_DIR_TYPE'] == "alignment":
        for submission_dir in submission_dirs:
            metadata = os.path.join(ctx.obj['CURRENT_DIR'],submission_dir,"analysis.yaml")
            analysis = Analysis.load_from_yaml(ctx,metadata)
            sample = Sample.load_from_yaml(ctx,metadata)
            submit_analysis(ctx,analysis)
            continue


        #echo(" - Submission of the sample")
        # we will need to do more to be able to really track submssion steps
        #if not os.path.isdir(sample_log_directory(ctx,submission_dir)):
        #    os.mkdir(sample_log_directory(ctx,submission_dir))
        #if not os.path.exists(sample_status_file(ctx,submission_dir)):
        #    set_sample_status(ctx,submission_dir,"DRAFT")
        #if get_sample_status(ctx,submission_dir)=="VALIDATED":
        #    continue
        
    echo("Logging out the session")
    logout(ctx)
    echo("")


def perform_submission(ctx, submission_dirs, dry_run):
    echo("Login ...")
    try:
        login(ctx)
    except CredentialsError as error:
        print "An error occured: " +str(error)
        sys.exit(1) # exit with non-zero code
        
    echo("Login success")
    submission = Submission('title', 'a description',SubmissionSubsetData.create_empty())
    prepare_submission(ctx, submission)

    # get class by string
    submission_type = ctx.obj['CURRENT_DIR_TYPE']
    submittable_class = eval(submission_type.capitalize())

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

    for submission_dir in submission_dirs:
        submittable = submittable_class(submission_dir)
        if submission_type == 'unaligned':
            submittable.sample.attributes.append(
                    Attribute(
                        'icgc_sample_id',
                        id_service(ctx, 'sample',
                            ctx.obj['SETTINGS']['icgc_project_code'],
                            submittable.sample.alias,
                            True,True
                        )
                    )
                )

            submit_obj(ctx, submittable.sample, 'sample')

            submittable.experiment.sample_id = submittable.sample.id
            submittable.experiment.study_id = study.id
            submit_obj(ctx, submittable.experiment, 'experiment')

            submittable.run.sample_id = submittable.sample.id
            submittable.run.experiment_id = submittable.experiment.id
            submit_obj(ctx, submittable.run, 'run')

        if submission_type == 'alignment':
            """
            TODO: to be implemented
            """
            print submittable.sample.to_dict()
            print submittable.analysis.to_dict()

        if submission_type == 'variation':
            """
            TODO: to be implemented
            """
            pass


    echo("Logging out the session")
    logout(ctx)
    echo("")


