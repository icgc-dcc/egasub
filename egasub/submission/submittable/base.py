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

    @property
    def local_validation_errors(self):
        return self._local_validation_errors

    def _add_local_validation_errors(self, type_, alias, field, message):
        self._local_validation_errors.append({
                "object_type" : type_,
                "object_alias": alias,
                "field": field,
                "error": message
            })

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

    @abstractmethod
    def local_validate(self):
        pass

    def _check_status(self):
        """
        This will check local log info to get the status
        """
        # hardcode to 'NEW' for now
        return 'NEW'

class Experiment(Submittable):
    @property
    def sample(self):
        return self._sample

    @property
    def experiment(self):
        return self._experiment

    @property
    def run(self):
        return self._run

    def local_validate(self, ega_enums):
        # Gender validation
        if not any(gender['tag'] == str(self.sample.gender_id) for gender in ega_enums.lookup("genders")):
            self._add_local_validation_errors("sample",self.sample.alias,"gender","Invalid value '%s'" % self.sample.gender_id)

        # Case or control validation
        if not any(cc['tag'] == str(self.sample.case_or_control_id) for cc in ega_enums.lookup("case_control")):
            self._add_local_validation_errors("sample",self.sample.alias,"case_or_control","Invalid value '%s'" % self.sample.case_or_control_id)

        # Instrument model validation
        if not any(model['tag'] == str(self.experiment.instrument_model_id) for model in ega_enums.lookup("instrument_models")):
            self._add_local_validation_errors("experiment",self.experiment.alias,"instrument_model","Invalid instrument model value")

        # Library source validation
        if not any(source['tag'] == str(self.experiment.library_source_id) for source in ega_enums.lookup("library_sources")):
            self._add_local_validation_errors("experiment",self.experiment.alias,"library_sources","Invalid library source value")

        # Library selection validation
        if not any(selection['tag'] == str(self.experiment.library_selection_id) for selection in ega_enums.lookup("library_selections")):
            self._add_local_validation_errors("experiment",self.experiment.alias,"library_selection","Invalid library selection value")

        # Library strategy validation
        if not any(strategy['tag'] == str(self.experiment.library_strategy_id) for strategy in ega_enums.lookup("library_strategies")):
            self._add_local_validation_errors("experiment",self.experiment.alias,"library_strategies","Invalid library strategy value")

        # Run file type validation
        if not any(file_type['tag'] == str(self.run.run_file_type_id) for file_type in ega_enums.lookup("file_types")):
            self._add_local_validation_errors("run",self.experiment.alias,"file_types","Invalid file types value")


class Analysis(Submittable):
    @property
    def analysis(self):
        return self._analysis

    def local_validate(self,ega_enums):
        # Analysis type validation
        if not any(cc['tag'] == str(self.analysis.analysis_type_id) for cc in ega_enums.lookup("analysis_types")):
            self._add_local_validation_errors("analysis",self.analysis.alias,"analysis_types","Invalid value '%s'" % self.analysis.analysis_type_id)

        # Reference genomes type validation
        if not any(cc['tag'] == str(self.analysis.genome_id) for cc in ega_enums.lookup("reference_genomes")):
            self._add_local_validation_errors("analysis",self.analysis.alias,"reference_genomes","Invalid reference genome type value")

        # Reference genomes type validation
        if not any(cc['tag'] == str(self.analysis.experiment_type_id) for cc in ega_enums.lookup("experiment_types")):
            self._add_local_validation_errors("analysis",self.analysis.alias,"experiment_types","Invalid value '%s'" % self.analysis.experiment_type_id)

        #TODO
        # Chromosome references validation
        #if not any(cc['tag'] == str(self.analysis.experiment_type_id) for cc in ega_enums.lookup("experiment_types")):
        #    self._add_local_validation_errors("analysis",self.analysis.alias,"experiment_types","Invalid experiment type value")


