#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools.command.test import test as TestCommand

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        tox.cmdline(args=args)

setup(
    name='jenkins-job-builder-addons',
    version='1.0.0',
    description="A suite of jenkins job builder addons",
    long_description=readme + '\n\n' + history,
    author="Mike Buzzetti",
    author_email='mike.buzzetti@gmail.com',
    url='https://github.com/jimbydamonk/jenkins-job-builder-addons',
    packages=['jenkins_jobs_addons'],
    include_package_data=True,
    install_requires=requirements,
    license="Apache",
    zip_safe=False,
    keywords='jenkins ',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=['tox'] + test_requirements,
    cmdclass={'test': Tox},
    entry_points={
        'jenkins_jobs.projects': [
            'folder=jenkins_jobs_addons.folders:Folder',
        ],
        'jenkins_jobs.views': [
            'all=jenkins_jobs_addons.views:all_view',
            'build_pipeline=jenkins_jobs_addons.views:build_pipeline_view',
            'delivery_pipeline=jenkins_jobs_addons.'
            'views:delivery_pipeline_view'
        ],
        'jenkins_jobs.modules': [
            'views=jenkins_jobs_addons.views:Views'

        ]
    },
)
