
from ftplib import FTP
from click import echo

def file_exists(host, username, password,file_path):
    ftp = FTP(host)
    ftp.login(username, password)    
    
    file_size = None
    file_size = ftp.size(file_path)
    ftp.quit()
    
    return file_size is not None