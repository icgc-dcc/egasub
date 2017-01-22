import requests
import json
from click import echo
from ..entities import sample
from ..entities import analysis
import pprint


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
    
    try:
        ctx.obj['SUBMISSION'] = {}
        ctx.obj['SUBMISSION']['sessionToken'] = r_data['response']['result'][0]['session']['sessionToken']
    except TypeError:
        echo("Your credentials are invalid. Verify your username and password in config.yaml file.")


def logout(ctx):
    url = "%slogout" % EGA_SUB_URL_PROD
    headers = {
        'Content-Type': 'application/json',
        'X-Token': ctx.obj['SUBMISSION']['sessionToken']
        }
    r = requests.delete(url,headers=headers)
    if json.loads(r.text)['header']['userMessage'] == "OK":
        ctx.obj['SUBMISSION'] = {}
        
        

def prepare_submission(ctx, submission):
    if 'id' in ctx.obj['SUBMISSION']:
        return
    
    url = "%ssubmissions" % EGA_SUB_URL_PROD
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    r = requests.post(url,data=json.dumps(submission.to_dict()), headers=headers)
    r_data = json.loads(r.text)
    
    ctx.obj['SUBMISSION']['id'] = r_data['response']['result'][0]['id']
    
    


def submit_sample(ctx, sample):
    url = "%s/submissions/%s/samples" % (EGA_SUB_URL_PROD,ctx.obj['SUBMISSION']['id'])
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    
    r = requests.post(url,data=json.dumps(sample.to_dict()), headers=headers)
    r_data = json.loads(r.text)
    print r_data
    if r_data['header']['code'] != 200:
        print r_data['header']['userMessage']
        return r_data['response']['result'][0]['id']
    else:
        return r_data['header']['userMessage']


def submit_experiment(ctx, experiment):
    url = "%s/submissions/%s/experiments" % (EGA_SUB_URL_PROD,ctx.obj['SUBMISSION']['id'])
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    
    r = requests.post(url,data=json.dumps(experiment.to_dict()), headers=headers)
    r_data = json.loads(r.text)
    
    if r_data['header']['code'] != 200:
        print r_data['header']['userMessage']
        return r_data['response']['result'][0]['id']
    else:
        return r_data['header']['userMessage']

def submit_analysis(ctx, analysis):
    """
    To be implemented
    """
    pass


def submit_run(ctx, run):
    url = "%s/submissions/%s/runs" % (EGA_SUB_URL_PROD,ctx.obj['SUBMISSION']['id'])
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    
    r = requests.post(url,data=json.dumps(run.to_dict()), headers=headers)
    print r.text
    r_data = json.loads(r.text)
    
    if r_data['header']['code'] != 200:
        print r_data['header']['userMessage']
        return r_data['response']['result'][0]['id']
    else:
        return r_data['header']['userMessage']


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


