#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup
from re import search


def get_version():
    with open('kiss_headers/version.py') as version_file:
        return search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                      version_file.read()).group('version')


# Package meta-data.
NAME = 'kiss-headers'
DESCRIPTION = 'Headers: Keep-It=Simple; And=Stupid.'
URL = 'https://github.com/ousret/kiss-headers'
EMAIL = 'ahmed.tahri@cloudnursery.dev'
AUTHOR = 'Ahmed TAHRI @Ousret'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = get_version()

REQUIRED = [
    'cached_property',
    'requests'
]

EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    keywords=['headers', 'http', 'mail', 'text', 'imap', 'header', 'https', 'imap4'],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
