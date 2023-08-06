#!/usr/bin/env python
import os
import shutil

from setuptools import setup, find_packages
from distutils.command import clean


def get_version():
    """
    Determine a version string using git or a file VERSION.txt
    """
    # VERSION.txt is not added to git, it can be generated manually or by CI/CD
    version = '0.0.1'
    if os.path.isfile('VERSION.txt'):
        with open('VERSION.txt', 'r') as f:
            version = f.read().strip()
    return version


def get_readme():
    """
    Open and read the readme. This would be the place to convert to RST, but we no longer have to.
    """
    with open('README.md') as f:
        return f.read()


class PurgeCommand(clean.clean):
    """
    Custom command to purge everything
    """
    description = "purge 'build', 'dist', and '*.egg-info' directories"

    def run(self):
        super().run()
        if not self.dry_run:
            for path in ['build', 'dist', 'rds_secrets.egg-info']:
                os.path.isdir(path) and shutil.rmtree(path)


setup(
    name='confsecrets',
    version=get_version(),
    description='Simple utility to symmetrically encrypt/decrypt application secrets',
    long_description=get_readme(),
    long_description_content_type='text/markdown; charset=UTF-8; variant=CommonMark',
    author='Dan Davis',
    author_email='dan@danizen.net',
    maintainer='Dan Davis',
    maintainer_email='dan@danizen.net',
    url='https://github.com/danizen/confsecrets.git',
    project_urls={
        'Documentation': 'https://danizen.github.io/confsecrets/',
    },
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts': [
            'confsecrets=confsecrets.cli:main',
        ]
    },
    tests_require=['tox'],
    cmdclass={
        'purge': PurgeCommand,
    },
    install_requires=['cryptography'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ]
)
