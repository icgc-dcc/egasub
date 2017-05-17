import pytest
import os
from egasub.submission.submittable import Variation
from egasub.ega.entities import Sample, EgaEnums, \
                                Analysis as EAnalysis
from egasub import __version__ as ver
#from egasub.exceptions import Md5sumFileError


def test_variation():
    initial_directory = os.getcwd()
    os.chdir('tests/data/workspace/variation.20170119/')
    variation = Variation('test_x')

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
        'alias': 'test_x',
        'caseOrControlId': 0,
        'id': None,
        'phenotype': 'Breast cancer',
        'attributes': [],
        'bioSampleId': None,
        'anonymizedName': None,
        'status': None,
        'sampleDetail': None,
        'egaAccessionId': None
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
        'egaAccessionId': None,
        'files': [
            {
                'unencryptedChecksum': '5e0024389829a7b131fed6476f7e71c4',
                'checksum': '5e0024389829a7b131fed6476f7e71c4',
                'fileName': 'variation.20170119/test_x/somatic.snv.test_x.vcf.gz.gpg',
                'checksumMethod': 'md5',
                'fileId': None
            },
            {
                'unencryptedChecksum': '5e0024389829a7b131fed6476f7e71c4',
                'checksum': '5e0024389829a7b131fed6476f7e71c4',
                'fileName': 'variation.20170119/test_x/somatic.snv.test_x.vcf.gz.tbi.gpg',
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
            {'tag':'_submitted_using','unit':None,'value':'egasub %s' % ver}
        ]
    }

    variation._add_local_validation_error("type", "alias", "field", "message")

    assert cmp(variation.sample.to_dict(),reference_sample) == 0
    assert cmp(variation.analysis.to_dict(), reference_analysis)  == 0
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

    # Cannot contain '/'
    with pytest.raises(Exception):
        variation = Variation('sdf/df/ff/')

    with pytest.raises(Exception):
        variation = Variation('test_@')

    assert variation.status == 'NEW'

    assert variation.files == variation.analysis.files

    variation.local_validate(EgaEnums())

    os.chdir(initial_directory)
    os.chdir('tests/data/workspace/alignment.20170115/')

    variation = Variation('test_x')

    variation.local_validate(EgaEnums())

    os.chdir(initial_directory)
