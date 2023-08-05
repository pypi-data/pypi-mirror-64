#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    reshapedata LLC
"""
import platform
from setuptools import setup
from setuptools import find_packages

setup(
    name = 'rdlaiye',
    version = '1.0.0',
    install_requires=[
        'requests',
        'time',
        'json',
        'hashlib',
        'string',
        'random',
    ],
    packages=find_packages(),
    license = 'Apache License',
    author = 'Reshapedata',
    author_email = 'hulilei@takewiki.com.cn',
    url = 'http://www.reshapedata.com',
    description = 'test for python pkg',
    keywords = ['reshapedata', 'takewiki'],
    python_requires='>=3.6',
)
