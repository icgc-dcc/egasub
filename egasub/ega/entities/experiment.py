
class Experiment(object):
    def __init__(self,alias, title, instrument_model_id, library_source_id, library_selection_id,
                 library_strategy_id, design_description, library_name, library_construction_protocol,
                 library_layout_id, paired_nomial_length, paired_nominal_sdev,
                 sample_id, study_id):
        self.title = title
        self.instrument_model_id = instrument_model_id
        self.library_source_id = library_source_id
        self.library_selection_id = library_selection_id
        self.library_strategy_id = library_strategy_id
        self.design_description = design_description
        self.library_name = library_name
        self.library_construction_protocol = library_construction_protocol
        self.library_layout_id = library_layout_id
        self.paired_nominal_length = paired_nomial_length
        self.paired_nominal_sdev = paired_nominal_sdev
        self.sample_id = sample_id
        self.study_id = study_id
        self.alias = alias
        
    def to_dict(self):
        return {
            'title' : self.title,
            'instrumentModelId' : self.instrument_model_id,
            'librarySourceId' : self.library_source_id,
            'librarySelectionId' : self.library_selection_id,
            'libraryStrategyId' : self.library_strategy_id,
            'designDescription' :self.design_description,
            'libraryName' : self.library_name,
            'libraryConstructionProtocol' : self.library_construction_protocol,
            'libraryLayoutId' : self.library_layout_id,
            'pairedNominalLength' : self.paired_nominal_length,
            'pairedNominalSdev' : self.paired_nominal_sdev,
            'sampleId' : self.sample_id,
            'studyId' : self.study_id,
            'alias' : self.alias
            }
        
    def to_xml(self):
        pass