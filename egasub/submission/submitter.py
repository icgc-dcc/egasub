from click import echo

from ..icgc.services import id_service
from ..ega.services import login, logout, submit_obj
from ..ega.entities import Attribute


class Submitter(object):
    def __init__(self, ctx):
        self.ctx = ctx

    def submit(self, submittable, dry_run=None):
        if self.ctx.obj['CURRENT_DIR_TYPE'] == 'unaligned':
            echo(' Processing %s' % submittable.sample.alias)

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

                submit_obj(self.ctx, submittable.sample, 'sample')

                submittable.experiment.sample_id = submittable.sample.id
                submittable.experiment.study_id = self.ctx.obj['SETTINGS']['STUDY_ID']

                submit_obj(self.ctx, submittable.experiment, 'experiment')
                submittable.run.sample_id = submittable.sample.id
                submittable.run.experiment_id = submittable.experiment.id
                submit_obj(self.ctx, submittable.run, 'run')

                echo(' Finished processing %s' % submittable.sample.alias)
            except Exception as error:
                echo('Error caught: '+repr(error))

        if self.ctx.obj['CURRENT_DIR_TYPE'] == 'alignment':
            """
            TODO: to be implemented
            """
            #print submittable.sample.to_dict()
            #print submittable.analysis.to_dict()
            echo("Not implemented yet.")

        if self.ctx.obj['CURRENT_DIR_TYPE'] == 'variation':
            """
            TODO: to be implemented
            """
            echo("Not implemented yet.")

