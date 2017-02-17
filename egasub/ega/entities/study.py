
class Study(object):
    def __init__(self,alias,study_type_id, short_name, title, study_abstract, own_term, pub_med_ids,custom_tags, id_):
        self.alias = alias
        self.study_type_id = study_type_id
        self.short_name = short_name
        self.title = title
        self.study_abstract = study_abstract
        self.own_term = own_term
        self.pub_med_ids = pub_med_ids
        self.custom_tags = custom_tags
        self.id = id_

    def to_dict(self):
        return {
            'alias' : self.alias,
            'studyTypeId' : self.study_type_id,
            'shortName' : self.short_name,
            'title' : self.title,
            'studyAbstract' : self.study_abstract,
            'ownTerm' : self.own_term,
            'pubMedIds' : self.pub_med_ids,
            'customTags' : map(lambda tag: tag.to_dict(), self.custom_tags),
            'id' : self.id
            }


    def to_xml(self):
        pass