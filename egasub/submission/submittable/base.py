import os
import re
import yaml
import time
from abc import ABCMeta, abstractproperty

from egasub.exceptions import Md5sumFileError
from egasub.ega.entities import Sample, Attribute, \
                                Run as ERun, \
                                File as EFile, \
                                Analysis as EAnalysis, \
                                Experiment as EExperiment
from egasub.ega.services.ftp import file_exists
from egasub import __version__ as ver


def _get_md5sum(md5sum_file):
    try:
        checksum = open(md5sum_file, 'r').readline().rstrip()
    except:
        raise Md5sumFileError("Please make sure md5sum file '%s' exist" % md5sum_file)

    if not re.findall(r"^[a-fA-F\d]{32}$", checksum):
        raise Md5sumFileError("Please make sure md5sum file '%s' contain valid md5sum string" % md5sum_file)
    return checksum.lower()


class Submittable(object):
    __metaclass__ = ABCMeta

    def __init__(self, path):
        path = path.rstrip('/')
        if '/' in path:
            raise Exception("Submission directory '%s' can not contain '/'" % path)

        if path.upper().startswith('SA'):  # we may want to make this configurable to allow it turned off for non-ICGC submitters
            raise Exception("Submission directory '%s' can not start with 'SA' or 'sa', this is reserved for ICGC DCC." % path)

        if path.upper().startswith('EGA'):
            raise Exception("Submission directory '%s' can not start with 'EGA' or 'ega', this is reserved for EGA." % path)

        self._local_validation_errors = []
        self._ftp_file_validation_errors = []
        self._path = path

    @property
    def path(self):
        return self._path

    @property
    def submission_dir(self):
        return os.path.basename(self._path)

    @property
    def submission_batch(self):
        return os.path.basename(os.getcwd())

    @property
    def type(self):
        return self.__class__.__name__.lower()

    @property
    def metadata(self):
        return self._metadata

    @abstractproperty
    def status(self):
        return

    @abstractproperty
    def files(self):
        return

    @property
    def local_validation_errors(self):
        return self._local_validation_errors

    @property
    def ftp_file_validation_errors(self):
        return self._ftp_file_validation_errors

    def _add_local_validation_error(self, type_, alias, field, message):
        self._local_validation_errors.append({
                "object_type" : type_,
                "object_alias": alias,
                "field": field,
                "error": message
            })

    def _add_ftp_file_validation_error(self,field,message):
        self._ftp_file_validation_errors.append({
                "field": field,
                "error": message
            })

    def _parse_meta(self):
        yaml_file = os.path.join(self.path, '.'.join([self.type, 'yaml']))
        try:
            with open(yaml_file, 'r') as yaml_stream:
                self._metadata = yaml.safe_load(yaml_stream)

            # some basic validation of the YAML
            if self.type == 'experiment':
                if 'alias' in self._metadata.get('experiment', {}):
                    raise Exception("Can not have 'alias' for 'experiment' in %s." % yaml_file)
                if 'alias' in self._metadata.get('run', {}):
                    raise Exception("Can not have 'alias' for 'run' in %s." % yaml_file)
            if self.type == 'analysis':
                if 'alias' in self._metadata.get('analysis', {}):
                    raise Exception("Can not have 'alias' for 'analysis' in %s." % yaml_file)

        except Exception, e:
            raise Exception('Not a properly formed submission directory: %s. Please make sure YAML is well-formed. Error: %s' % (self.submission_dir, e))

        self._parse_md5sum_file()


    def _parse_md5sum_file(self):
        """
        parse md5sum file(s) to get checksum and unencryptedChecksum
        """
        for f in self.metadata.get('files'):
            # sequence_file.paired_end.sample_y.fq.gz.gpg
            if not f.get('fileName'):
                # echo('Skip file entry without fileName specified.')  # for debug
                continue
            data_file_name = os.path.basename(f.get('fileName'))
            md5sum_file = os.path.join(self.path, data_file_name + '.md5')
            f['checksumMethod'] = 'md5'
            f['checksum'] = _get_md5sum(md5sum_file)
            f['checksum'] = _get_md5sum(md5sum_file)

            unencrypt_md5sum_file = os.path.join(self.path, re.sub(r'\.gpg$', '', data_file_name) + '.md5')
            f['unencryptedChecksum'] = _get_md5sum(unencrypt_md5sum_file)

    def restore_latest_object_status(self, obj_type):
        if not obj_type in ('sample', 'analysis', 'experiment', 'run'):
            return

        obj = getattr(self, obj_type)

        status_file = os.path.join(self.path, '.status', '%s.log' % obj_type)

        try:
            with open(status_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    line = lines[-1].rstrip('\n')
                    status_values = line.split('\t')
                    id_, alias, status, timestamp, op_type, session_id, log_file, ega_accession_id = \
                        (lambda a,b,c,d=None,e=None,f=None,g=None,h=None: (a,b,c,d,e,f,g,h))(*status_values[0:8]) # this is mostly for backward compatibility, earlier versions may have fewer columns
                    if obj.alias and not obj.alias == alias:
                        pass # alias has changed, this should never happen, if it does, we simply ignore and do not restore the status
                    else:  # never restore object id, which should always be taken from the server side
                        obj.alias = alias
                        obj.status = status  # we need to get status at last operation with EGA, it will be used to decide whether it's ready for performing submission
                        obj.ega_accession_id = ega_accession_id
        except Exception:
            pass

    def record_object_status(self, obj_type, dry_run, submission_session, log_file, ega_accession_id=None):
        if not obj_type in ('sample', 'analysis', 'experiment', 'run'):
            return

        status_dir = os.path.join(self.path, '.status')

        if not os.path.exists(status_dir):
            os.makedirs(status_dir)

        status_file = os.path.join(status_dir, '%s.log' % obj_type)

        obj = getattr(self, obj_type)

        op_type = 'dry_run' if dry_run else 'submit'

        if ega_accession_id == None: ega_accession_id = ""

        with open(status_file, 'a') as f:
            f.write("%s\n" % '\t'.join([str(obj.id), str(obj.alias), str(obj.status), str(int(time.time())), op_type, submission_session, log_file, ega_accession_id]))

    def local_validate(self, ega_enums):
        # Alias validation
        sample_alias_in_sub_dir = self.submission_dir.split('.')[0]  # first portion is sample alias
        if not self.sample.alias:
            self._add_local_validation_error("sample",self.sample.alias,"alias","Invalid value '%s'. Sample alias must be set" % (self.sample.alias))
            return  # no need to move on

        if self.sample.alias != sample_alias_in_sub_dir:
            self._add_local_validation_error("sample",self.sample.alias,"alias","Invalid value '%s'. Sample alias must be set and match the 'alias' portion in the submission directory '%s'." % (self.sample.alias, sample_alias_in_sub_dir))

        if not re.match(r'^[a-zA-Z0-9_\-]+$', self.sample.alias):  # validate sample alias pattern
            self._add_local_validation_error("sample",self.sample.alias,"alias","Invalid value '%s'. Sample alias must only contain [a-zA-Z0-9], underscore (_) or dash (-)." % self.sample.alias)

        # subjustId validation
        if not self.sample.subject_id:
            self._add_local_validation_error("sample",self.sample.alias,"subjectId","Invalid value, sample's subjectId must be set.")
        # subjustId validation: can not start with DO/do/Do/dO
        elif str(self.sample.subject_id).upper().startswith('DO'):
            self._add_local_validation_error("sample",self.sample.alias,"subjectId","Invalid value, sample's subjectId can not start with 'DO', this is reserved for ICGC DCC.")

        # Gender validation
        if not any(gender['tag'] == str(self.sample.gender_id) for gender in ega_enums.lookup("genders")):
            self._add_local_validation_error("sample",self.sample.alias,"gender","Invalid value '%s'" % self.sample.gender_id)

        # Case or control validation
        if not any(cc['tag'] == str(self.sample.case_or_control_id) for cc in ega_enums.lookup("case_control")):
            self._add_local_validation_error("sample",self.sample.alias,"caseOrControl","Invalid value '%s'" % self.sample.case_or_control_id)

        # phenotype validation
        if not self.sample.phenotype:
            self._add_local_validation_error("sample",self.sample.alias,"phenotype","Invalid value, sample's phenotype must be set.")

        # validate file
        if not self.files:
            self._add_local_validation_error("file",None,"files.fileName","File(s) must be set.")

        # validate file path
        expected_file_path_start = "%s/%s/" % (self.submission_batch, self.submission_dir)
        for f in self.files:
            if not f or not f.file_name or not f.file_name.startswith(expected_file_path_start):
                self._add_local_validation_error("file",None,"files.fileName","File path incorrect for '%s', expected file path starts with '%s'" % (f.file_name, expected_file_path_start))

    # TODO: should move this to file check as part of local validation, will need to come up with a way
    #       to pass in credentials, currently 'submittable' object has no access to such information
    def ftp_files_remote_validate(self,host,username, password):
        for file_ in self.files:
            if not file_exists(host,username,password,file_.file_name):
                self._add_ftp_file_validation_error("fileName","File missing on FTP ega server: %s. Make sure this file has been uploaded to EGA FTP server" % file_.file_name)


class Experiment(Submittable):
    __metaclass__ = ABCMeta

    def __init__(self, path):
        super(Experiment, self).__init__(path)

        if not re.match(r'^[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+){0,1}$', self.submission_dir):
            raise Exception("Submission directory should be named as <sample alias> or <sample alias>.<lane label>, sample alias and lane label may only contain letter, digit, underscore (_) or dash (-)")

        try:
            self._parse_meta()

            self._sample = Sample.from_dict(self.metadata.get('sample'))
            self.restore_latest_object_status('sample')

            self._experiment = EExperiment.from_dict(self.metadata.get('experiment'))
            self.restore_latest_object_status('experiment')

            self._run = ERun.from_dict(self.metadata.get('run'))
            self.restore_latest_object_status('run')

            self.run.files = [EFile.from_dict(file_) for file_ in self.metadata.get('files')]
        except Exception, err:
            raise Exception("Can not create submission from this directory: %s. Please verify it's content. Error: %s" % (self._path, err))

    @property
    def status(self):
        if self.run.status:
            return self.run.status
        else:
            return 'NEW'

    @property
    def files(self):
        return self.run.files

    @property
    def type(self):
        return self.__class__.__bases__[0].__name__.lower()

    @property
    def sample(self):
        return self._sample

    @property
    def experiment(self):
        return self._experiment

    @property
    def run(self):
        return self._run

    # Future todo: move these validations to a new Validator class
    def local_validate(self, ega_enums):
        super(Experiment, self).local_validate(ega_enums)

        # submission_dir validate
        submission_dir_parts = self.submission_dir.split('.')
        if len(submission_dir_parts) > 2:  # more than 2 parts
            self._add_local_validation_error("submission_dir",self.submission_dir,"submission_dir","Submission directory for EGA Experiment must follow this naming pattern 'sample_alias[.line_label] (line_label is optional)'. Incorrect directory name: %s" % self.submission_dir)

        # Instrument model validation
        if not any(model['tag'] == str(self.experiment.instrument_model_id) for model in ega_enums.lookup("instrument_models")):
            self._add_local_validation_error("experiment",self.experiment.alias,"instrumentModel","Invalid value '%s'" % self.experiment.instrument_model_id)

        # Library name validation
        if not self.experiment.library_name:
            self._add_local_validation_error("experiment",self.experiment.alias,"libraryName","Invalid value, library name must be provided")

        # Experiment design description validation
        if not self.experiment.design_description:
            self._add_local_validation_error("experiment",self.experiment.alias,"designDescription","Invalid value, design description must be provided")

        # Library source validation
        if not any(source['tag'] == str(self.experiment.library_source_id) for source in ega_enums.lookup("library_sources")):
            self._add_local_validation_error("experiment",self.experiment.alias,"librarySources","Invalid value '%s'" % self.experiment.library_source_id)

        # Library selection validation
        if not any(selection['tag'] == str(self.experiment.library_selection_id) for selection in ega_enums.lookup("library_selections")):
            self._add_local_validation_error("experiment",self.experiment.alias,"librarySelection","Invalid value '%s'" % self.experiment.library_selection_id)

        # Library strategy validation
        if not any(strategy['tag'] == str(self.experiment.library_strategy_id) for strategy in ega_enums.lookup("library_strategies")):
            self._add_local_validation_error("experiment",self.experiment.alias,"libraryStrategies","Invalid value '%s'" % self.experiment.library_strategy_id)

        # Library layout validation
        if not any(layout['tag'] == str(self.experiment.library_layout_id) for layout in ega_enums.lookup("library_layouts")):
            self._add_local_validation_error("experiment",self.experiment.alias,"libraryLayoutId","Invalid value '%s'" % self.experiment.library_layout_id)

        # Run file type validation
        if not any(file_type['tag'] == str(self.run.run_file_type_id) for file_type in ega_enums.lookup("file_types")):
            self._add_local_validation_error("run",self.run.alias,"runFileTypeId","Invalid value '%s'" % self.run.run_file_type_id)


class Analysis(Submittable):
    __metaclass__ = ABCMeta

    def __init__(self, path):
        super(Analysis, self).__init__(path)

        try:
            self._parse_meta()

            self._sample = Sample.from_dict(self.metadata.get('sample'))
            self.restore_latest_object_status('sample')

            self._analysis = EAnalysis.from_dict(self.metadata.get('analysis'))
            self.restore_latest_object_status('analysis')

            self._analysis.files = [EFile.from_dict(file_) for file_ in self.metadata.get('files')]

            # not sure for what reason, EGA validation expect to have at least one attribute
            self.analysis.attributes = [
                Attribute('_submitted_using', 'egasub %s' % ver)
            ]
        except Exception, err:
            raise Exception("Can not create submission from this directory: %s. Please verify it's content. Error: %s" % (self._path, err))


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
        return self.analysis.files

    @property
    def sample(self):
        return self._sample

    @property
    def analysis(self):
        return self._analysis

    def local_validate(self, ega_enums):
        super(Analysis, self).local_validate(ega_enums)

        # Reference genomes type validation
        if not any(cc['tag'] == str(self.analysis.genome_id) for cc in ega_enums.lookup("reference_genomes")):
            self._add_local_validation_error("analysis",self.analysis.alias,"genomeId","Invalid value '%s'" % self.analysis.genome_id)

        # experimentTypeId type validation
        if not isinstance(self.analysis.experiment_type_id, list):
            self._add_local_validation_error("analysis",self.analysis.alias,"experimentTypes","Invalid value: experimentTypeId must be a list.")

        for e_type in self.analysis.experiment_type_id:
            if not any(cc['tag'] == str(e_type) for cc in ega_enums.lookup("experiment_types")):
                self._add_local_validation_error("analysis",self.analysis.alias,"experimentTypes","Invalid value '%s' in experimentTypeId." % e_type)

        # Analysis titile validation
        if not self.analysis.title:
            self._add_local_validation_error("analysis",self.analysis.alias,"title","Invalid value: analysis title must be provided.")

        # Analysis description validation
        if not self.analysis.description:
            self._add_local_validation_error("analysis",self.analysis.alias,"description","Invalid value: analysis description must be provided.")

        # Chromosome references validation
        # for some reason EGA only excepts this for variant file submission, not alignment
        # but let's put it here, so it's required for both
        if not isinstance(self.analysis.chromosome_references, list):
            self._add_local_validation_error("analysis",self.analysis.alias,"chromosomeReferences","Invalid value: chromosomeReferences must be a list.")

        for chr_ref in self.analysis.chromosome_references:
            if not any(cc['tag'] == str(chr_ref.value) for cc in ega_enums.lookup("reference_chromosomes")):
                self._add_local_validation_error("analysis",self.analysis.alias,"chromosomeReferences","Invalid value '%s' in chromosomeReferences" % chr_ref.value)

