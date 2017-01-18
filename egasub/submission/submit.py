from ..ega.entities.sample import Sample
from ..ega.entities.analysis import Analysis
from ..ega.entities.run import Run
from ..ega.entities.experiment import Experiment
from ..icgc.services import id_service
from ..exceptions import ImproperlyConfigured, EgaSubmissionError, EgaObjectExistsError
from click import echo

def metadata_parser(ctx, metadata):
    pass


def submit_object(ctx, object):
    pass


def perform_submission(ctx, submission_dirs):
    echo(submission_dirs)

