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


def submit_obj(ctx, obj, obj_type):
    echo(" - Registering %s ..." % obj_type)
    endpoint = obj_type_to_endpoint(obj_type)

    # TODO: before registering new object, we should check existence
    #       of same type of object with the same alias

    url = "%s/submissions/%s/%s" % (
                                        EGA_SUB_URL_PROD,
                                        ctx.obj['SUBMISSION']['id'],
                                        endpoint
                                    )
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }

    #echo('Registering object: %s' % json.dumps(obj.to_dict())) # for debug
    r = requests.post(url,data=json.dumps(obj.to_dict()), headers=headers)
    #echo(r.text)  # for debug
    r_data = json.loads(r.text)

    if r_data['header']['code'] == "200":
        obj.id = r_data['response']['result'][0]['id']
    else:
        #TODO
        raise Exception(r_data['header']['userMessage'])

    validate_obj(ctx, obj, obj_type)


def validate_obj(ctx, obj, obj_type):
    echo(" - Validating %s ..." % obj_type)
    endpoint = obj_type_to_endpoint(obj_type)

    if obj.id == None:
        raise Exception('EGA Object id missing.')

    url = "%s%s/%s?action=VALIDATE" % (
                                        EGA_SUB_URL_PROD,
                                        endpoint,
                                        obj.id
                                    )

    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    r = requests.put(url,headers=headers)
    #echo(r.text)  # for debug
    r_data = json.loads(r.text)

    # enable this when EGA fixes the validation bug
    #if r_data.get('header', {}).get('code') != "200":
    #    raise Exception("Error message: %s" % r_data.get('header', {}).get('userMessage'))

    result = r_data.get('response').get('result',[]) if r_data.get('response') else None

    if result and result[0].get('validationErrorMessages'):
        err = "\n".join(result[0].get('validationErrorMessages'))
        # echo('Validation error: %s' % err)  # for debug
        if err == 'Alias %s already exists in another %s' % (obj.alias, obj_type):
            objects_with_err = query_by_id(ctx, endpoint, obj.alias, 'ALIAS')
            for s in objects_with_err:
                if s.get('status') == 'VALIDATED_WITH_ERRORS':
                    delete(ctx, endpoint, s.get('id'))
        else:
            raise Exception

    for s in query_by_id(ctx, endpoint, obj.alias, 'ALIAS'):
        #echo('%s with alias: %s, id: %s' % (obj_type, s.get('alias'), s.get('id')))  # for debug
        #echo(json.dumps(s))  # for debug
        if s.get('status') in ('VALIDATED', 'SUBMITTED'):  # use the good object id
            obj.id = s.get('id')
            break

    echo(" - Validation completed.")


def obj_type_to_endpoint(obj_type):
    if obj_type in ('sample', 'experiment', 'run'):
        endpoint = '%ss' % obj_type
    elif obj_type == 'analysis':
        endpoint = 'analyses'
    elif obj_type == 'study':
        endpoint = 'studies'
    else:
        raise Exception('Not supported EGA object type %s' % obj_type)

    return endpoint


def query_by_id(ctx, obj_type, obj_id, id_type):
    url = "%s%s/%s?idType=%s" % (EGA_SUB_URL_PROD, obj_type, obj_id, id_type)

    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }

    r = requests.get(url, headers=headers)
    #echo(r.text)  # for debug
    r_data = json.loads(r.text)
    if r_data.get('response'):
        return r_data.get('response').get('result',[])
    else:
        return []


def delete(ctx, obj_type, obj_id):
    url = "%s%s/%s" % (EGA_SUB_URL_PROD, obj_type, obj_id)

    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    r = requests.delete(url, headers=headers)
    # echo('Deleted: %s %s' % (obj_type, obj_id))  # for debug
    #echo(r.text)  # for debug


def submit_submission(ctx,submission):
    url = "%ssubmissions/%s?action=SUBMIT" % (EGA_SUB_URL_PROD,ctx.obj['SUBMISSION']['id'])
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }

    r = requests.put(url,data=json.dumps(submission.to_dict()), headers=headers)
    r_data = json.loads(r.text)

