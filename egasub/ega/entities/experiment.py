
class Experiment(object):
    def __init__(self, alias, title, instrument_model_id, library_source_id, library_selection_id,
                 library_strategy_id, design_description, library_name, library_construction_protocol,
                 library_layout_id, paired_nomial_length, paired_nominal_sdev,
                 sample_id, study_id,_id, status=None, ega_accession_id=None):
        self.alias = alias
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
        self.id = _id
        self.status = status
        self.ega_accession_id = ega_accession_id

    def to_dict(self):
        return {
            'alias' : self.alias,
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
            'id' : self.id,
            'status': self.status,
            'egaAccessionId': self.ega_accession_id
            }


    def to_xml(self):
        pass


    @staticmethod
    def from_dict(exp_dict):
        return Experiment(
                    None,
                    exp_dict.get('title'),
                    exp_dict.get('instrumentModelId'),
                    exp_dict.get('librarySourceId'),
                    exp_dict.get('librarySelectionId'),
                    exp_dict.get('libraryStrategyId'),
                    exp_dict.get('designDescription'),
                    exp_dict.get('libraryName'),
                    exp_dict.get('libraryConstructionProtocol'),
                    exp_dict.get('libraryLayoutId'),
                    exp_dict.get('pairedNominalLength'),
                    exp_dict.get('pairedNominalSdev'),
                    exp_dict.get('sampleId'),
                    exp_dict.get('studyId'),
                    None
        )
