
class File(object):
    def __init__(self,file_id,file_name,checksum,unencrypted_checksum,checksum_method):
        self.file_id = file_id
        self.file_name = file_name
        self.checksum = checksum
        self.unencrypted_checksum = unencrypted_checksum
        self.checksum_method = checksum_method

    def to_dict(self):
        return {
            'fileId': self.file_id,
            'fileName': self.file_name,
            'checksum': self.checksum,
            'unencryptedChecksum' : self.unencrypted_checksum,
            'checksumMethod' : self.checksum_method
        }

    def to_xml(self):
        pass

    @staticmethod
    def from_dict(file_dict):
        return File(
                None,
                file_dict.get('fileName'),
                file_dict.get('checksum'),
                file_dict.get('unencryptedChecksum'),
                file_dict.get('checksumMethod')
            )

