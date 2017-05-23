from mock import patch, mock_open
from egasub.ega.services.ftp import file_exists

@patch('ftplib.FTP')
def test_file_exists(MockFTP):
    with patch('__main__.open', mock_open(), create=True) as m:
    #    file_exists('ftp.ega.ebi.ac.uk', 'test_user', 'test_pass', 'tests/data/workspace/submittable/test_u/')
        pass