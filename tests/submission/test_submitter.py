from egasub.submission.submitter import Submitter
import os
import pytest
from egasub.submission.submittable import Unaligned
from egasub.ega.entities.sample import Sample
from egasub.ega.entities.attribute import Attribute

def test_submitter(ctx, mock_server):
    initial_directory = os.getcwd()
    os.chdir('tests/data/workspace/submittable/')
    unaligned = Unaligned('ssample_y')
    os.chdir(initial_directory)

    submitter = Submitter(ctx)

    ctx.obj['SUBMISSION']['sessionToken'] = 'X-Token'
    ctx.obj['SETTINGS']['icgc_project_code'] = "abjdh"

    #do not uncomment
    with pytest.raises(ValueError):
        submitter.submit(unaligned, True)

    attributes = [Attribute('tag1', 'value1'), Attribute('tag2', 'value2')]
    sample = Sample('an alias','the title','the description',123,2,'head','test line','test region','a phenotype',33,'anonymized name',22,10,'some details',attributes,33)
    with pytest.raises(Exception):
        submitter.set_icgc_ids(sample, True)

    ctx.obj['SETTINGS']['_icgc_sample_id'] = "abjdhf"

    with pytest.raises(Exception):
        submitter.set_icgc_ids(sample, True)


