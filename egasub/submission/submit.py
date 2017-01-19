from ..ega.entities.sample import Sample
from ..ega.entities.analysis import Analysis
from ..ega.entities.run import Run
from ..ega.entities.experiment import Experiment
from ..ega.entities.file import File
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
    
    experiment = Experiment(yaml_experiment.get('title'),
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
    
    sample = Sample(yaml_sample.get('title'),
                    yaml_sample.get('description'),
                    yaml_sample.get('caseOrControlId'),
                    yaml_sample.get('genderId'),
                    yaml_sample.get('organismPart'),
                    yaml_sample.get('cellLine'),
                    yaml_sample.get('region'),
                    yaml_sample.get('phenotype'),
                    yaml_sample.get('subjectId'),
                    yaml_sample.get('anonymizedName'),
                    yaml_sample.get('biosampleId'),
                    yaml_sample.get('sampleAge'),
                    yaml_sample.get('sampleDetail'),
                    []
        )
    
    run = Run(yaml_run.get('sampleId'),
              yaml_run.get('runFileTypeId'),
              yaml_run.get('experimentId'),
              files)
    
    submit_object(ctx, experiment)
    submit_object(ctx, sample)
    submit_object(ctx, run)


def submit_object(ctx, object):
    class_name = object.__class__.__name__
    if class_name == "Experiment":
        print "Submit Experiment"
    elif class_name == "Sample":
        print "Submit Sample"
    elif class_name == "Run":
        print "Submit Run"


def perform_submission(ctx, submission_dirs):
    for submission_dir in submission_dirs:
        metadata_parser(ctx,os.path.join(ctx.obj['CURRENT_DIR'],submission_dir,'experiment.yaml'))
        
def generate_file(ctx, file_id,file_name,checksum_method):
    
    full_path_file = os.path.join(ctx.obj['WORKSPACE_PATH'],file_name)
    
    md5_file = full_path_file+"."+checksum_method
    md5_checksum_encrypt = open(md5_file, 'r').readline().rstrip()
    md5_checksum_unencrypt = open(os.path.splitext(full_path_file)[0]+"."+checksum_method,'r').readline().rstrip()
    
    return File(file_id,file_name,md5_checksum_encrypt,md5_checksum_unencrypt,checksum_method)



