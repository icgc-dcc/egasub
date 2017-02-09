import yaml
from file import File

class Run(object):
    def __init__(self,alias,sample_id,run_file_type_id,experiment_id,files,id, status=None):
        self.alias = alias
        self.sample_id = sample_id
        self.run_file_type_id = run_file_type_id
        self.experiment_id = experiment_id
        self.files = files
        self.id = id
        self.status = status

        
    def to_dict(self):
        return {
            'alias' : self.alias,
            'sampleId' : self.sample_id,
            'runFileTypeId' : self.run_file_type_id,
            'experimentId' : self.experiment_id,
            'files' : map(lambda file: file.to_dict(), self.files),
            'id' : self.id,
            'status': self.status
            }


    def to_xml(self):
        pass


    @staticmethod
    def from_dict(run_dict):
        return Run(
                None,
                run_dict.get('sampleId'),
                run_dict.get('runFileTypeId'),
                run_dict.get('experimentId'),
                [] if not run_dict.get('files') else map(lambda file_dict: File.from_dict(file_dict), run_dict.get('files')),
                None
            )

