import pytest
from egasub.submission.submit import submittable_status

def test_submittable_status():
    assert submittable_status("fail") == None
    assert submittable_status("egasub/cli.py") == ['']