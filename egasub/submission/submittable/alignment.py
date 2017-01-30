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
        self._analysis = EAnalysis.from_dict(self.metadata.get('analysis'))
        self._analysis.files = map(lambda file_: EFile.from_dict(file_), self.metadata.get('files'))
        
    def validate(self,ega_enums):
        # Gender validation
        if not any(gender['tag'] == str(self.sample.gender_id) for gender in ega_enums.lookup("genders")):
            self.add_local_validation_errors("sample",self.sample.alias,"gender","Invalid gender value")
            
        # Case or control validation
        if not any(cc['tag'] == str(self.sample.case_or_control_id) for cc in ega_enums.lookup("case_control")):
            self.add_local_validation_errors("sample",self.sample.alias,"case_or_control","Invalid case or control value")
            
        # Analysis type validation
        if not any(cc['tag'] == str(self.analysis.analysis_type_id) for cc in ega_enums.lookup("analysis_types")):
            self.add_local_validation_errors("analysis",self.analysis.alias,"analysis_types","Invalid analysis type value")
            
        # Reference genomes type validation
        if not any(cc['tag'] == str(self.analysis.genome_id) for cc in ega_enums.lookup("reference_genomes")):
            self.add_local_validation_errors("analysis",self.analysis.alias,"reference_genomes","Invalid reference genome type value")
            
        # Reference genomes type validation
        if not any(cc['tag'] == str(self.analysis.experiment_type_id) for cc in ega_enums.lookup("experiment_types")):
            self.add_local_validation_errors("analysis",self.analysis.alias,"experiment_types","Invalid experiment type value")
        
        #TODO
        # Chromosome references validation    
        #if not any(cc['tag'] == str(self.analysis.experiment_type_id) for cc in ega_enums.lookup("experiment_types")):
        #    self.add_local_validation_errors("analysis",self.analysis.alias,"experiment_types","Invalid experiment type value")
            
            
        
        

    @property
    def type(self):
        return self.__class__.__bases__[0].__name__.lower()

    @property
    def sample(self):
        return self._sample

    @property
    def analysis(self):
        return self._analysis
