
from ftplib import FTP

def file_exists(host, username, password,file_path):
    ftp = FTP(host)
    ftp.login(username, password)
    ftp.quit()