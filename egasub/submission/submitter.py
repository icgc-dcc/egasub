from click import echo

from ..icgc.services import id_service
from ..ega.services import login, logout, object_submission, delete_obj
from ..ega.entities import Attribute


class Submitter(object):
    def __init__(self, ctx):
        self.ctx = ctx

    def submit(self, submittable, dry_run=True):
        if self.ctx.obj['CURRENT_DIR_TYPE'] == 'unaligned':
            self.ctx.obj['LOGGER'].info("Processing '%s'" % submittable.sample.alias)

            try:
                submittable.sample.attributes.append(
                        Attribute(
                            'icgc_sample_id',
                            id_service(self.ctx, 'sample',
                                self.ctx.obj['SETTINGS']['icgc_project_code'],
                                submittable.sample.alias,
                                True,True
                            )
                        )
                    )
                submittable.sample.attributes.append(
                        Attribute(
                            'icgc_donor_id',
                            id_service(self.ctx, 'donor',
                                self.ctx.obj['SETTINGS']['icgc_project_code'],
                                submittable.sample.subject_id,
                                True,True
                            )
                        )
                    )

                # set update_if_exist to True by default for now
                # proper way to do it is to set to True when there is a change
                # TODO: add hash property to Sample, Experiment etc object, in order to be able
                #       to detect change
                object_submission(self.ctx, submittable.sample, 'sample', dry_run)
                submittable.record_object_status('sample')

                submittable.experiment.sample_id = submittable.sample.id
                submittable.experiment.study_id = self.ctx.obj['SETTINGS']['STUDY_ID']

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


        if self.ctx.obj['CURRENT_DIR_TYPE'] == 'alignment':
            """
            TODO: to be implemented
            """
            echo("Not implemented yet.")

        if self.ctx.obj['CURRENT_DIR_TYPE'] == 'variation':
            """
            TODO: to be implemented
            """
            echo("Not implemented yet.")

