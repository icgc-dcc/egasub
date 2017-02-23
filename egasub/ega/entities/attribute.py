
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
    def from_dict(attr_dict):
        return Attribute(attr_dict.get('tag'),attr_dict.get('value'),attr_dict.get('unit'))
