import os
import click
import utils


@click.group()
@click.option('--debug/--no-debug', '-d', default=False, envvar='EGASUB_DEBUG')
@click.pass_context
def main(ctx, debug):
    # initializing ctx.obj
    ctx.obj = {}
    ctx.obj['DEBUG'] = debug
    ctx.obj['IS_TEST'] = False
    if ctx.obj['DEBUG']: click.echo('Debug is on.', err=True)


@main.command()
@click.argument('source', type=click.Path(exists=True), nargs=-1)
@click.pass_context
def submit(ctx, source):
    utils.initialize_app(ctx)
    if not ctx.obj.get('WORKSPACE_PATH'):
        click.echo('Not in an EGA submission workspace %s' % ctx.obj['WORKSPACE_PATH'])
        ctx.abort()

    click.echo(source)


@main.command()
@click.argument('source', type=click.Path(exists=True), nargs=-1)
@click.pass_context
def report(ctx, source):
    utils.initialize_app(ctx)
    if not ctx.obj.get('WORKSPACE_PATH'):
        click.echo('Not in an EGA submission workspace %s' % ctx.obj['WORKSPACE_PATH'])
        ctx.abort()

    click.echo(source)


@main.command()
@click.pass_context
def init(ctx):
    """
    Run once to create a submission workspace.
    """
    # To be implemented

    if ctx.obj.get('WORKSPACE_PATH'):
        click.echo('Already in an EGA submission workspace %s' % ctx.obj['WORKSPACE_PATH'])
        ctx.abort()


if __name__ == '__main__':
  main()

