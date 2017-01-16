import requests
from ..entities import sample
from ..entities import analysis


XML_EGA_SUB_URL_TEST = "https://www-test.ebi.ac.uk/ena/submit/drop-box/submit/"
XML_EGA_SUB_URL_PROD = "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"

EGA_SUB_URL_TEST = ""
EGA_SUB_URL_PROD = "https://ega.crg.eu/submitterportal/v1/"

EGA_ACCESS_URL = "https://ega.ebi.ac.uk/ega/rest/access/v2/"
EGA_DOWNLOAD_URL = "http://ega.ebi.ac.uk/ega/rest/download/v2/"


def submit_sample(ctx, sample):
    """
    To be implemented
    """
    pass


def submit_analysis(ctx, analysis):
    """
    To be implemented
    """
    pass


def submit_run(ctx, run):
    """
    To be implemented
    """
    pass


def submit_study(ctx, run):
    """
    To be implemented
    """
    pass


def submit_metadata(ctx, metadata):
    """
    To be implemented
    metadata is a universal Metadata object which can be Analysis or Experiment
    """
    pass


