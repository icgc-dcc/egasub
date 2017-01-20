
class SubmissionSubsetData(object):
    def __init__(self,alias,analysis_ids, dac_ids, dataset_ids, experiment_ids, policy_ids, run_ids,
                 sample_ids, study_ids):
        self.analysis_ids = analysis_ids
        self.dac_ids = dac_ids
        self.dataset_ids = dataset_ids
        self.experiment_ids = experiment_ids
        self.policy_ids = policy_ids
        self.run_ids = run_ids
        self.sample_ids = sample_ids
        self.study_ids = study_ids
        self.alias = alias
        
    def to_dict(self):
        return {
            'analysisIds' : self.analysis_ids,
            'dacIds' : self.dac_ids,
            'datasetIds' : self.dataset_ids,
            'experimentIds' : self.experiment_ids,
            'policyIds' : self.policy_ids,
            'runIds' : self.run_ids,
            'sampleIds' : self.sample_ids,
            'studyIds' : self.study_ids,
            'alias' : self.alias
            }
        
    def to_xml(self):
        pass