import yaml

class Sample(object):
    def __init__(self,alias,title,description,case_or_control_id,gender_id,organism_part,
                 cell_line,region,phenotype, subject_id, anonymized_name, bio_sample_id,
                 sample_age, sample_detail, attributes,id):
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
        self.id = id


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
            'id' : self.id
            }


    def to_xml(self):
        pass
        
    @staticmethod
    def load_from_yaml(ctx,yaml_path):
        with open(yaml_path, 'r') as stream:
            yaml_stream = yaml.load(stream)
            
        yaml_sample = yaml_stream.get('sample')
            
        return Sample(yaml_sample.get('alias'),yaml_sample.get('title'),
                    yaml_sample.get('description'),
                    yaml_sample.get('caseOrControlId'),
                    yaml_sample.get('genderId'),
                    yaml_sample.get('organismPart'),
                    yaml_sample.get('cellLine'),
                    yaml_sample.get('region'),
                    yaml_sample.get('phenotype'),
                    yaml_sample.get('subjectId'),
                    yaml_sample.get('anonymizedName'),
                    yaml_sample.get('bioSampleId'),
                    yaml_sample.get('sampleAge'),
                    yaml_sample.get('sampleDetail'),
                    [],
                    None
        )