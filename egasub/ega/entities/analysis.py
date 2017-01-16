"""
Example doc given by EGA: https://ega-archive.org/submission/programmatic_submissions/json-message-format#analysisJson
Analysis
{
  "title": "",
  "description": "",
  "studyId": "",
  "sampleReferences": [
    {
      "value": "",
      "label": ""
    }
  ],
  "analysisCenter": "",
  "analysisDate": "",
  "analysisTypeId": "", → /enums/analysis_types
  "files": [
    {
    "fileId": "",
      "fileName": "",
      "checksum": "",
      "unencryptedChecksum": ""
    }
  ],
  "attributes": [
    {
      "tag": "",
      "value": "",
      "unit": ""
    }
  ],
  "genomeId": "", → /enums/reference_genomes
  "chromosomeReferences": [ → /enums/reference_chromosomes
    {
      "value": "",
      "label": ""
    }
  ],
  "experimentTypeId": [ "" ], → /enums/experiment_types
  "platform": ""
}
"""

from sample import Sample


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
            'sampleReferences' : self.sample_references,
            'analysisCenter' : self.analysis_center,
            'analysisDate' : self.analysis_date,
            'analysisTypeId' : self.analysis_type_id,
            'files' : self.files,
            'attributes' : self.attributes,
            'genomeId' : self.genome_id,
            'chromosomeReferences' : self.chromosome_references,
            'experimentTypeId' : self.experiment_type_id,
            'platform' : self.platform
            }

    def to_xml(self):
        pass



