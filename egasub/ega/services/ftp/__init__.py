from ftplib import FTP

def file_exists(host, username, password,file_path):
    ftp = FTP(host)
    ftp.login(username, password)

    file_size = None
    try:
        file_size = ftp.size(file_path)
    except Exception, err:
        pass  # do not need to do anything

    ftp.quit()

    return file_size is not None