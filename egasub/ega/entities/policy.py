

class Policy(object):
    def __init__(self, alias, dac_id, title, policy_text, url, id_=None):
        self.alias = alias
        self.dac_id = dac_id
        self.title = title
        self.policy_text = policy_text
        self.url = url
        self.id = id_

    def to_dict(self):
        return {
            'alias' : self.alias,
            'dacId' : self.dac_id,
            'title' : self.title,
            'policyText' : self.policy_text,
            'url' : self.url
            }

    def to_xml(self):
        pass