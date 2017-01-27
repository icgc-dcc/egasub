import yaml
from file import File
from sample_reference import SampleReference
from attribute import Attribute

class Analysis(object):
    def __init__(self, alias, title, description, study_id, sample_references, analysis_center, analysis_date,
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
        self.alias = alias

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
            'chromosomeReferences' : self.chromosome_references,
            'experimentTypeId' : self.experiment_type_id,
            'platform' : self.platform,
            'alias' : self.alias
            }

    def to_xml(self):
        pass
    
    @staticmethod
    def load_from_yaml(ctx,yaml_path):
        with open(yaml_path, 'r') as stream:
            yaml_stream = yaml.load(stream)
            
        yaml_analysis = yaml_stream.get('analysis')        
            
        return Analysis(None,
            yaml_analysis.get('title'),
            yaml_analysis.get('description'),
            yaml_analysis.get('study_id'),
            SampleReference.load_list_from_yaml(ctx,yaml_path),
            yaml_analysis.get('analysis_center'),
            yaml_analysis.get('analysis_date'),
            yaml_analysis.get('analysis_type_id'),
            File.load_list_from_yaml(ctx,yaml_path),
            Attribute.load_list_from_yaml(ctx,yaml_path),
            yaml_analysis.get('genome_id'),
            yaml_analysis.get('chromosome_references'),
            yaml_analysis.get('experiment_type_id'),
            yaml_analysis.get('platform')
            )





