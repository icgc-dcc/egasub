import os
import click
import utils
from click import echo
from submission import init_workspace, perform_submission


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

    perform_submission(ctx, source)


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
@click.argument('credentials',nargs=-1)
@click.pass_context
def init(ctx,credentials):
    """
    Run once to create a submission workspace.]
    egasub init ega_submitter_account ega_submitter_password icgc_id_service_token icgc_project_code
    """

    if ctx.obj.get('WORKSPACE_PATH'):
        click.echo('Already in an EGA submission workspace %s' % ctx.obj['WORKSPACE_PATH'])
        ctx.abort()
        
    ega_submitter_account = credentials[0] if len(credentials)>0  else None
    ega_submitter_password = credentials[1] if len(credentials)>1  else None
    icgc_id_service_token = credentials[2] if len(credentials)>2  else None
    icgc_project_code = credentials[3] if len(credentials)>3  else None

    init_workspace(ctx,ega_submitter_account,ega_submitter_password,icgc_id_service_token,icgc_project_code )


if __name__ == '__main__':
  main()

