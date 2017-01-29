__all__ = [
    'ImproperlyConfigured',
    'EgaSubmissionError',
    'EgaObjectExistsError',
    'CredentialsError',
    'Md5sumFileError'
]


class ImproperlyConfigured(Exception):
    """
    Exception raised when the config passed to the client is inconsistent or invalid.
    """

class EgaSubmissionError(Exception):
    @property
    def error(self):
        """ A string error message. """
        return self.args[0]

    @property
    def info(self):
        """ Dict of returned error info from EGA, where available. """
        return self.args[1]

    def __str__(self):
        cause = ''
        try:
            if self.info:
                cause = ', %r' % self.info
        except LookupError:
            pass
        return 'EgaSubmissionError(%r%s)' % (self.error, cause)


class EgaObjectExistsError(EgaSubmissionError):
    def __str__(self):
        return 'EgaObjectExistsError(%s) caused by: %s(%s)' % (
            self.error, self.info.__class__.__name__, self.info)

class CredentialsError(Exception):
    """
    Exception raised when the login credentials are not working
    """

class Md5sumFileError(Exception):
    def __str__(self):
        return 'Md5sumFileError(%s)' % (self.args[0])

