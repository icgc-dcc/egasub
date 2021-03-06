import pytest
import os
import shutil
from egasub.submission.submittable import Unaligned
from egasub.submission.submittable.base import Experiment
from egasub.ega.entities import Sample, EgaEnums, \
                                Experiment as EExperiment, \
                                Run as ERun

def test_unaligned():
    initial_directory = os.getcwd()
    os.chdir('tests/data/workspace/unaligned.20170110/')
    unaligned = Unaligned('ssample_y')
    localval = Unaligned('local_val')
    #unaligned2 = Unaligned('sample_x')

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
                    'status': None,
                    'egaAccessionId': None
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
                    'status': None,
                    'egaAccessionId': None
                }

    reference_run = {
                    'files': [
                        {
                            'unencryptedChecksum': '66819a95fed1aaf5445a0792c328e124',
                            'checksum': '62c5105b86de105f56aafde8588ffbe5',
                            'fileName': 'unaligned.20170110/ssample_y/sequence_file.paired_end.sample_y.fq.gz.gpg',
                            'checksumMethod': 'md5',
                            'fileId': None
                        }
                    ],
                    'sampleId': None,
                    'experimentId': None,
                    'runFileTypeId': 0,
                    'alias': None,
                    'id': None,
                    'status': None,
                    'egaAccessionId': None
                }

    assert cmp(unaligned.sample.to_dict(),reference_sample) == 0
    assert cmp(unaligned.experiment.to_dict(),reference_experiment)  == 0
    assert cmp(unaligned.run.to_dict(),reference_run)  == 0

    localval.local_validate(EgaEnums())

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

    # Cannot create submission error
    with pytest.raises(Exception):
        unaligned = Unaligned('tests')
    # Name error
    with pytest.raises(Exception):
        unaligned = Unaligned('^*#')

    cwd = os.getcwd()

    assert unaligned.status == 'NEW'

    assert unaligned.files == unaligned.run.files

    assert unaligned.local_validate(EgaEnums()) is None
    #test bad object type
    unaligned.record_object_status('none', True, "test", "test")
    #make sure no log was built
    assert os.path.isfile(os.path.join(cwd, 'ssample_y/.status')) == False
    #make sure no record to restore
    unaligned.restore_latest_object_status('none')
    #make sure no log was built
    assert os.path.isfile(os.path.join(cwd, 'ssample_y/.status')) == False
    #proper run
    unaligned.record_object_status('sample', True, "test", "test")
    #assert log file exists
    assert os.path.isfile(os.path.join(cwd, 'ssample_y/.status/sample.log')) == True
    #restore object from log
    unaligned.restore_latest_object_status('sample')

    assert os.path.isfile(os.path.join(cwd, 'ssample_y/.status')) == False

    #delete log file path
    shutil.rmtree(os.path.join(cwd, 'ssample_y/.status'))

    os.chdir(initial_directory)
