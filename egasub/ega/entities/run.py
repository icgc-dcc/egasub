

class Run(object):
    def __init__(self,sample_id,run_file_type_id,experiment_id,files):
        self.sample_id = sample_id
        self.run_file_type_id = run_file_type_id
        self.experiment_id = experiment_id
        self.files = files
        
    def to_dict(self):
        return {
            'sampleId' : self.sample_id,
            'runFileTypeId' : self.run_file_type_id,
            'experimentId' : self.experiment_id,
            'files' : self.files
            }
        
    def to_xml(self):
        pass