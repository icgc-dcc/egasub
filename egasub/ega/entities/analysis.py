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
    “fileId”: “”,
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
    def __init__(self, samples, files, attributes, genome, chromosomes):
        self.title = None
        self.description = None
        self.samples = samples
        self.files = samples
        self.attributes = attributes
        self.genome_id = genome
        self.chromosomes = chromosomes
        self.


    def to_xml(self):
        pass


    def to_json(self):
        pass



