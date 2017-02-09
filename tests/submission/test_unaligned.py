import pytest
from egasub.submission.submittable import Unaligned
from egasub.ega.entities import Sample, \
                                Experiment as EExperiment, \
                                Run as ERun
from egasub.exceptions import Md5sumFileError


def test_unaligned():
    unaligned = Unaligned('tests/data/workspace/unaligned.20170110/sample_y')

    assert isinstance(unaligned.sample, Sample)
    assert isinstance(unaligned.experiment, EExperiment)
    assert isinstance(unaligned.run, ERun)

    assert cmp(
                unaligned.sample.to_dict(),
                {
                    'genderId': 1,
                    'cellLine': None,
                    'description': None,
                    'sampleAge': None,
                    'title': None,
                    'region': None,
                    'subjectId': 'abc',
                    'organismPart': None,
                    'alias': 'sample_y',
                    'caseOrControlId': 2,
                    'id': None,
                    'phenotype': 'Breast cancer',
                    'attributes': [],
                    'bioSampleId': None,
                    'anonymizedName': None,
                    'sampleDetail': None,
                    'status': None
                }
            ) == 0

    assert cmp(
                unaligned.experiment.to_dict(),
                {
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
            )  == 0

    assert cmp(
                unaligned.run.to_dict(),
                {
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
            )  == 0


# disable this test, need to replace it with a good one
#def test_bad_unaligned():
#    with pytest.raises(Md5sumFileError):
#        unaligned = Unaligned('tests/data/workspace/unaligned.20170110/sample_bad')

