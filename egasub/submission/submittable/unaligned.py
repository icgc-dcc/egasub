from .base import Experiment
from egasub.ega.entities import Sample, \
                                Run as ERun, \
                                File as EFile, \
                                Experiment as EExperiment
from egasub.ega.services.ftp import file_exists


class Unaligned(Experiment):
    def __init__(self, path):
        self._local_validation_errors = []
        self._ftp_file_validation_errors = []
        self._path = path

        try:
            self._parse_meta()

            self._sample = Sample.from_dict(self.metadata.get('sample'))
            self.restore_latest_object_status('sample')

            self._experiment = EExperiment.from_dict(self.metadata.get('experiment'))
            self.restore_latest_object_status('experiment')

            self._run = ERun.from_dict(self.metadata.get('run'))
            self.restore_latest_object_status('run')

            self._run.files = map(lambda file_: EFile.from_dict(file_), self.metadata.get('files'))
        except Exception, err:
            raise Exception("Can not create 'unaligned' submission from this directory: %s. Please verify it's content. Error: %s" % (self._path, err))

    @property
    def status(self):
        if self.run.status:
            return self.run.status
        else:
            return 'NEW'  # hardcoded for now

    @property
    def files(self):
        return self._run.files

    @property
    def type(self):
        return self.__class__.__bases__[0].__name__.lower()

    def ftp_files_remote_validate(self,host,username, password):
        for _file in self._run.files:
            if not file_exists(host,username,password,_file.file_name):
                self._add_ftp_file_validation_error("fileName","File missing on FTP ega server: %s" % _file.file_name)