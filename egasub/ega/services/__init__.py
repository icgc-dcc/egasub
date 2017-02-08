import requests
import json
from ..entities import sample
from ..entities import analysis
from egasub.exceptions import CredentialsError
import os
from egasub.icgc.services import id_service


XML_EGA_SUB_URL_TEST = "https://www-test.ebi.ac.uk/ena/submit/drop-box/submit/"
XML_EGA_SUB_URL_PROD = "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"

EGA_SUB_URL_TEST = ""
EGA_SUB_URL_PROD = "https://ega.crg.eu/submitterportal/v1/"

EGA_ACCESS_URL = "https://ega.ebi.ac.uk/ega/rest/access/v2/"
EGA_DOWNLOAD_URL = "http://ega.ebi.ac.uk/ega/rest/download/v2/"

def api_url(ctx):
    if 'apiUrl' in ctx.obj['SETTINGS']:
        api_url = ctx.obj['SETTINGS']['apiUrl']
    else:
        api_url = EGA_SUB_URL_PROD
    return api_url


def login(ctx):
    """
    Documentation: https://ega-archive.org/submission/programmatic_submissions/how-to-use-the-api#Login
    """
        
    url = "%slogin" % api_url(ctx)
    
    #Check for the ega_submitter account
    if not ctx.obj['SETTINGS'].get('ega_submitter_account'):
        raise CredentialsError(Exception('Your ega_submitter_account is missing in .egasub/config.yaml file.'))
    
    #Check for the ega submitter password
    if not ctx.obj['SETTINGS'].get('ega_submitter_password'):
        raise CredentialsError(Exception('Your ega_submitter_password is missing in .egasub/config.yaml file.'))
    
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
        
    url = "%slogout" % api_url(ctx)
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token': ctx.obj['SUBMISSION']['sessionToken']
        }
    r = requests.delete(url,headers=headers)
    ctx.obj['SUBMISSION'].clear()


def prepare_submission(ctx, submission):
    """ This function checks if the submission has an ega id and requests one if not """
    
    if 'id' in ctx.obj['SUBMISSION']:
        return
    
    url = "%ssubmissions" % api_url(ctx)

    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    r = requests.post(url,data=json.dumps(submission.to_dict()), headers=headers)
    r_data = json.loads(r.text)
    
    ctx.obj['SUBMISSION']['id'] = r_data['response']['result'][0]['id']


def object_submission(ctx, obj, obj_type, dry_run=True):
    existing_objects = query_by_id(ctx, obj_type, obj.alias, 'ALIAS')
    for o in existing_objects:
        if o.get('status') == 'SUBMITTED' or (dry_run and o.get('status') == 'VALIDATED'):
            obj.id = o.get('id')
            ctx.obj['LOGGER'].info("%s with alias '%s' already exists in '%s' status, no need to submit." \
                                     % (obj_type, obj.alias, o.get('status')))
            return

    register_obj(ctx, obj, obj_type)
    if dry_run:
        validate_obj(ctx, obj, obj_type)
    else:
        submit_obj(ctx, obj, obj_type)


def register_obj(ctx, obj, obj_type):
    ctx.obj['LOGGER'].info("Registering '%s' ..." % obj_type)

    url = "%ssubmissions/%s/%s" % (
                                        api_url(ctx),
                                        ctx.obj['SUBMISSION']['id'],
                                        _obj_type_to_endpoint(obj_type)
                                    )
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }

    ctx.obj['LOGGER'].debug("Registering '%s': \n%s" % (obj_type, json.dumps(obj.to_dict()))) # for debug
    r = requests.post(url,data=json.dumps(obj.to_dict()), headers=headers)
    ctx.obj['LOGGER'].debug("Response after registering: \n%s" % r.text)  # for debug
    r_data = json.loads(r.text)

    if r_data['header']['code'] == "200":
        obj.id = r_data['response']['result'][0]['id']
    else:
        raise Exception(r_data['header']['userMessage'])


def validate_obj(ctx, obj, obj_type):
    _validate_submit_obj(ctx, obj, obj_type, 'validate')


def submit_obj(ctx, obj, obj_type):
    _validate_submit_obj(ctx, obj, obj_type, 'submit')


def _validate_submit_obj(ctx, obj, obj_type, op_type):
    if not op_type in ('validate', 'submit'):
        raise Exception('Not supported operation %s' % op_type)

    ctx.obj['LOGGER'].info("%s '%s' ..." % (op_type.capitalize(), obj_type))

    if obj.id == None:
        raise Exception('EGA Object id missing.')

    # we directly go to submit
    url = "%s%s/%s?action=%s" % (
                                        api_url(ctx),
                                        _obj_type_to_endpoint(obj_type),
                                        obj.id,
                                        op_type.upper()
                                    )

    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    r = requests.put(url,headers=headers)
    ctx.obj['LOGGER'].debug("Response after '%s': \n%s" % (op_type, r.text))  # for debug
    r_data = json.loads(r.text)

    # enable this when EGA fixes the validation bug
    if r_data.get('header', {}).get('code') != "200":
        raise Exception("Error message: %s" % r_data.get('header', {}).get('userMessage'))

    ctx.obj['LOGGER'].info("%s '%s' completed." % (op_type.capitalize(), obj_type))

    return r_data.get('response').get('result',[]) if r_data.get('response') else []


def update_obj(ctx, obj, obj_type):
    """
    Not implemented yet
    """
    pass


def _obj_type_to_endpoint(obj_type):
    if obj_type in ('sample', 'experiment', 'run'):
        return '%ss' % obj_type
    elif obj_type == 'analysis':
        return 'analyses'
    elif obj_type == 'study':
        return 'studies'
    else:
        raise Exception('Not supported EGA object type %s' % obj_type)


def query_by_id(ctx, obj_type, obj_id, id_type):
    url = "%s%s/%s?idType=%s" % (api_url(ctx), _obj_type_to_endpoint(obj_type), obj_id, id_type)

    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }

    r = requests.get(url, headers=headers)
    ctx.obj['LOGGER'].debug("Response after querying '%s' by '%s' (%s): \n%s" % (obj_type, obj_id, id_type, r.text))  # for debug
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
    ctx.obj['LOGGER'].info('Deleted: %s %s' % (obj_type, obj_id))  # for debug
    ctx.obj['LOGGER'].debug("Response after deleting '%s' with ID '%s': \n%s" % (obj_type, obj_id, r.text))  # for debug


def submit_submission(ctx,submission):
    url = "%ssubmissions/%s?action=SUBMIT" % (EGA_SUB_URL_PROD,ctx.obj['SUBMISSION']['id'])
    
    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }

    r = requests.put(url,data=json.dumps(submission.to_dict()), headers=headers)
    r_data = json.loads(r.text)

