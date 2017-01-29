import yaml
import os

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


    @staticmethod
    def load_list_from_yaml(ctx, yaml_path):
        with open(yaml_path, 'r') as stream:
            yaml_stream = yaml.load(stream)
            
        yaml_files = yaml_stream.get('files')
        
        files = []
        checksum_method = 'md5'
        for _file in yaml_files:
            full_path_file = os.path.join(ctx.obj['WORKSPACE_PATH'],_file.get('fileName'))
            md5_file = full_path_file+"."+checksum_method
            md5_checksum_encrypt = open(md5_file, 'r').readline().rstrip()
            md5_checksum_unencrypt = open(os.path.splitext(full_path_file)[0]+"."+checksum_method,'r').readline().rstrip()
            files.append(File(None,_file.get('fileName'),md5_checksum_encrypt,md5_checksum_unencrypt,checksum_method))
        return files