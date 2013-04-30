#!/usr/bin/env python
#
# This file is subject to the terms and conditions defined in file
# 'LICENSE.txt', which is part of this source code package.

import sys
from setuptools import setup

setup(
    name='daemonic',
    version='0.5',
    description='Properly set up UNIX daemon processes',
    author='Eric Suh',
    author_email='contact@ericsuh.com',
    packages=['daemonic'],
    provides=['daemonic'],
    test_suite = 'tests.test_suite',
    url='http://github.com/ericsuh/daemonic',
    download_url='https://github.com/ericsuh/daemonic/zipball/master',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    long_description="""\
Daemonic
--------

Provides functions and classes to properly set up POSIX daemon processes,
including managing PID files.
""",
)
