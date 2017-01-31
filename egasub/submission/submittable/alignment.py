from .base import Analysis

from egasub.ega.entities import Sample, \
                                File as EFile, \
                                Analysis as EAnalysis


class Alignment(Analysis):
    def __init__(self, path):
        self._local_validation_errors = []
        self._path = path
        self._parse_meta()
        self._status = self._check_status()

        self._sample = Sample.from_dict(self.metadata.get('sample'))
        self._analysis = EAnalysis.from_dict(self.metadata.get('analysis'))
        self._analysis.files = map(lambda file_: EFile.from_dict(file_), self.metadata.get('files'))

    @property
    def type(self):
        return self.__class__.__bases__[0].__name__.lower()

    @property
    def sample(self):
        return self._sample

    def local_validate(self,ega_enums):
        super(Alignment, self).local_validate(ega_enums)
        # Gender validation
        if not any(gender['tag'] == str(self.sample.gender_id) for gender in ega_enums.lookup("genders")):
            self._add_local_validation_error("sample",self.sample.alias,"gender","Invalid value '%s'" % self.sample.gender_id)

        # Case or control validation
        if not any(cc['tag'] == str(self.sample.case_or_control_id) for cc in ega_enums.lookup("case_control")):
            self._add_local_validation_error("sample",self.sample.alias,"caseOrControl","Invalid value '%s'" % self.sample.case_or_control_id)

