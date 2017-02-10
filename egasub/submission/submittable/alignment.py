from .base import Analysis


class Alignment(Analysis):

    def local_validate(self, ega_enums):
        super(Alignment, self).local_validate(ega_enums)
        # Analysis type validation, 0 - Reference Alignment (BAM)
        if not str(self.analysis.analysis_type_id) == "0":
            self._add_local_validation_error("analysis",self.analysis.alias,"analysisTypes", "Invalid value '%s', analysisTypeId must be '0' for alignment data." % self.analysis.analysis_type_id)
