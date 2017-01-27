import yaml
from file import File

class Run(object):
    def __init__(self,alias,sample_id,run_file_type_id,experiment_id,files,id):
        self.alias = alias
        self.sample_id = sample_id
        self.run_file_type_id = run_file_type_id
        self.experiment_id = experiment_id
        self.files = files
        self.id = id

        
    def to_dict(self):
        return {
            'alias' : self.alias,
            'sampleId' : self.sample_id,
            'runFileTypeId' : self.run_file_type_id,
            'experimentId' : self.experiment_id,
            'files' : map(lambda file: file.to_dict(), self.files),
            'id' : self.id
            }


    def to_xml(self):
        pass
    
    @staticmethod
    def load_from_yaml(ctx,yaml_path):
        with open(yaml_path, 'r') as stream:
            yaml_stream = yaml.load(stream)
            
        yaml_run = yaml_stream.get('run')
        
        return Run(None,yaml_run.get('sampleId'),
              yaml_run.get('runFileTypeId'),
              yaml_run.get('experimentId'),
              File.load_list_from_yaml(ctx,yaml_path),None)