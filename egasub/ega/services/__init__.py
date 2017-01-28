import requests
import json
from click import echo
from ..entities import sample
from ..entities import analysis
from egasub.exceptions import CredentialsError
import os


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
    if 'apiUrl' in ctx.obj['SETTINGS']:
        api_url = ctx.obj['SETTINGS']['apiUrl']
    else:
        api_url = EGA_SUB_URL_PROD
        
    url = "%slogin" % api_url
    
    #Check for the ega_submitter account
    if not ctx.obj['SETTINGS'].get('ega_submitter_account'):
        raise CredentialsError(Exception('Your ega_submitter_account is missing in config.yaml file.'))
    
    #Check for the ega submitter password
    if not ctx.obj['SETTINGS'].get('ega_submitter_password'):
        raise CredentialsError(Exception('Your ega_submitter_password is missing in config.yaml file.'))
    
    payload = {
        "username": ctx.obj['SETTINGS'].get('ega_submitter_account'),
        "password": ctx.obj['SETTINGS'].get('ega_submitter_password'),
        "loginType": "submitter"
    }

    r = requests.post(url, data=payload)
    r_data = json.loads(r.text)
    
    #Check if the credentials are accepted
    print r.text
    if r_data["header"]['code'] != '200':
        raise CredentialsError(Exception('Your credentials are invalid. Verify your username and password in config.yaml file.'))
    
    ctx.obj['SUBMISSION'] = {}
    ctx.obj['SUBMISSION']['sessionToken'] = r_data['response']['result'][0]['session']['sessionToken']
    
    


def logout(ctx):
    """ Terminate the session token on EGA side and deleting the token on the client side. """
    if 'apiUrl' in ctx.obj['SETTINGS']:
        api_url = ctx.obj['SETTINGS']['apiUrl']
    else:
        api_url = EGA_SUB_URL_PROD
        
    url = "%slogout" % api_url
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token': ctx.obj['SUBMISSION']['sessionToken']
        }
    r = requests.delete(url,headers=headers)
    ctx.obj['SUBMISSION'].clear()
        
        

def prepare_submission(ctx, submission):
    """ This function checks if the submission has an ega id and requests one if not """
    
    if 'apiUrl' in ctx.obj['SETTINGS']:
        api_url = ctx.obj['SETTINGS']['apiUrl']
    else:
        api_url = EGA_SUB_URL_PROD
    
    if 'id' in ctx.obj['SUBMISSION']:
        return
    
    url = "%ssubmissions" % api_url
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    r = requests.post(url,data=json.dumps(submission.to_dict()), headers=headers)
    r_data = json.loads(r.text)
    
    ctx.obj['SUBMISSION']['id'] = r_data['response']['result'][0]['id']
    
    
def sample_log_directory(ctx,sample_dir):
    return os.path.join(ctx.obj['CURRENT_DIR'],sample_dir,".log")

def sample_status_file(ctx, sample_dir):
    return os.path.join(sample_log_directory(ctx, sample_dir),"status")

def set_sample_status(ctx,sample_dir,status):
    status_file = open(sample_status_file(ctx, sample_dir),"w")
    status_file.write(status)
    status_file.close()
    
def get_sample_status(ctx,sample_dir):
    return open(sample_status_file(ctx, sample_dir),"r").read()

def submit_sample(ctx, sample,sample_dir):
    url = "%s/submissions/%s/samples" % (EGA_SUB_URL_PROD,ctx.obj['SUBMISSION']['id'])
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    
    r = requests.post(url,data=json.dumps(sample.to_dict()), headers=headers)
    r_data = json.loads(r.text)
    
    if r_data['header']['code'] == "200":
        sample.id = r_data['response']['result'][0]['id']
    else:
        #TODO
        raise Exception(r_data['header']['userMessage'])
    
    set_sample_status(ctx, sample_dir, "DRAFT")
    
    echo(" - Sample validation...")
    validate_sample(ctx, sample,sample_dir)
    echo(" - Validation completed")
    
    
    
def validate_sample(ctx,sample,sample_dir):
    if sample.id == None:
        raise Exception('Sample id missing.')
    
    url = "%ssamples/%s?action=VALIDATE" % (EGA_SUB_URL_PROD,sample.id)
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    r = requests.put(url,headers=headers)
    r_data = json.loads(r.text)
    
    if r_data['header']['code'] == "200":
        set_sample_status(ctx, sample_dir, "VALIDATED")
    else:
        raise Exception(r_data['header']['userMessage'])
    

def submit_experiment(ctx, experiment):
    url = "%s/submissions/%s/experiments" % (EGA_SUB_URL_PROD,ctx.obj['SUBMISSION']['id'])
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    
    r = requests.post(url,data=json.dumps(experiment.to_dict()), headers=headers)
    r_data = json.loads(r.text)
    
    if r_data['header']['code'] == "200":
        experiment.id = r_data['response']['result'][0]['id']
    else:
        #TODO
        raise Exception(r_data['header']['userMessage'])

def submit_analysis(ctx, analysis):
    url = "%s/submissions/%s/analyses" % (EGA_SUB_URL_PROD,ctx.obj['SUBMISSION']['id'])
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    
    r = requests.post(url,data=json.dumps(analysis.to_dict()), headers=headers)
    r_data = json.loads(r.text)
    print r_data
    
    if r_data['header']['code'] == "200":
        run.id = r_data['response']['result'][0]['id']
    else:
        #TODO
        raise Exception(r_data['header']['userMessage'])


def submit_run(ctx, run):
    url = "%s/submissions/%s/runs" % (EGA_SUB_URL_PROD,ctx.obj['SUBMISSION']['id'])
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    
    r = requests.post(url,data=json.dumps(run.to_dict()), headers=headers)
    #print r.text
    r_data = json.loads(r.text)
    
    if r_data['header']['code'] == "200":
        run.id = r_data['response']['result'][0]['id']
    else:
        #TODO
        raise Exception(r_data['header']['userMessage'])
    


def submit_submission(ctx,submission):
    url = "%ssubmissions/%s?action=SUBMIT" % (EGA_SUB_URL_PROD,ctx.obj['SUBMISSION']['id'])
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }

    r = requests.put(url,data=json.dumps(submission.to_dict()), headers=headers)
    r_data = json.loads(r.text)


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


