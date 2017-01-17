import pytest
from file import File

file = File(32,'file name','CheckSum','UnencryptedChecksum','md5')

def test_file_id():
    assert 32 == file.file_id
    
def test_file_name():
    assert 'file name' == file.file_name
    
def test_checksum():
    assert 'CheckSum' == file.checksum
    
def test_unencrypted_checksum():
    assert 'UnencryptedChecksum' == file.unencrypted_checksum
    
def test_checksum_method():
    assert 'md5'.lower() == file.checksum_method.lower()
    
def test_to_dict():
    assert cmp({'fileId':32,'fileName':'file name','checksum':'CheckSum','unencryptedChecksum':'UnencryptedChecksum'}, file.to_dict()) == 0