#!/usr/bin/env python
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from pip.req import parse_requirements
from pip.download import PipSession

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


install_reqs = parse_requirements('requirements.txt', session=PipSession())
tests_require = parse_requirements('requirements-test.txt', session=PipSession())

setup(
    name = 'egasub',
    description = 'ICGC tool for assisting EGA data submission',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires = [str(ir.req) for ir in install_reqs],
    tests_require = [str(ir.req) for ir in tests_require],
    cmdclass = {'test': PyTest},
    package_data={'egasub': [
                                'ega/data/enums/*.json',
                                'submission/metadata_template/*/*.yaml'
                            ]},
    include_package_data = True,
    entry_points={
        'console_scripts': [
            'egasub=egasub.cli:main',
        ]
    },
)
