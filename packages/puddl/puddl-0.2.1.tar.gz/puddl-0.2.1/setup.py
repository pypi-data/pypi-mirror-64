#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    install_requires=[
        'django',
        'requests',
        'psycopg2-binary',
        'tinytag',
        'supervisor',
        'Click',
        'ffmpeg-python',
        'filetype',
    ],
    entry_points='''
        [console_scripts]
        puddl=puddl.cli:main
    ''',
)
