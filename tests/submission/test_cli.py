from egasub.cli import print_version, main, dry_run
import pytest
import os

def test_print_version(ctx):
    ctx.resilient_parsing = True
    assert print_version(ctx, 'version 1', True) is None
    ctx.resilient_parsing = False
    with pytest.raises(Exception):
        print_version(ctx, 'version 1', True)

def test_main(ctx):
    with pytest.raises(SystemExit):
        main()

#def test_dry_run(ctx):
#    dry_run(ctx, "tests/data/workspace/submittable")
