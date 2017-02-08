from click import echo

from ..icgc.services import id_service
from ..ega.services import login, logout, object_submission
from ..ega.entities import Attribute


class Submitter(object):
    def __init__(self, ctx):
        self.ctx = ctx

    def submit(self, submittable, dry_run=True):
        if self.ctx.obj['CURRENT_DIR_TYPE'] == 'unaligned':
            self.ctx.obj['LOGGER'].info('Processing %s' % submittable.sample.alias)

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


                object_submission(self.ctx, submittable.sample, 'sample', dry_run)

                submittable.experiment.sample_id = submittable.sample.id
                submittable.experiment.study_id = self.ctx.obj['SETTINGS']['STUDY_ID']

                object_submission(self.ctx, submittable.experiment, 'experiment', dry_run)
                submittable.run.sample_id = submittable.sample.id
                submittable.run.experiment_id = submittable.experiment.id
                object_submission(self.ctx, submittable.run, 'run', dry_run)

                self.ctx.obj['LOGGER'].info('Finished processing %s' % submittable.sample.alias)
            except Exception as error:
                self.ctx.obj['LOGGER'].error(error)

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

