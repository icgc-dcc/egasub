
class SubmissionSubsetData(object):
    def __init__(self,analysis_ids, dac_ids, dataset_ids, experiment_ids, policy_ids, run_ids,
                 sample_ids, study_ids):
        self.analysis_ids = analysis_ids
        self.dac_ids = dac_ids
        self.dataset_ids = dataset_ids
        self.experiment_ids = experiment_ids
        self.policy_ids = policy_ids
        self.run_ids = run_ids
        self.sample_ids = sample_ids
        self.study_ids = study_ids

    def to_dict(self):
        return {
            'analysisIds' : self.analysis_ids,
            'dacIds' : self.dac_ids,
            'datasetIds' : self.dataset_ids,
            'experimentIds' : self.experiment_ids,
            'policyIds' : self.policy_ids,
            'runIds' : self.run_ids,
            'sampleIds' : self.sample_ids,
            'studyIds' : self.study_ids
            }

    def to_xml(self):
        pass

    @staticmethod
    def create_empty():
        return SubmissionSubsetData(None,None,None,None,None,None,None,None)