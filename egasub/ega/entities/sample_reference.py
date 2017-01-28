import yaml


class SampleReference(object):
    def __init__(self,value,label):
        self.value = value
        self.label = label
        
    def to_dict(self):
        return {
            'value' : self.value,
            'label' : self.label
            }
        
    def to_xml(self):
        pass
        
    @staticmethod
    def load_list_from_yaml(ctx, yaml_path):
        references = []
        with open(yaml_path, 'r') as stream:
            yaml_stream = yaml.load(stream)
            
        if not yaml_stream.get('sample_references'):
            return references
            
        yaml_references = yaml_stream.get('sample_references')
        
        for reference in yaml_references:
            references.append(SampleReference(reference.get('value'),reference.get('label')))
        return references
