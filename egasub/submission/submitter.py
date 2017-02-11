from click import echo

from ..icgc.services import id_service
from ..ega.services import object_submission, delete_obj
from ..ega.entities import Attribute, SampleReference


class Submitter(object):
    def __init__(self, ctx):
        self.ctx = ctx

    def submit(self, submittable, dry_run=True):
        if self.ctx.obj['CURRENT_DIR_TYPE'] == 'unaligned':
            self.ctx.obj['LOGGER'].info("Processing '%s'" % submittable.sample.alias)

            try:
                if not dry_run:  # only to get ICGC ID when not dry_run
                    self.set_icgc_ids(submittable.sample, dry_run)
                object_submission(self.ctx, submittable.sample, 'sample', dry_run)
                submittable.record_object_status('sample')

                submittable.experiment.sample_id = submittable.sample.id
                submittable.experiment.study_id = self.ctx.obj['SETTINGS']['ega_study_id']

                object_submission(self.ctx, submittable.experiment, 'experiment', dry_run)
                submittable.record_object_status('experiment')

                submittable.run.sample_id = submittable.sample.id
                submittable.run.experiment_id = submittable.experiment.id

                object_submission(self.ctx, submittable.run, 'run', dry_run)
                submittable.record_object_status('run')

                self.ctx.obj['LOGGER'].info('Finished processing %s' % submittable.sample.alias)
            except Exception as error:
                self.ctx.obj['LOGGER'].error('Failed processing %s: %s' % (submittable.sample.alias, error))

            # now remove all created object that is not in SUBMITTED status
            self.ctx.obj['LOGGER'].info('Clean up unneeded objects ...')
            if not submittable.sample.status == 'SUBMITTED' and submittable.sample.id:
                delete_obj(self.ctx, 'sample', submittable.sample.id)

            if not submittable.run.status == 'SUBMITTED' and submittable.run.id:  # need to delete run before experiment
                delete_obj(self.ctx, 'run', submittable.run.id)

            if not submittable.experiment.status == 'SUBMITTED' and submittable.experiment.id:
                delete_obj(self.ctx, 'experiment', submittable.experiment.id)


        if self.ctx.obj['CURRENT_DIR_TYPE'] in ('alignment', 'variation'):
            try:
                if not dry_run:  # only to get ICGC ID when not dry_run
                    self.set_icgc_ids(submittable.sample, dry_run)
                object_submission(self.ctx, submittable.sample, 'sample', dry_run)
                submittable.record_object_status('sample')

                submittable.analysis.study_id = self.ctx.obj['SETTINGS']['ega_study_id']
                submittable.analysis.sample_references = [
                                                            SampleReference(
                                                                    submittable.sample.id,
                                                                    submittable.sample.alias
                                                                )
                                                            ]
                object_submission(self.ctx, submittable.analysis, 'analysis', dry_run)
                submittable.record_object_status('analysis')

                self.ctx.obj['LOGGER'].info('Finished processing %s' % submittable.sample.alias)
            except Exception as error:
                self.ctx.obj['LOGGER'].error('Failed processing %s: %s' % (submittable.sample.alias, str(error)))

            # now remove all created object that is not in SUBMITTED status
            self.ctx.obj['LOGGER'].info('Clean up unneeded objects ...')
            if not submittable.sample.status == 'SUBMITTED' and submittable.sample.id:
                delete_obj(self.ctx, 'sample', submittable.sample.id)

            if not submittable.analysis.status == 'SUBMITTED' and submittable.analysis.id:
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
