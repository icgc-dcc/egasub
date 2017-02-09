from .base import Analysis

from egasub.ega.entities import Sample, Attribute, \
                                File as EFile, \
                                Analysis as EAnalysis
from egasub.ega.services.ftp import file_exists


class Alignment(Analysis):
    def __init__(self, path):
        self._local_validation_errors = []
        self._ftp_file_validation_errors = []
        self._path = path

        try:
            self._parse_meta()

            self._sample = Sample.from_dict(self.metadata.get('sample'))
            self.restore_latest_object_status('sample')

            self._analysis = EAnalysis.from_dict(self.metadata.get('analysis'))
            self.restore_latest_object_status('analysis')

            self._analysis.files = map(lambda file_: EFile.from_dict(file_), self.metadata.get('files'))

            # not sure for what reason, EGA validation expect to have at least one attribute
            self._analysis.attributes = [
                Attribute('submitted_using', 'egasub')
            ]
        except Exception, err:
            raise Exception("Can not create 'alignment' submission from this directory: %s. Please verify it's content. Error: %s" % (self._path, err))


    @property
    def status(self):
        if self.analysis.status:
            return self.analysis.status
        else:
            return 'NEW'  # hardcoded for now

    @property
    def type(self):
        return self.__class__.__bases__[0].__name__.lower()

    @property
    def files(self):
        return self._analysis.files

    @property
    def sample(self):
        return self._sample

    def ftp_files_remote_validate(self,host,username, password):
        for _file in self._analysis.files:
            if not file_exists(host,username,password,_file.file_name):
                self._add_ftp_file_validation_error("fileName","File missing on FTP ega server: %s" % _file.file_name)