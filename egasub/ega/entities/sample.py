from .attribute import Attribute


class Sample(object):
    def __init__(self,alias,title,description,case_or_control_id,gender_id,organism_part,
                 cell_line,region,phenotype, subject_id, anonymized_name, bio_sample_id,
                 sample_age, sample_detail, attributes,id_=None,status=None,ega_accession_id=None):
        self.alias = alias
        self.title = title
        self.description  = description
        self.case_or_control_id = case_or_control_id
        self.gender_id = gender_id
        self.organism_part = organism_part
        self.cell_line = cell_line
        self.region = region
        self.phenotype = phenotype
        self.subject_id = subject_id
        self.anonymized_name = anonymized_name
        self.bio_sample_id = bio_sample_id
        self.sample_age = sample_age
        self.sample_detail = sample_detail
        self.attributes = attributes
        self.id = id_
        self.status = status
        self.ega_accession_id = ega_accession_id

    def to_dict(self):
        return {
            'alias' : self.alias,
            'title' : self.title,
            'description' : self.description,
            'caseOrControlId' : self.case_or_control_id,
            'genderId' : self.gender_id,
            'organismPart' : self.organism_part,
            'cellLine' : self.cell_line,
            'region' : self.region,
            'phenotype' : self.phenotype,
            'subjectId' : self.subject_id,
            'anonymizedName' : self.anonymized_name,
            'bioSampleId' : self.bio_sample_id,
            'sampleAge' : self.sample_age,
            'sampleDetail' : self.sample_detail,
            'attributes' : map(lambda attribute: attribute.to_dict(), self.attributes),
            'id' : self.id,
            'status': self.status,
            'egaAccessionId': self.ega_accession_id
            }

    def to_xml(self):
        pass

    @staticmethod
    def from_dict(sample_dict):
        return Sample(
                    sample_dict.get('alias'),
                    sample_dict.get('title'),
                    sample_dict.get('description'),
                    sample_dict.get('caseOrControlId'),
                    sample_dict.get('genderId'),
                    sample_dict.get('organismPart'),
                    sample_dict.get('cellLine'),
                    sample_dict.get('region'),
                    sample_dict.get('phenotype'),
                    sample_dict.get('subjectId'),
                    sample_dict.get('anonymizedName'),
                    sample_dict.get('bioSampleId'),
                    sample_dict.get('sampleAge'),
                    sample_dict.get('sampleDetail'),
                    [] if not sample_dict.get('attributes') else [ Attribute.from_dict(attr_dict) for attr_dict in sample_dict.get('attributes')],
                    None
        )
