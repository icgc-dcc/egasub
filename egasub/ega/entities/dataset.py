
class Dataset(object):
    
    def __init__(self, dataset_type_ids, policy_id, runs_references, analysis_references, title,
                 dataset_links, attributes):
        self.dataset_type_ids = dataset_type_ids
        self.policy_id = policy_id
        self.runs_references = runs_references
        self.analysis_references = analysis_references
        self.title = title
        self.dataset_links = dataset_links
        self.attributes = attributes
        
    def to_dict(self):
        return {
            'datasetTypeIds' : self.dataset_type_ids,
            'policyId' : self.policy_id,
            'runsReferences' : self.runs_references,
            'analysisReferences' : self.analysis_references,
            'title' : self.title,
            'datasetLinks' : self.dataset_links,
            'attributes' : self.attributes
        }
        
    def to_xml(self):
        pass