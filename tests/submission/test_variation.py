import pytest
import os
from egasub.submission.submittable import Variation
from egasub.ega.entities import Sample, \
                                Experiment as EExperiment, \
                                Analysis as EAnalysis
from egasub.exceptions import Md5sumFileError


def test_variation():
    initial_directory = os.getcwd()
    os.chdir('tests/data/workspace/variation.20170119/')
    variation = Variation('sample_1')

    assert isinstance(variation.sample, Sample)
    assert isinstance(variation.analysis, EAnalysis)
    
    reference_sample = {
        'genderId': 1,
        'cellLine' : None,
        'description': None,
        'sampleAge': None,
        'title': None,
        'region': None,
        'subjectId': 'donor 1',
        'organismPart': None,
        'alias': 'sample_1',
        'caseOrControlId': 0,
        'id': None,
        'phenotype': 'Breast cancer',
        'attributes': [],
        'bioSampleId': None,
        'anonymizedName': None,
        'status': None,
        'sampleDetail': None
    }
    
    reference_analysis = {
        'title': 'The title of the analysis',
        'description': 'description',
        'alias': None,
        'studyId': None,
        'sampleReferences': [],
        'analysisCenter': 'analysis_center',
        'analysisDate': None,
        'analysisTypeId': 1,
        'experimentTypeId' : [0],
        'status': None,
        'files': [
            {
                'unencryptedChecksum': '5e0024389829a7b131fed6476f7e71c4',
                'checksum': '5e0024389829a7b131fed6476f7e71c4',
                'fileName': 'variation.20170119/sample_1/somatic.snv.sample_1.vcf.gz.gpg',
                'checksumMethod': 'md5',
                'fileId': None
            },
            {
                'unencryptedChecksum': '5e0024389829a7b131fed6476f7e71c4',
                'checksum': '5e0024389829a7b131fed6476f7e71c4',
                'fileName': 'variation.20170119/sample_1/somatic.snv.sample_1.vcf.gz.tbi.gpg',
                'checksumMethod': 'md5',
                'fileId': None
            }
        ],
        'genomeId': 1,
        'chromosomeReferences': [
            {'value':24,'label':None},
            {'value':25,'label':None},
            {'value':26,'label':None}
        ],
        'platform': 'Illumina HiSeq 2000',
        'attributes': [
            {'tag':'submitted_using','unit':None,'value':'egasub'}
        ]
    }
    
    variation._add_local_validation_error("type", "alias", "field", "message")

    assert cmp(variation.sample.to_dict(),reference_sample) == 0
    assert cmp(variation.analysis.to_dict(),reference_analysis)  == 0
    assert variation.local_validation_errors[0] == {'object_alias':'alias','field':'field','object_type':'type','error':'message'}    

    # Check if the md5 checksum is missing in the file
    with pytest.raises(Exception):
        variation = Variation('sample_bad')
        
    # Check if the folder name is malformed
    with pytest.raises(Exception):
        variation = Variation('sample_bad2$')
        
    # Missing experiment.yaml file    
    with pytest.raises(Exception):    
        variation = Variation('sample_bad3')
        
    # Check if the folder exists
    with pytest.raises(Exception):    
        variation = Variation('sample_bad_99')
            
    os.chdir(initial_directory)