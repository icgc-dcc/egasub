
class Dataset(object):
    
    def __init__(self,alias,dataset_type_ids, policy_id, runs_references, analysis_references, title,
                 dataset_links, attributes, id_=None):
        self.alias = alias
        self.dataset_type_ids = dataset_type_ids
        self.policy_id = policy_id
        self.runs_references = runs_references
        self.analysis_references = analysis_references
        self.title = title
        self.dataset_links = dataset_links
        self.attributes = attributes
        self.id = id_

        
    def to_dict(self):
        return {
            'alias' : self.alias,
            'datasetTypeIds' : self.dataset_type_ids,
            'policyId' : self.policy_id,
            'runsReferences' : self.runs_references,
            'analysisReferences' : self.analysis_references,
            'title' : self.title,
            'datasetLinks' : map(lambda dataset_link: dataset_link.to_dict(), self.dataset_links),
            'attributes' : map(lambda attribute: attribute.to_dict(), self.attributes)
        }

        
    def to_xml(self):
        pass