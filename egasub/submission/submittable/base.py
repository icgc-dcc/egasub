import os
import re
import yaml
from abc import ABCMeta, abstractmethod, abstractproperty

from egasub.ega.entities import Sample, Analysis as EAnalysis, Experiment as EExperiment
from egasub.exceptions import Md5sumFileError

def _get_md5sum(md5sum_file):
    checksum = open(md5sum_file, 'r').readline().rstrip()
    if not re.findall(r"^[a-fA-F\d]{32}$", checksum):
        raise Md5sumFileError("Please make sure md5sum file '%s' exist and contain valid md5sum string" % md5sum_file)
    return checksum.lower()


class Submittable(object):
    __metaclass__ = ABCMeta

    @property
    def path(self):
        return self._path

    @property
    def type(self):
        return self.__class__.__name__.lower()

    @property
    def metadata(self):
        return self._metadata

    @property
    def status(self):
        return self._status

    def _parse_meta(self):
        yaml_file = os.path.join(self.path, '.'.join([self.type, 'yaml']))
        with open(yaml_file, 'r') as yaml_stream:
            self._metadata = yaml.load(yaml_stream)
        self._parse_md5sum_file()

    def _parse_md5sum_file(self):
        """
        parse md5sum file(s) to get checksum and unencryptedChecksum
        """
        for f in self.metadata.get('files'):
            # sequence_file.paired_end.sample_y.fq.gz.gpg
            data_file_name = os.path.basename(f.get('fileName'))
            md5sum_file = os.path.join(self.path, data_file_name + '.md5')
            f['checksumMethod'] = 'md5'
            f['checksum'] = _get_md5sum(md5sum_file)
            f['checksum'] = _get_md5sum(md5sum_file)

            unencrypt_md5sum_file = os.path.join(self.path, re.sub(r'\.gpg$', '', data_file_name) + '.md5')
            f['unencryptedChecksum'] = _get_md5sum(unencrypt_md5sum_file)

    def _check_status(self):
        """
        This will check local log info to get the status
        """
        # hardcode to 'NEW' for now
        return 'NEW'


class Experiment(Submittable):
    @abstractproperty
    def sample(self):
        pass

    @abstractproperty
    def experiment(self):
        pass

    @abstractproperty
    def run(self):
        pass


class Analysis(Submittable):
    @abstractproperty
    def analysis(self):
        pass

