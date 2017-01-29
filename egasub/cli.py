import os
import click
import utils
from click import echo
from submission import init_workspace, perform_submission, perform_submission_old


@click.group()
@click.option('--debug/--no-debug', '-d', default=False, envvar='EGASUB_DEBUG')
@click.pass_context
def main(ctx, debug):
    # initializing ctx.obj
    ctx.obj = {}
    ctx.obj['DEBUG'] = debug
    ctx.obj['IS_TEST'] = False
    if ctx.obj['DEBUG']: click.echo('Debug is on.', err=True)

    ctx.obj['CURRENT_DIR'] = os.getcwd()
    ctx.obj['IS_TEST_PROJ'] = None
    ctx.obj['WORKSPACE_PATH'] = utils.find_workspace_root(cwd=ctx.obj['CURRENT_DIR'])


@main.command()
@click.argument('source', type=click.Path(exists=True), nargs=-1)
@click.pass_context
def submit(ctx, source):
    utils.initialize_app(ctx)
    if not ctx.obj.get('WORKSPACE_PATH'):
        echo('Error: Not in an EGA submission workspace %s' % ctx.obj['WORKSPACE_PATH'])
        ctx.abort()

    if not source:
        echo('Error: You must specify at least one submission directory.')
        ctx.abort()

    # to be replaced by perform_submission
    perform_submission_old(ctx, source)

@main.command()
@click.argument('source', type=click.Path(exists=True), nargs=-1)
@click.pass_context
def dry_run(ctx, source):
    utils.initialize_app(ctx)
    if not ctx.obj.get('WORKSPACE_PATH'):
        echo('Error: Not in an EGA submission workspace %s' % ctx.obj['WORKSPACE_PATH'])
        ctx.abort()

    if not source:
        echo('Error: You must specify at least one submission directory.')
        ctx.abort()

    perform_submission(ctx, source, True)


@main.command()
@click.argument('source', type=click.Path(exists=True), nargs=-1)
@click.pass_context
def report(ctx, source):
    utils.initialize_app(ctx)
    if not ctx.obj.get('WORKSPACE_PATH'):
        click.echo('Not in an EGA submission workspace %s' % ctx.obj['WORKSPACE_PATH'])
        ctx.abort()

    echo(source)


@main.command()
@click.option('--ega_submitter_account')
@click.option('--ega_submitter_password')
@click.option('--icgc_id_service_token')
@click.option('--icgc_project_code')
@click.pass_context
def init(ctx,ega_submitter_account,ega_submitter_password,icgc_id_service_token,icgc_project_code):
    """
    Run once to create a submission workspace.]
    """

    if ctx.obj.get('WORKSPACE_PATH'):
        click.echo('Already in an EGA submission workspace %s' % ctx.obj['WORKSPACE_PATH'])
        ctx.abort()

    init_workspace(ctx,ega_submitter_account,ega_submitter_password,icgc_id_service_token,icgc_project_code )


if __name__ == '__main__':
  main()

