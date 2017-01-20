import requests
import json
from click import echo
from ..entities import sample
from ..entities import analysis


XML_EGA_SUB_URL_TEST = "https://www-test.ebi.ac.uk/ena/submit/drop-box/submit/"
XML_EGA_SUB_URL_PROD = "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"

EGA_SUB_URL_TEST = ""
EGA_SUB_URL_PROD = "https://ega.crg.eu/submitterportal/v1/"

EGA_ACCESS_URL = "https://ega.ebi.ac.uk/ega/rest/access/v2/"
EGA_DOWNLOAD_URL = "http://ega.ebi.ac.uk/ega/rest/download/v2/"


def login(ctx):
    """
    Documentation: https://ega-archive.org/submission/programmatic_submissions/how-to-use-the-api#Login
    """
    url = "%slogin" % EGA_SUB_URL_PROD
    payload = {
        "username": ctx.obj['SETTINGS'].get('ega_submitter_account'),
        "password": ctx.obj['SETTINGS'].get('ega_submitter_password'),
        "loginType": "submitter"
    }

    r = requests.post(url, data=payload)

    r_data = json.loads(r.text)

    # to be finished



def logout(ctx):
    pass


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


