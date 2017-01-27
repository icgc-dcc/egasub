from ..ega.entities.sample import Sample
from ..ega.entities.analysis import Analysis
from ..ega.entities.run import Run
from ..ega.entities.experiment import Experiment
from ..ega.entities.file import File
from ..ega.entities.submission import Submission
from ..ega.entities.submission_subset_data import SubmissionSubsetData
from ..ega.services import login, logout, submit_sample, prepare_submission, submit_experiment, submit_run, submit_submission, sample_log_directory,sample_status_file,set_sample_status,get_sample_status
from ..icgc.services import id_service
from ..exceptions import ImproperlyConfigured, EgaSubmissionError, EgaObjectExistsError
from click import echo
import yaml
import os

def metadata_parser(ctx, metadata):
    with open(metadata, 'r') as stream:
        yaml_stream = yaml.load(stream)
        
    yaml_experiment = yaml_stream.get('experiment')
    yaml_sample = yaml_stream.get('sample')
    yaml_run = yaml_stream.get('run')
    yaml_files = yaml_stream.get('file')
    
    files = []
    for _file in yaml_files:
        files.append(generate_file(ctx,None,_file.get('fileName'),'md5'))
    
    experiment = Experiment(None,yaml_experiment.get('title'),
                    yaml_experiment.get('instrumentModelId'),
                    yaml_experiment.get('librarySourceId'),
                    yaml_experiment.get('librarySelectionId'),
                    yaml_experiment.get('libraryStrategyId'),
                    yaml_experiment.get('designDescription'),
                    yaml_experiment.get('libraryName'),
                    yaml_experiment.get('libraryConstructionProtocol'),
                    yaml_experiment.get('libraryLayoutId'),
                    yaml_experiment.get('pairedNominalLength'),
                    yaml_experiment.get('pairedNominalSdev'),
                    yaml_experiment.get('sampleId'),
                    yaml_experiment.get('studyId'),
                    None
        )
    
    sample = Sample(yaml_sample.get('alias'),yaml_sample.get('title'),
                    yaml_sample.get('description'),
                    yaml_sample.get('caseOrControlId'),
                    yaml_sample.get('genderId'),
                    yaml_sample.get('organismPart'),
                    yaml_sample.get('cellLine'),
                    yaml_sample.get('region'),
                    yaml_sample.get('phenotype'),
                    yaml_sample.get('subjectId'),
                    yaml_sample.get('anonymizedName'),
                    yaml_sample.get('bioSampleId'),
                    yaml_sample.get('sampleAge'),
                    yaml_sample.get('sampleDetail'),
                    [],
                    None
        )
    
    run = Run(None,yaml_run.get('sampleId'),
              yaml_run.get('runFileTypeId'),
              yaml_run.get('experimentId'),
              files,None)
    
    return experiment, sample, run


def perform_submission(ctx, submission_dirs):
    echo("Login attempt with credentials in .egasub/config.yaml")
    login(ctx)
    echo("Login success")
    submission = Submission('title', 'a description',SubmissionSubsetData.create_empty())
    prepare_submission(ctx, submission)
    
    experiment_ids = []
    run_ids = []
    sample_ids = []

    for submission_dir in submission_dirs:
        echo("-------")
        echo("Processing "+submission_dir)
        
        echo("Data parsing from experiment.yaml")
        experiment, sample, run = metadata_parser(ctx,os.path.join(ctx.obj['CURRENT_DIR'],submission_dir,'experiment.yaml'))
        
        echo(" - Submission of the sample")
        """
        # we will need to do more to be able to really track submssion steps
        if not os.path.isdir(sample_log_directory(ctx,submission_dir)):
            os.mkdir(sample_log_directory(ctx,submission_dir))
        if not os.path.exists(sample_status_file(ctx,submission_dir)):
            set_sample_status(ctx,submission_dir,"DRAFT")
        if get_sample_status(ctx,submission_dir)=="VALIDATED":
            continue
        """

        # Submission of the sample and recording of the id
        submit_sample(ctx, sample,submission_dir)
        
        echo(" - Submission of the experiment")
        # Submission of the experiment and recording of the id
        experiment.sample_id = sample.id
        submit_experiment(ctx,experiment)
        
        echo(" - Submission of the run")
        # Submission of the run and recording of the id
        run.sample_id = sample.id
        run.experiment_id = experiment.id
        submit_run(ctx,run)
        
        experiment_ids.append(experiment.id)
        run_ids.append(run.id)
        sample_ids.append(sample.id)
        echo(submission_dir+" completed")
        echo("-------")
        
    echo("Finalizing the submission with all samples")
    submission.submission_subset.experiment_ids = experiment_ids
    submission.submission_subset.run_ids = run_ids
    submission.submission_subset.sample_ids = sample_ids
    
    echo("Submission of the submission metadata to EGA")
    submit_submission(ctx,submission)
    echo("")
          
    echo("Logging out the session")
    logout(ctx)
    echo("")
        
    
        
def generate_file(ctx, file_id,file_name,checksum_method):
    
    full_path_file = os.path.join(ctx.obj['WORKSPACE_PATH'],file_name)
    
    md5_file = full_path_file+"."+checksum_method
    md5_checksum_encrypt = open(md5_file, 'r').readline().rstrip()
    md5_checksum_unencrypt = open(os.path.splitext(full_path_file)[0]+"."+checksum_method,'r').readline().rstrip()
    
    return File(file_id,file_name,md5_checksum_encrypt,md5_checksum_unencrypt,checksum_method)



