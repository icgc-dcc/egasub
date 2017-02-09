from egasub.submission.submittable import Submittable, _get_md5sum, Alignment, Unaligned
from click.testing import CliRunner
import hashlib
import os
import yaml

def test_get_md5Sum():
    runner = CliRunner()
    with runner.isolated_filesystem():
        m = hashlib.md5()
        m.update("secret")
        
        file_path = "newfile"
        f = open(file_path,"wb")
        f.write(m.hexdigest())
        f.close()
        
        _get_md5sum(file_path)
        
def test_alignment():
    runner = CliRunner()
    with runner.isolated_filesystem():
        submission_dir = "test"
        os.mkdir(submission_dir)
        
        m = hashlib.md5()
        m.update("secret")
        
        md5_file = "fileName.md5"
        f = open(os.path.join(submission_dir,md5_file),"wb")
        f.write(m.hexdigest())
        f.close()
        
        file_path = "analysis.yaml"
        with open(os.path.join(submission_dir,file_path),"w") as outfile:
            yaml.dump(dict(
                sample = dict(alias="an alias"),
                analysis = dict(title="a title"),
                files=[dict(fileName="fileName", checksumMethod="md5")])
                      , outfile)
        
        alignment = Alignment(submission_dir)
        
        _type = "type"
        _alias = "alias"
        _field = "field"
        _message = "error message"
        
        alignment._add_local_validation_error(_type,_alias,_field,_message)
        alignment._add_ftp_file_validation_error(_field,_message)
        
        assert len(alignment.local_validation_errors) == 1
        assert alignment.local_validation_errors[0]['object_alias'] == _alias
        assert alignment.local_validation_errors[0]['field'] == _field
        assert alignment.local_validation_errors[0]['object_type'] == _type
        assert alignment.local_validation_errors[0]['error'] == _message
        
        assert len(alignment.ftp_file_validation_errors) == 1
        assert alignment.ftp_file_validation_errors[0]['field'] == _field
        assert alignment.ftp_file_validation_errors[0]['error'] == _message
        
def test_unaligned():
    runner = CliRunner()
    with runner.isolated_filesystem():
        submission_dir = "test"
        os.mkdir(submission_dir)
        
        m = hashlib.md5()
        m.update("secret")
        
        md5_file = "fileName.md5"
        f = open(os.path.join(submission_dir,md5_file),"wb")
        f.write(m.hexdigest())
        f.close()
        
        file_path = "experiment.yaml"
        with open(os.path.join(submission_dir,file_path),"w") as outfile:
            yaml.dump(dict(
                sample = dict(alias="an alias"),
                experiment = dict(title="a title"),
                run = dict(runFileTypeId="ID"),
                files=[dict(fileName="fileName", checksumMethod="md5")])
                      , outfile)
        
        unaligned = Unaligned(submission_dir)
        
        _type = "type"
        _alias = "alias"
        _field = "field"
        _message = "error message"
        
        unaligned._add_local_validation_error(_type,_alias,_field,_message)
        unaligned._add_ftp_file_validation_error(_field,_message)
        
        assert len(unaligned.local_validation_errors) == 1
        assert unaligned.local_validation_errors[0]['object_alias'] == _alias
        assert unaligned.local_validation_errors[0]['field'] == _field
        assert unaligned.local_validation_errors[0]['object_type'] == _type
        assert unaligned.local_validation_errors[0]['error'] == _message
        
        assert len(unaligned.ftp_file_validation_errors) == 1
        assert unaligned.ftp_file_validation_errors[0]['field'] == _field
        assert unaligned.ftp_file_validation_errors[0]['error'] == _message

