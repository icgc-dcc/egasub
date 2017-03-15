from file import File
from chromosome_reference import ChromosomeReference

class Analysis(object):
    def __init__(self, alias, title, description, study_id, sample_references, analysis_center, analysis_date,
                 analysis_type_id, files, attributes, genome_id, chromosome_references, experiment_type_id,platform,status=None, id_=None,ega_accession_id=None):
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
        self.alias = alias
        self.status = status
        self.id = id_
        self.ega_accession_id = ega_accession_id

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
            'chromosomeReferences' : [ ref.to_dict() for ref in self.chromosome_references],
            'experimentTypeId' : self.experiment_type_id,
            'platform' : self.platform,
            'alias' : self.alias,
            'status': self.status,
            'egaAccessionId': self.ega_accession_id
            }

    def to_xml(self):
        pass

    @staticmethod
    def from_dict(analysis_dict):
        return Analysis(
                analysis_dict.get('alias'),
                analysis_dict.get('title'),
                analysis_dict.get('description'),
                analysis_dict.get('studyId'),
                [], # sampleReferences
                analysis_dict.get('analysisCenter'),
                analysis_dict.get('analysisDate'),
                analysis_dict.get('analysisTypeId'),
                [] if not analysis_dict.get('files') else [ File.from_dict(file_dict) for file_dict in analysis_dict.get('files')],
                [], # attribute
                analysis_dict.get('genomeId'),
                [] if not analysis_dict.get('chromosomeReferences') else [ChromosomeReference(tag) for tag in analysis_dict.get('chromosomeReferences')],
                analysis_dict.get('experimentTypeId'),
                analysis_dict.get('platform')
            )
