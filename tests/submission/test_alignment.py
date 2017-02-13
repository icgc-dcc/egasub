import pytest
import os
from egasub.submission.submittable import Alignment
from egasub.ega.entities import Sample, \
                                Experiment as EExperiment, \
                                Analysis as EAnalysis
from egasub.exceptions import Md5sumFileError
import json


def test_alignment():
    initial_directory = os.getcwd()
    os.chdir('tests/data/workspace/alignment.20170115/')
    alignment = Alignment('sample_x')
    os.chdir(initial_directory)

    assert isinstance(alignment.sample, Sample)
    assert isinstance(alignment.analysis, EAnalysis)
    
    assert cmp(
                alignment.sample.to_dict(),
                {
                    'genderId': 1,
                    'status': None,
                    'cellLine' : None,
                    'description': None,
                    'sampleAge': None,
                    'title': None,
                    'region': None,
                    'subjectId': None,
                    'organismPart': None,
                    'alias': 'sample_x',
                    'caseOrControlId': 0,
                    'id': None,
                    'phenotype': 'Breast cancer',
                    'attributes': [],
                    'bioSampleId': None,
                    'anonymizedName': None,
                    'sampleDetail': None
                }
            ) == 0
                        
    assert cmp(
                alignment.analysis.to_dict(),
                {
                    'title': 'The title of the analysis',
                    'description': 'description',
                    'alias': None,
                    'studyId': None,
                    'sampleReferences': [],
                    'analysisCenter': 'analysis_center',
                    'analysisDate': 'analysis_date',
                    'analysisTypeId': 0,
                    'experimentTypeId' : [0],
                    'status': None,
                    'files': [
                        {
                            'unencryptedChecksum': '5e0024389829a7b131fed6476f7e71c4',
                            'checksum': '5e0024389829a7b131fed6476f7e71c4',
                            'fileName': 'alignment.20170115/sample_x/sequence_file.single_end.sample_x.bam.gpg',
                            'checksumMethod': 'md5',
                            'fileId': None
                        }
                    ],
                    'genomeId': 15,
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
            )  == 0
            