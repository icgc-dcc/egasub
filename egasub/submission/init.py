from click import echo, prompt
import os
import yaml
import json
from ..ega.entities import Dac, Policy, Contact, Study, Submission, SubmissionSubsetData
from ..ega.services import login, logout, object_submission, query_by_type, prepare_submission
from ..exceptions import CredentialsError


def init_workspace(ctx,ega_submitter_account=None,ega_submitter_password=None,icgc_id_service_token=None,icgc_project_code=None):
    ctx.obj['LOGGER'].info('Initalizing EGA submission workspace...')
    ctx.obj['LOGGER'].info('Note: information collected below will be stored in')
    ctx.obj['LOGGER'].info('      \'.egasub/config.yaml\' which can be edited later.')
    
    projects = ["BLCA-CN","BOCA-FR","BOCA-UK","BRCA-EU","BRCA-FR","BRCA-KR","BRCA-UK","BTCA-JP","BTCA-SG","CLLE-ES","CMDI-UK",
            "COCA-CN","EOPC-DE","ESAD-UK","ESCA-CN","GACA-CN","LAML-CN","LAML-KR",
            "LIAD-FR","LICA-CN","LICA-FR","LIHM-FR","LINC-JP","LIRI-JP","LUSC-CN","LUSC-KR","MALY-DE","MELA-AU","ORCA-IN","OV-AU",
            "PACA-AU","PACA-CA","PAEN-AU","PAEN-IT","PBCA-DE","PRAD-CA","PRAD-UK","RECA-CN","RECA-EU","SKCA-BR","THCA-SA",
        ]
    
    #Ask user input for config.yaml
    if not ega_submitter_account:
        ega_submitter_account = prompt("Enter your EGA submitter account", default='')
    if not ega_submitter_password:
        ega_submitter_password = prompt("Enter your EGA submitter password", default='', hide_input=True)
    if not icgc_id_service_token:
        icgc_id_service_token = prompt("Enter your ICGC ID service token", default='')
    if not icgc_project_code:
        while True:
            icgc_project_code = prompt("Enter your ICGC project code", default='')
            if icgc_project_code.upper() in projects:
                break
            else:
                echo("Please enter a project from the following list:")
                echo('\t'.join(projects))
        
    yaml_info = {
        'ega_submitter_account': ega_submitter_account,
        'ega_submitter_password': ega_submitter_password,
        'icgc_id_service_token': icgc_id_service_token,
        'icgc_project_code': icgc_project_code.upper()
        }
    
    ctx.obj['LOGGER'].info("EGA and ICGC credentials collected")

    initialize_dac_policy_study(ctx, yaml_info, ega_submitter_account, ega_submitter_password)

    current_dir = ctx.obj['CURRENT_DIR']
    egasub_dir = os.path.join(current_dir,'.egasub')
    script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    
    if os.access(current_dir, os.W_OK):
        os.mkdir(egasub_dir)
        ctx.obj['LOGGER'].info("Creation of .egasub directory")
        
        with open(os.path.join(egasub_dir,'config.yaml'),'w') as outfile:
            yaml.safe_dump(yaml_info,outfile,default_flow_style=False)
            
        ctx.obj['LOGGER'].info("Credentials added to .egasub/config.yaml file")

        ctx.obj['LOGGER'].info('EGA submission workspace initialized')
        
    else:
        ctx.obj['LOGGER'].critical('Permission denied on directory '+current_dir)


def initialize_dac_policy_study(ctx, yaml_info, ega_submitter_account, ega_submitter_password):
    """
    Function to create dummy Dac and Policy, and associate existing EGA study with
    the EGA submission workspace to be initialized. Will create new EGA study if none exists 
    """
    if not ctx.obj.get('SETTINGS'):
        ctx.obj['SETTINGS'] = {}

    ctx.obj['SETTINGS']['ega_submitter_account'] = ega_submitter_account
    ctx.obj['SETTINGS']['ega_submitter_password'] = ega_submitter_password

    try:
        login(ctx)
    except CredentialsError as error:
        ctx.obj['LOGGER'].critical("Login failed: %s" % str(error))
        ctx.abort()

    ctx.obj['LOGGER'].info("Login success")
    submission = Submission('title', 'a description',SubmissionSubsetData.create_empty())
    prepare_submission(ctx, submission)

    # query for existing studies
    studies = query_by_type(ctx, 'study', obj_status="SUBMITTED")
    study_alias = None
    study_id = None
    if studies:
        """
        TO be implemented
        """
        echo("Please pickup one study from below or choose none to create a new study in the next step.")

    if not (study_alias and study_id):
        # let user create one
        echo("Please enter the following to create a new EGS study.")
        study = Study(
            prompt("Study alias (required)"), # alias
            prompt("Study type ID (required, 8 for Cancer Genomics)", default=8), # studyTypeId, Cancer Genomics
            prompt("Short study name", default=""), # should take it from config
            prompt("Study title (required)"), # should take it from config
            prompt("Study abstract (required)"), # should take it from config
            None,  # ownTerm
            [],  # pubMedIds
            [],   # customTags
            None
        )

        object_submission(ctx, study, 'study', dry_run=False)
        study_alias = study.alias
        study_id = study.id

    yaml_info['ega_study_alias'] = study_alias
    yaml_info['ega_study_id'] = study_id

    # new create dac and policy
    dac = make_dummy_dac()
    object_submission(ctx, dac, 'dac', dry_run=False)

    policy = make_dummy_policy(dac.id)
    object_submission(ctx, policy, 'policy', dry_run=False)

    yaml_info['ega_policy_id'] = policy.id

    login(ctx)


# EGA REST API based submission does not handle this properly yet,
# we were advised to create dummy Dac and Policy object to get things started 
def make_dummy_dac():
    return Dac(
            "ICGC DACO",
            [Contact("Helpdesk", "dcc-support@icgc.org", "ICGC", "")]
        )

def make_dummy_policy(dac_id):
    return Policy(
            "ICGC Data Access Agreements",
            dac_id,
            'ICGC Data Access',
            'Please use the ICGC website for applying access to the data',
            'http://www.icgc.org'
        )

