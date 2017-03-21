from ..icgc.services import id_service
from ..ega.services import object_submission, delete_obj
from ..ega.entities import Attribute, SampleReference
from egasub import __version__ as ver


class Submitter(object):
    def __init__(self, ctx):
        self.ctx = ctx

    def submit(self, submittable, dry_run=True):
        self.ctx.obj['LOGGER'].info("Processing '%s'" % submittable.submission_dir)

        # sample readiness check, we can do submit sample when only when it's VALIDATED or SUBMITTED, in latter case, it will be just ignored but the submit process moves on
        if not dry_run and not submittable.sample.status in ('VALIDATED', 'SUBMITTED'):
            self.ctx.obj['LOGGER'].error("Failed processing '%s': sample object is not ready to 'submit', please try 'dry_run' first." % submittable.submission_dir)
            return

        if not dry_run:  # only to get ICGC ID when not dry_run
            try:
                self.set_icgc_ids(submittable.sample, dry_run)
            except Exception, err:
                self.ctx.obj['LOGGER'].error("Failed processing '%s', can not get ICGC ID, error: %s." % (submittable.submission_dir, err))
                return

        object_submission(self.ctx, submittable.sample, 'sample', dry_run)
        submittable.record_object_status('sample', dry_run, self.ctx.obj['SUBMISSION']['id'], self.ctx.obj['log_file'], submittable.sample.ega_accession_id)

        if self.ctx.obj['CURRENT_DIR_TYPE'] == 'unaligned':
            try:
                # readiness check before performing 'submit', this is helpful
                # preventing from the situation experiment is submitted but run failed
                if not dry_run and not (submittable.experiment.status in ('VALIDATED', 'SUBMITTED') and submittable.run.status == 'VALIDATED'):
                    raise Exception("Not ready to submit '%s' yet, please validate it using 'dry_run' instead. Experiment object status '%s', run object status '%s'" \
                                                    % (submittable.submission_dir, submittable.experiment.status, submittable.run.status))

                submittable.experiment.sample_id = submittable.sample.id
                submittable.experiment.study_id = self.ctx.obj['SETTINGS']['ega_study_id']

                object_submission(self.ctx, submittable.experiment, 'experiment', dry_run)
                submittable.record_object_status('experiment', dry_run, self.ctx.obj['SUBMISSION']['id'], self.ctx.obj['log_file'], submittable.experiment.ega_accession_id)

                submittable.run.sample_id = submittable.sample.id
                submittable.run.experiment_id = submittable.experiment.id

                object_submission(self.ctx, submittable.run, 'run', dry_run)
                submittable.record_object_status('run', dry_run, self.ctx.obj['SUBMISSION']['id'], self.ctx.obj['log_file'], submittable.run.ega_accession_id)

                self.ctx.obj['LOGGER'].info("Finished processing '%s'" % submittable.submission_dir)
            except Exception, error:
                self.ctx.obj['LOGGER'].error("Failed processing '%s': %s" % (submittable.submission_dir, error))
            finally:
                # we only clean up when it's dry_run, which will never turn something new into 'SUBMITTED'
                # objects created by dry_run that are not in 'SUBMITTED' status can be safely deleted
                if dry_run:
                    self.ctx.obj['LOGGER'].info('Clean up unneeded objects created by dry_run ...')
                    if not 'SUBMITTED' in str(submittable.sample.status) and \
                            submittable.sample.id:
                        delete_obj(self.ctx, 'sample', submittable.sample.id)

                    # additional condition for run: can not delete run when the associated experiment is in SUBMITTED status
                    if not 'SUBMITTED' in str(submittable.experiment.status) and \
                            not 'SUBMITTED' in str(submittable.run.status) and \
                            submittable.run.id:  # need to delete run before experiment
                        delete_obj(self.ctx, 'run', submittable.run.id)

                    if not 'SUBMITTED' in str(submittable.experiment.status) and \
                            submittable.experiment.id:
                        delete_obj(self.ctx, 'experiment', submittable.experiment.id)

        if self.ctx.obj['CURRENT_DIR_TYPE'] in ('alignment', 'variation'):
            try:
                # readiness check before performing 'submit'
                if not dry_run and not submittable.analysis.status == 'VALIDATED':
                    raise Exception("Not ready to submit '%s' yet, please validate it using 'dry_run' instead. Analysis object status '%s'" \
                                                    % (submittable.submission_dir, submittable.analysis.status))

                submittable.analysis.study_id = self.ctx.obj['SETTINGS']['ega_study_id']
                submittable.analysis.sample_references = [
                                                            SampleReference(
                                                                    submittable.sample.id,
                                                                    submittable.sample.alias
                                                                )
                                                            ]
                object_submission(self.ctx, submittable.analysis, 'analysis', dry_run)
                submittable.record_object_status('analysis', dry_run, self.ctx.obj['SUBMISSION']['id'], self.ctx.obj['log_file'], submittable.analysis.ega_accession_id)

                self.ctx.obj['LOGGER'].info('Finished processing %s' % submittable.submission_dir)
            except Exception, error:
                self.ctx.obj['LOGGER'].error('Failed processing %s: %s' % (submittable.submission_dir, error))
            finally:
                # we only clean up when it's dry_run, which will never turn something new into 'SUBMITTED'
                # objects created by dry_run that are not in 'SUBMITTED' status can be safely deleted
                if dry_run:
                    self.ctx.obj['LOGGER'].info('Clean up unneeded objects created by dry_run ...')
                    if not 'SUBMITTED' in str(submittable.sample.status) and \
                            submittable.sample.id:
                        delete_obj(self.ctx, 'sample', submittable.sample.id)

                    if not 'SUBMITTED' in str(submittable.analysis.status) and \
                            submittable.analysis.id:
                        delete_obj(self.ctx, 'analysis', submittable.analysis.id)


    def set_icgc_ids(self, sample, dry_run=True):

        icgc_sample_id = id_service(
            self.ctx, 'sample',
            self.ctx.obj['SETTINGS']['icgc_project_code'],
            sample.alias,
            True, # create param
            dry_run  # is_test param, eq to dry_run
        )

        sample.attributes.append(Attribute('_icgc_sample_id', icgc_sample_id))

        icgc_donor_id = id_service(
            self.ctx, 'donor',
            self.ctx.obj['SETTINGS']['icgc_project_code'],
            sample.subject_id,
            True,
            dry_run
        )
        sample.attributes.append(Attribute('_icgc_donor_id', icgc_donor_id))

        sample.attributes.append(Attribute('_submitted_using', 'egasub %s' % ver))
