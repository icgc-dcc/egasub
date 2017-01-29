from .base import Analysis

from egasub.ega.entities import Sample, \
                                Run as ERun, \
                                File as EFile, \
                                Analysis as EAnalysis


class Alignment(Analysis):
    def __init__(self, path):
        self._path = path
        self._parse_meta()
        self._status = self._check_status()

        self._sample = Sample.from_dict(self.metadata.get('sample'))
        self._analysis = ERun.from_dict(self.metadata.get('analysis'))
        self._analysis.files = map(lambda file_: EFile.from_dict(file_), self.metadata.get('files'))

    @property
    def type(self):
        return self.__class__.__bases__[0].__name__.lower()

    @property
    def sample(self):
        return self._sample

    @property
    def analysis(self):
        return self._analysis
