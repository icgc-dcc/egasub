

class Run(object):
    def __init__(self,alias,sample_id,run_file_type_id,experiment_id,files):
        self.sample_id = sample_id
        self.run_file_type_id = run_file_type_id
        self.experiment_id = experiment_id
        self.files = files
        self.alias = alias
        
    def to_dict(self):
        return {
            'sampleId' : self.sample_id,
            'runFileTypeId' : self.run_file_type_id,
            'experimentId' : self.experiment_id,
            'files' : map(lambda file: file.to_dict(), self.files),
            'alias' : self.alias
            }
        
    def to_xml(self):
        pass