from click import echo

from ..icgc.services import id_service
from ..ega.services import object_submission, delete_obj
from ..ega.entities import Attribute, SampleReference


class Submitter(object):
    def __init__(self, ctx):
        self.ctx = ctx

    def submit(self, submittable, dry_run=True):
        self.ctx.obj['LOGGER'].info("Processing '%s'" % submittable.submission_dir)

        if self.ctx.obj['CURRENT_DIR_TYPE'] == 'unaligned':
            try:
                if not dry_run:  # only to get ICGC ID when not dry_run
                    self.set_icgc_ids(submittable.sample, dry_run)

                object_submission(self.ctx, submittable.sample, 'sample', dry_run)
                submittable.record_object_status('sample', dry_run, self.ctx.obj['SUBMISSION']['id'], self.ctx.obj['log_file'])

                submittable.experiment.sample_id = submittable.sample.id
                submittable.experiment.study_id = self.ctx.obj['SETTINGS']['ega_study_id']

                object_submission(self.ctx, submittable.experiment, 'experiment', dry_run)
                submittable.record_object_status('experiment', dry_run, self.ctx.obj['SUBMISSION']['id'], self.ctx.obj['log_file'])

                submittable.run.sample_id = submittable.sample.id
                submittable.run.experiment_id = submittable.experiment.id

                object_submission(self.ctx, submittable.run, 'run', dry_run)
                submittable.record_object_status('run', dry_run, self.ctx.obj['SUBMISSION']['id'], self.ctx.obj['log_file'])

                self.ctx.obj['LOGGER'].info("Finished processing '%s'" % submittable.submission_dir)
            except Exception as error:
                self.ctx.obj['LOGGER'].error("Failed processing '%s': %s" % (submittable.submission_dir, error))
            finally:
                # we only clean up when it's dry_run, which will never turn something new into 'SUBMITTED'
                # objects created by dry_run that are not in 'SUBMITTED' status can be safely deleted
                if dry_run:
                    self.ctx.obj['LOGGER'].info('Clean up unneeded objects created by dry_run ...')
                    if not 'SUBMITTED' in submittable.sample.status and \
                            submittable.sample.id:
                        delete_obj(self.ctx, 'sample', submittable.sample.id)

                    # additional condition for run: can not delete run when the associated experiment is in SUBMITTED status
                    if not 'SUBMITTED' in submittable.experiment.status and \
                            not 'SUBMITTED' in submittable.run.status and \
                            submittable.run.id:  # need to delete run before experiment
                        delete_obj(self.ctx, 'run', submittable.run.id)

                    if not 'SUBMITTED' in submittable.experiment.status and \
                            submittable.experiment.id:
                        delete_obj(self.ctx, 'experiment', submittable.experiment.id)

        if self.ctx.obj['CURRENT_DIR_TYPE'] in ('alignment', 'variation'):
            try:
                if not dry_run:  # only to get ICGC ID when not dry_run
                    self.set_icgc_ids(submittable.sample, dry_run)

                object_submission(self.ctx, submittable.sample, 'sample', dry_run)
                submittable.record_object_status('sample', dry_run, self.ctx.obj['SUBMISSION']['id'], self.ctx.obj['log_file'])

                submittable.analysis.study_id = self.ctx.obj['SETTINGS']['ega_study_id']
                submittable.analysis.sample_references = [
                                                            SampleReference(
                                                                    submittable.sample.id,
                                                                    submittable.sample.alias
                                                                )
                                                            ]
                object_submission(self.ctx, submittable.analysis, 'analysis', dry_run)
                submittable.record_object_status('analysis', dry_run, self.ctx.obj['SUBMISSION']['id'], self.ctx.obj['log_file'])

                self.ctx.obj['LOGGER'].info('Finished processing %s' % submittable.submission_dir)
            except Exception as error:
                self.ctx.obj['LOGGER'].error('Failed processing %s: %s' % (submittable.submission_dir, str(error)))
            finally:
                # we only clean up when it's dry_run, which will never turn something new into 'SUBMITTED'
                # objects created by dry_run that are not in 'SUBMITTED' status can be safely deleted
                if dry_run:
                    self.ctx.obj['LOGGER'].info('Clean up unneeded objects created by dry_run ...')
                    if not 'SUBMITTED' in submittable.sample.status and \
                            submittable.sample.id:
                        delete_obj(self.ctx, 'sample', submittable.sample.id)

                    if not 'SUBMITTED' in submittable.analysis.status and \
                            submittable.analysis.id:
                        delete_obj(self.ctx, 'analysis', submittable.analysis.id)


    def set_icgc_ids(self, sample, dry_run=True):
        sample.attributes.append(
                Attribute(
                    'icgc_sample_id',
                    id_service(
                        self.ctx, 'sample',
                        self.ctx.obj['SETTINGS']['icgc_project_code'],
                        sample.alias,
                        True, # create param
                        dry_run  # is_test param, eq to dry_run
                    )
                )
            )

        sample.attributes.append(
                Attribute(
                    'icgc_donor_id',
                    id_service(
                        self.ctx, 'donor',
                        self.ctx.obj['SETTINGS']['icgc_project_code'],
                        sample.subject_id,
                        True,
                        dry_run
                    )
                )
            )

        sample.attributes.append(Attribute('submitted_using', 'egasub'))
