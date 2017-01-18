
class Analysis(object):
    def __init__(self, title, description, study_id, sample_references, analysis_center, analysis_date,
                 analysis_type_id, files, attributes, genome_id, chromosome_references, experiment_type_id,platform):
        self.title = title
        self.description = description
        self.study_id = study_id
        self.sample_references = sample_references
        self.analysis_center = analysis_center
        self.analysis_date = analysis_date
        self.analysis_type_id = analysis_type_id
        self.files = files
        self.attributes = attributes
        self.genome_id = genome_id
        self.chromosome_references = chromosome_references
        self.experiment_type_id = experiment_type_id
        self.platform = platform

    def to_dict(self):
        return {
            'title' : self.title,
            'description' : self.description,
            'studyId' : self.study_id,
            'sampleReferences' : map(lambda ref: ref.to_dict(), self.sample_references),
            'analysisCenter' : self.analysis_center,
            'analysisDate' : self.analysis_date,
            'analysisTypeId' : self.analysis_type_id,
            'files' : map(lambda file: file.to_dict(), self.files),
            'attributes' : map(lambda att: att.to_dict(), self.attributes),
            'genomeId' : self.genome_id,
            'chromosomeReferences' : map(lambda ref: ref.to_dict(), self.chromosome_references),
            'experimentTypeId' : self.experiment_type_id,
            'platform' : self.platform
            }

    def to_xml(self):
        pass





