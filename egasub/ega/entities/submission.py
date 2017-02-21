
class Submission(object):
    def __init__(self,title, description,submission_subset):
        self.title = title
        self.description = description
        self.submission_subset = submission_subset

    def to_dict(self):
        return {
            "title" : self.title,
            "description" : self.description,
            "submissionSubset" : self.submission_subset.to_dict()
            }

    def to_xml(self):
        pass