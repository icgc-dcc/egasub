from ..ega.entities.sample import Sample
from ..ega.entities.analysis import Analysis
from ..ega.entities.run import Run
from ..ega.entities.experiment import Experiment
from ..ega.entities.file import File
from ..ega.entities.submission import Submission
from ..ega.entities.attribute import Attribute
from ..ega.entities.submission_subset_data import SubmissionSubsetData
from ..ega.services import login, logout, submit_sample, submit_analysis,prepare_submission, submit_experiment, submit_run, submit_submission, sample_log_directory,sample_status_file,set_sample_status,get_sample_status
from ..icgc.services import id_service
from ..exceptions import ImproperlyConfigured, EgaSubmissionError, EgaObjectExistsError, CredentialsError
from click import echo
import os


def perform_submission(ctx, submission_dirs):
    echo("Login attempt with credentials in .egasub/config.yaml")
    
    try:
        login(ctx)
    except CredentialsError as error:
        print "An error occured: " +str(error)
        sys.exit(0)
        
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
        


