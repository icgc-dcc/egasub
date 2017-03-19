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
        raise CredentialsError(Exception("Your 'ega_submitter_account' is missing."))

    #Check for the ega submitter password
    if not ctx.obj['SETTINGS'].get('ega_submitter_password'):
        raise CredentialsError(Exception("Your 'ega_submitter_password' is missing."))

    payload = {
        "username": ctx.obj['SETTINGS'].get('ega_submitter_account'),
        "password": ctx.obj['SETTINGS'].get('ega_submitter_password'),
        "loginType": "submitter"
    }

    r = requests.post(url, data=payload)
    r_data = json.loads(r.text)

    #Check if the credentials are accepted
    if r_data["header"]['code'] != '200':
        raise CredentialsError(Exception('Your credentials are invalid. Verify your EGA submitter username and password.'))

    ctx.obj['SUBMISSION'] = {}
    ctx.obj['SUBMISSION']['sessionToken'] = r_data['response']['result'][0]['session']['sessionToken']


def logout(ctx):
    """ Terminate the session token on EGA side and deleting the token on the client side. """

    url = "%slogout" % api_url(ctx)

    headers = {
        'Content-Type': 'application/json',
        'X-Token': ctx.obj['SUBMISSION']['sessionToken']
        }
    requests.delete(url,headers=headers)
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
    if obj.alias:  # only lookup for existing object when alias is available
        existing_objects = query_by_id(ctx, obj_type, obj.alias, 'ALIAS')
        for o in existing_objects:
            if not obj.id == o.get('id'):
                obj.id = o.get('id')

            # if status includes SUBMITTED, it can not be updated.
            # message from REST endpoint: Deletion not implemented yet for entities in status
            # PARTIALLY_SUBMITTED, SUBMITTED, SUBMITTED_DRAFT, SUBMITTED_VALIDATED and SUBMITTED_VALIDATED_WITH_ERRORS
            if 'SUBMITTED' in o.get('status'):
                obj.status = o.get('status')
                obj.ega_accession_id = o.get('egaAccessionId')
                ctx.obj['LOGGER'].info("%s with alias '%s' already exists in '%s' status, not submitting." \
                                         % (obj_type, obj.alias, o.get('status')))

                return obj
            else:
                ctx.obj['LOGGER'].info("%s with alias '%s' already exists in '%s' status, updating it." \
                                         % (obj_type, obj.alias, o.get('status')))

                update_obj(ctx, obj, obj_type)

    if not obj.id:
        try:
            register_obj(ctx, obj, obj_type)
        except Exception, err:
            raise Exception("Error occurred while creating '%s': \n%s" % (obj_type, err))

    if dry_run:
        try:
            validate_obj(ctx, obj, obj_type)
        except Exception, err:
            raise Exception("Error occurred while validating '%s': \n%s" % (obj_type, err))
    else:
        try:
            submit_obj(ctx, obj, obj_type)
        except Exception, err:
            raise Exception("Error occurred while submitting '%s': \n%s" % (obj_type, err))

    return obj


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
        obj.alias = r_data['response']['result'][0]['alias']
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
        raise Exception("Error message: \n  userMessage: %s\n  developerMessage: %s" % (
                                                    r_data.get('header', {}).get('userMessage'),
                                                    r_data.get('header', {}).get('developerMessage')
                                                )
                        )
    elif (op_type == 'submit' and not r_data.get('response').get('result')[0].get('status') == 'SUBMITTED'):
        errors = []
        error_validation = r_data.get('response').get('result')[0].get('validationErrorMessages')
        error_submission = r_data.get('response').get('result')[0].get('submissionErrorMessages')

        errors = error_validation if error_validation else []
        errors = errors + (error_submission if error_submission else [])
        raise Exception("Submission failed (note that 'File not found' error, if any, will disappear if you make sure file is indeed uploaded and give it a bit more time (could be a few hours) for EGA systems to synchronize file information): \n%s" % '\n'.join(errors))
    elif (op_type == 'validate' and not r_data.get('response').get('result')[0].get('status') == 'VALIDATED'):
        errors = r_data.get('response').get('result')[0].get('validationErrorMessages')
        ctx.obj['LOGGER'].error("Validation exception (note that 'Sample not found' or 'Unknown sample' error, if any, will disappear when perform 'submit' instead of 'dry_run'; 'File not found' error, if any, will disappear if you make sure file is indeed uploaded and give it a bit more time (could be a few hours) for EGA systems to synchronize file information): \n%s" % '\n'.join(errors))

    obj.status = r_data.get('response').get('result')[0].get('status')
    ega_accession_id = r_data.get('response').get('result')[0].get('egaAccessionId')
    if ega_accession_id:
        obj.ega_accession_id = str(ega_accession_id)
    elif r_data.get('response').get('result')[0].get('egaAccessionIds'):  # for same reason experiment object has a single element of egaAccessionIds
        obj.ega_accession_id = str(r_data.get('response').get('result')[0].get('egaAccessionIds')[0])

    ctx.obj['LOGGER'].info("%s '%s' completed." % (op_type.capitalize(), obj_type))


def update_obj(ctx, obj, obj_type):
    url = "%s%s/%s?action=EDIT" % (
                                        api_url(ctx),
                                        _obj_type_to_endpoint(obj_type),
                                        obj.id
                                    )

    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }

    r = requests.put(url, headers=headers, data=json.dumps(obj.to_dict()))
    ctx.obj['LOGGER'].debug("Response after updating: \n%s" % r.text)  # for debug
    r_data = json.loads(r.text)

    if r_data['header']['code'] == "200":
        obj.id = r_data['response']['result'][0]['id']
        obj.alias = r_data['response']['result'][0]['alias']
    else:
        raise Exception(r_data['header']['userMessage'])

    ctx.obj['LOGGER'].info("Update '%s' completed." % obj_type)


def _obj_type_to_endpoint(obj_type):
    if obj_type in ('sample', 'experiment', 'run', 'dac'):
        return '%ss' % obj_type
    elif obj_type == 'analysis':
        return 'analyses'
    elif obj_type == 'study':
        return 'studies'
    elif obj_type == 'dataset':
        return 'datasets'
    elif obj_type == 'policy':
        return 'policies'
    else:
        raise Exception('Not supported EGA object type %s' % obj_type)


def query_by_id(ctx, obj_type, obj_id, id_type):
    url = "%s%s/%s?idType=%s&skip=0&limit=0" % (api_url(ctx), _obj_type_to_endpoint(obj_type), obj_id, id_type)

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


def query_by_type(ctx, obj_type, obj_status="SUBMITTED"):
    url = "%s%s?status=%s&skip=0&limit=0" % (api_url(ctx), _obj_type_to_endpoint(obj_type), obj_status)

    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }

    r = requests.get(url, headers=headers)
    ctx.obj['LOGGER'].debug("Response after querying '%s' by status '%s': \n%s" % (obj_type, obj_status, r.text))  # for debug
    r_data = json.loads(r.text)
    if r_data.get('response'):
        return r_data.get('response').get('result',[])
    else:
        return []


def delete_obj(ctx, obj_type, obj_id):
    url = "%s%s/%s" % (EGA_SUB_URL_PROD, _obj_type_to_endpoint(obj_type), obj_id)

    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }
    r = requests.delete(url, headers=headers)
    ctx.obj['LOGGER'].debug("Response after deleting '%s' with ID '%s': \n%s" % (obj_type, obj_id, r.text))  # for debug
    r_data = json.loads(r.text)

    if r_data['header']['code'] == "200":
        ctx.obj['LOGGER'].info("Deleted '%s' with ID '%s'" % (obj_type, obj_id))
    elif r_data['header']['code'] == "404":  # it is a bit odd to have 404 here, but it happened when we tried to delete an object we created earlier, it appears it got deleted earlier when it failed validation
        ctx.obj['LOGGER'].debug("Object '%s' with ID '%s' does not exist, no need to delete" % (obj_type, obj_id))
    else:
        ctx.obj['LOGGER'].warning("Failed deleting '%s' with ID '%s'" % (obj_type, obj_id))


def submit_submission(ctx,submission):
    url = "%ssubmissions/%s?action=SUBMIT" % (EGA_SUB_URL_PROD,ctx.obj['SUBMISSION']['id'])

    headers = {
        'Content-Type': 'application/json',
        'X-Token' : ctx.obj['SUBMISSION']['sessionToken']
    }

    requests.put(url,data=json.dumps(submission.to_dict()), headers=headers)