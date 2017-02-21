import pytest
import os
from egasub.submission.submittable import Unaligned
from egasub.ega.entities import Sample, \
                                Experiment as EExperiment, \
                                Run as ERun

def test_unaligned():
    initial_directory = os.getcwd()
    os.chdir('tests/data/workspace/unaligned.20170110/')
    unaligned = Unaligned('ssample_y')

    assert isinstance(unaligned.sample, Sample)
    assert isinstance(unaligned.experiment, EExperiment)
    assert isinstance(unaligned.run, ERun)

    reference_sample = {
                    'genderId': 1,
                    'cellLine': None,
                    'description': None,
                    'sampleAge': None,
                    'title': None,
                    'region': None,
                    'subjectId': 'abc',
                    'organismPart': None,
                    'alias': 'ssample_y',
                    'caseOrControlId': 2,
                    'id': None,
                    'phenotype': 'Breast cancer',
                    'attributes': [],
                    'bioSampleId': None,
                    'anonymizedName': None,
                    'sampleDetail': None,
                    'status': None
                }

    reference_experiment = {
                    'libraryLayoutId': 1,
                    'pairedNominalLength': 420,
                    'libraryName': 'Library name',
                    'sampleId': None,
                    'instrumentModelId': 2,
                    'libraryConstructionProtocol': 'Library construction protocol',
                    'librarySelectionId': 3,
                    'title': 'The title of the experiment',
                    'designDescription': 'Description of the design',
                    'id': None,
                    'pairedNominalSdev': 36,
                    'librarySourceId': 4,
                    'studyId': None,
                    'libraryStrategyId': 5,
                    'alias': None,
                    'status': None
                }

    reference_run = {
                    'files': [
                        {
                            'unencryptedChecksum': '66819a95fed1aaf5445a0792c328e124',
                            'checksum': '62c5105b86de105f56aafde8588ffbe5',
                            'fileName': 'unaligned.20170110/sample_y/sequence_file.paired_end.sample_y.fq.gz.gpg',
                            'checksumMethod': 'md5',
                            'fileId': None
                        }
                    ],
                    'sampleId': None,
                    'experimentId': None,
                    'runFileTypeId': 0,
                    'alias': None,
                    'id': None,
                    'status': None
                }

    assert cmp(unaligned.sample.to_dict(),reference_sample) == 0
    assert cmp(unaligned.experiment.to_dict(),reference_experiment)  == 0
    assert cmp(unaligned.run.to_dict(),reference_run)  == 0

    # Check if the md5 checksum is missing in the file
    with pytest.raises(Exception):
        unaligned = Unaligned('sample_bad')

    # Check if the folder name is malformed
    with pytest.raises(Exception):
        unaligned = Unaligned('sample_bad2$')

    # Check if the folder exists
    with pytest.raises(Exception):
        unaligned = Unaligned('sample_bad_99')
        
    # Missing experiment.yaml file
    with pytest.raises(Exception):
        unaligned = Unaligned('sample_bad3')

    os.chdir(initial_directory)
