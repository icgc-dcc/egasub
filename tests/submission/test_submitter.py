from egasub.submission.submitter import Submitter
import os
from egasub.submission.submittable import Unaligned
from egasub.ega.entities.sample import Sample
from egasub.ega.entities.attribute import Attribute

def test_submitter(ctx, mock_server):
    initial_directory = os.getcwd()
    os.chdir('tests/data/workspace/unaligned.20170110/')
    unaligned = Unaligned('ssample_y')
    os.chdir(initial_directory)

    submitter = Submitter(ctx)

    ctx.obj['SUBMISSION']['sessionToken'] = 'X-Token'
    ctx.obj['SETTINGS']['icgc_project_code'] = "abjdh"
    #assert submitter.submit(unaligned, True) is None

    #attributes = [Attribute('tag1', 'value1'), Attribute('tag2', 'value2')]
    #sample = Sample('an alias','the title','the description',123,2,'head','test line','test region','a phenotype',33,'anonymized name',22,10,'some details',attributes,33)
    #assert submitter.set_icgc_ids(sample, True) is None


'''  
def something():
    with pytest.raises(CredentialsError):
        login(ctx)

    ctx.obj['SETTINGS']['ega_submitter_account'] = 'test_account'

    with pytest.raises(CredentialsError):
        login(ctx)

    ctx.obj['SETTINGS']['ega_submitter_password'] = 'test_password'

    login(ctx)
    assert not ctx.obj['SUBMISSION']['sessionToken'] == None
    assert ctx.obj['SUBMISSION']['sessionToken'] == "abcdefg"
'''