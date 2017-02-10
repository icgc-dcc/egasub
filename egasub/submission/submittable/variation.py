from .base import Analysis

class Variation(Analysis):
    def local_validate(self, ega_enums):
        super(Variation, self).local_validate(ega_enums)
        # Analysis type validation, 1 - Sequence variation (VCF)
        if not str(self.analysis.analysis_type_id) == "1":
            self._add_local_validation_error("analysis",self.analysis.alias,"analysisTypes", "Invalid value '%s', analysisTypeId must be '1' for variation data." % self.analysis.analysis_type_id)

