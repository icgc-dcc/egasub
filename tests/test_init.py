import os
import click
from click.testing import CliRunner
from egasub.cli import init

def test_init_function():    
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        result = runner.invoke(init)
        assert True