#!/usr/bin/env python
# -*- coding: utf-8 -*-
from io import open
from setuptools import setup


version = '1.3'

setup(
    name='yunnet',
    version=version,

    author='Yunnet',
    author_email='unt@yunnet.ru',

    description=(
        u'YunnetApi'
    ),

    license='Apache License, Version 2.0',

    packages=['yunnet'],
    install_requires=['requests'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
