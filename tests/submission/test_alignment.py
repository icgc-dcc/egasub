import pytest
import os
from egasub.submission.submittable import Alignment
from egasub.ega.entities import Sample, \
                                Analysis as EAnalysis

def test_alignment():
    initial_directory = os.getcwd()
    os.chdir('tests/data/workspace/alignment.20170115/')
    alignment = Alignment('test_x')

    assert isinstance(alignment.sample, Sample)
    assert isinstance(alignment.analysis, EAnalysis)

    reference_sample = {
        'genderId': 1,
        'status': None,
        'cellLine' : None,
        'description': None,
        'sampleAge': None,
        'title': None,
        'region': None,
        'subjectId': None,
        'organismPart': None,
        'alias': 'test_x',
        'caseOrControlId': 0,
        'id': None,
        'phenotype': 'Breast cancer',
        'attributes': [],
        'bioSampleId': None,
        'anonymizedName': None,
        'sampleDetail': None,
        'egaAccessionId':None
    }

    reference_analysis = {
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
        'egaAccessionId': None,
        'files': [
            {
                'unencryptedChecksum': '5e0024389829a7b131fed6476f7e71c4',
                'checksum': '5e0024389829a7b131fed6476f7e71c4',
                'fileName': 'alignment.20170115/test_x/sequence_file.single_end.test_x.bam.gpg',
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

    assert cmp(alignment.sample.to_dict(),reference_sample) == 0
    assert cmp(alignment.analysis.to_dict(),reference_analysis)  == 0

    # Check if the md5 checksum is missing in the file
    with pytest.raises(Exception):
        alignment = Alignment('sample_bad')

    # Check if the folder name is malformed
    with pytest.raises(Exception):
        alignment = Alignment('samplebad$2')

    # Check if the folder exists
    with pytest.raises(Exception):
        alignment = Alignment('sample_bad_99')

    # Missing analysis.yaml file
    with pytest.raises(Exception):
        alignment = Alignment('sample_bad3')

    os.chdir(initial_directory)
            