from .base import Experiment
from egasub.ega.entities import Sample, \
                                Run as ERun, \
                                File as EFile, \
                                Experiment as EExperiment


class Unaligned(Experiment):
    def __init__(self, path):
        self._local_validation_errors = []
        self._path = path
        self._parse_meta()
        self._status = self._check_status()

        self._sample = Sample.from_dict(self.metadata.get('sample'))
        self._experiment = EExperiment.from_dict(self.metadata.get('experiment'))
        self._run = ERun.from_dict(self.metadata.get('run'))
        self._run.files = map(lambda file_: EFile.from_dict(file_), self.metadata.get('files'))

    @property
    def type(self):
        return self.__class__.__bases__[0].__name__.lower()

