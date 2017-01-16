

class Policy(object):
    def __init__(self, dac_id, title, policy_text, url):
        self.dac_id = dac_id
        self.title = title
        self.policy_text = policy_text
        self.url = url
        
    def to_dict(self):
        return {
            'dacId' : self.dac_id,
            'title' : self.title,
            'policyText' : self.policy_text,
            'url' : self.url
            }
        
    def to_xml(self):
        pass