import yaml

class Attribute(object):
    def __init__(self, tag, value="", unit=None):
        self.tag = tag
        self.value = value
        self.unit = unit


    def to_dict(self):
        return {
            "tag": self.tag,
            "value": self.value,
            "unit": self.unit
        }


    def to_xml(self):
        xml_string = "<TAG>%s</TAG>\n<VALUE>%s</VALUE>\n" % (self.tag, self.value)
        if self.unit is not None:
            xml_string += "<UNIT>%s</UNIT>\n" % (self.unit)
        return xml_string
    
    @staticmethod
    def load_list_from_yaml(ctx, yaml_path):
        attributes = []
        with open(yaml_path, 'r') as stream:
            yaml_stream = yaml.load(stream)
            
        if not yaml_stream.get('attributes'):
            return attributes
            
        yaml_attributes = yaml_stream.get('attributes')
        
        for attribute in yaml_attributes:
            references.append(Attribute(attribute.get('tag'),attribute.get('value'),attribute.get('unit')))
        return attributes


    @staticmethod
    def from_dict(attr_dict):
        return Attribute(attr_dict.get('tag'),attr_dict.get('value'),attr_dict.get('unit'))
