
from ftplib import FTP
from click import echo

def file_exists(host, username, password,file_path):
    ftp = FTP(host)
    if ftp.login(username, password) != "230 Login successful.":
        raise Exception("Credentials not working for FTP server: %s", host)
    
    echo("Login to %s as %s" % (host, username))
    
    file_size = None
    
    try:
        file_size = ftp.size(file_path)
    except:
        pass
    echo("Exiting %s" %(host))
    ftp.quit()
    
    return file_size is not None