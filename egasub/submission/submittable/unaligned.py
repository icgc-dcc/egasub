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

    @property
    def sample(self):
        return self._sample

    @property
    def experiment(self):
        return self._experiment

    @property
    def run(self):
        return self._run
    
    def validate(self, ega_enums):
        
        # Gender validation
        if not any(gender['tag'] == str(self.sample.gender_id) for gender in ega_enums.lookup("genders")):
            self.add_local_validation_errors("sample",self.sample.alias,"gender","Invalid gender value")
            
        # Case or control validation
        if not any(cc['tag'] == str(self.sample.case_or_control_id) for cc in ega_enums.lookup("case_control")):
            self.add_local_validation_errors("sample",self.sample.alias,"case_or_control","Invalid case or control value")
            
        # Instrument model validation
        if not any(model['tag'] == str(self.experiment.instrument_model_id) for model in ega_enums.lookup("instrument_models")):
            self.add_local_validation_errors("experiment",experiment.alias,"instrument_model","Invalid instrument model value")
            
        # Library source validation
        if not any(source['tag'] == str(self.experiment.library_source_id) for source in ega_enums.lookup("library_sources")):
            self.add_local_validation_errors("experiment",experiment.alias,"library_sources","Invalid library source value")
            
        # Library selection validation
        if not any(selection['tag'] == str(self.experiment.library_selection_id) for selection in ega_enums.lookup("library_selections")):
            self.add_local_validation_errors("experiment",experiment.alias,"library_selection","Invalid library selection value")
            
        # Library strategy validation
        if not any(strategy['tag'] == str(self.experiment.library_strategy_id) for strategy in ega_enums.lookup("library_strategies")):
            self.add_local_validation_errors("experiment",experiment.alias,"library_strategies","Invalid library strategy value")
            
        # Run file type validation
        if not any(file_type['tag'] == str(self.run.run_file_type_id) for file_type in ega_enums.lookup("file_types")):
            self.add_local_validation_errors("run",experiment.alias,"file_types","Invalid file types value")

