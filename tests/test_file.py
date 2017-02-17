from egasub.ega.entities.file import File

file_ = File(32,'file name','CheckSum','UnencryptedChecksum','md5')

def test_file_id():
    assert 32 == file_.file_id

def test_file_name():
    assert 'file name' == file_.file_name
    
def test_checksum():
    assert 'CheckSum' == file_.checksum
    
def test_unencrypted_checksum():
    assert 'UnencryptedChecksum' == file_.unencrypted_checksum
    
def test_checksum_method():
    assert 'md5'.lower() == file_.checksum_method.lower()
    
def test_to_dict():
    assert cmp({
                    'fileId':32,
                    'fileName':'file name',
                    'checksum':'CheckSum',
                    'unencryptedChecksum':'UnencryptedChecksum',
                    'checksumMethod':'md5',
                }, file_.to_dict()) == 0