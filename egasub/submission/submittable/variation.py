import re
from .base import Analysis

class Variation(Analysis):
    def __init__(self, path):
        super(Variation, self).__init__(path)

        if not re.match(r'^[a-zA-Z0-9_\-]+$', self.submission_dir):
            raise Exception("Submission directory should be named as <sample alias>, sample alias may only contain letter, digit, underscore (_) or dash (-)")


    def local_validate(self, ega_enums):
        super(Variation, self).local_validate(ega_enums)
        # Analysis type validation, 1 - Sequence variation (VCF)
        if not str(self.analysis.analysis_type_id) == "1":
            self._add_local_validation_error("analysis",self.analysis.alias,"analysisTypes", "Invalid value '%s', analysisTypeId must be '1' for variation data." % self.analysis.analysis_type_id)

        # chromosomeReferences can not be empty list
        if not self.analysis.chromosome_references:
            self._add_local_validation_error("analysis",self.analysis.alias,"chromosomeReferences","Invalid value, chromosomeReferences can not be an empty list.")

        # experimentTypeId can not be empty list
        if not self.analysis.experiment_type_id:
            self._add_local_validation_error("analysis",self.analysis.alias,"experimentTypes","Invalid value, experimentTypes can not be an empty list.")
