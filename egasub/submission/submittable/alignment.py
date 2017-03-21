import re
from .base import Analysis


class Alignment(Analysis):
    def __init__(self, path):
        super(Alignment, self).__init__(path)

        if not re.match(r'^[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+){0,1}$', self.submission_dir):
            raise Exception("Submission directory should be named as <sample alias> or <sample alias>.<lane label>, sample alias and lane label may only contain letter, digit, underscore (_) or dash (-)")


    def local_validate(self, ega_enums):
        super(Alignment, self).local_validate(ega_enums)
        # Analysis type validation, 0 - Reference Alignment (BAM)
        if not str(self.analysis.analysis_type_id) == "0":
            self._add_local_validation_error("analysis",self.analysis.alias,"analysisTypes", "Invalid value '%s', analysisTypeId must be '0' for alignment data." % self.analysis.analysis_type_id)
