from ..ega.entities.sample import Sample
from ..ega.entities.analysis import Analysis
from ..ega.entities.run import Run
from ..ega.entities.experiment import Experiment
from ..ega.entities.file import File
from ..ega.entities.submission import Submission
from ..ega.entities.submission_subset_data import SubmissionSubsetData
from ..ega.services import login, logout, submit_sample, prepare_submission, submit_experiment, submit_run
from ..icgc.services import id_service
from ..exceptions import ImproperlyConfigured, EgaSubmissionError, EgaObjectExistsError
from click import echo
import yaml
import os
from multiprocessing.forking import prepare

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
                    yaml_experiment.get('studyId')
        )
    
    sample = Sample(None,yaml_sample.get('title'),
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
                    []
        )
    
    run = Run(None,yaml_run.get('sampleId'),
              yaml_run.get('runFileTypeId'),
              yaml_run.get('experimentId'),
              files)
    
    return experiment, sample, run


def perform_submission(ctx, submission_dirs):
    login(ctx)
    submission = Submission('title', 'a description',SubmissionSubsetData.create_empty())
    prepare_submission(ctx, submission)

    for submission_dir in submission_dirs:
        experiment, sample, run = metadata_parser(ctx,os.path.join(ctx.obj['CURRENT_DIR'],submission_dir,'experiment.yaml'))
        
        # Submission of the sample and recording of the id
        sample_id = submit_sample(ctx, sample)
        
        # Submission of the experiment and recording of the id
        experiment.sample_id = sample_id
        experiment_id = submit_experiment(ctx,experiment)
        
        # Submission of the run and recording of the id
        run.sample_id = sample_id
        run.experiment_id = experiment_id
        print run.to_dict()
        run_id = submit_run(ctx,run)
        
    logout(ctx)
        
    
        
def generate_file(ctx, file_id,file_name,checksum_method):
    
    full_path_file = os.path.join(ctx.obj['WORKSPACE_PATH'],file_name)
    
    md5_file = full_path_file+"."+checksum_method
    md5_checksum_encrypt = open(md5_file, 'r').readline().rstrip()
    md5_checksum_unencrypt = open(os.path.splitext(full_path_file)[0]+"."+checksum_method,'r').readline().rstrip()
    
    return File(file_id,file_name,md5_checksum_encrypt,md5_checksum_unencrypt,checksum_method)



