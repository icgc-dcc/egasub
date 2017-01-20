

class Sample(object):
    def __init__(self,alias,title,description,case_or_control_id,gender_id,organism_part,
                 cell_line,region,phenotype, subject_id, anonymized_name, biosample_id,
                 sample_age, sample_detail, attributes):
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
        self.biosample_id = biosample_id
        self.sample_age = sample_age
        self.sample_detail = sample_detail
        self.attributes = attributes
        self.alias = alias
        
    def to_dict(self):
        return {
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
            'bioSampleId' : self.biosample_id,
            'sampleAge' : self.sample_age,
            'sampleDetail' : self.sample_detail,
            'attributes' : map(lambda attribute: attribute.to_dict(), self.attributes),
            'alias' : self.alias
            }
        
    def to_xml(self):
        pass
        