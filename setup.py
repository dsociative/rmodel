#!/usr/bin/env python

from setuptools import setup


setup(
    name='rmodel',
    description='simple redis model',
    author='dsociative',
    author_email='admin@geektech.ru',
    packages=['rmodel', 'rmodel.fields', 'rmodel.models', 'rmodel.sessions'],
    package_dir={'rmodel': 'rmodel'},
    dependency_links=[
        'http://github.com/dsociative/ztest/tarball/master#egg=ztest-0.0.0',
    ],
    install_requires=[
        'redis',
        'ztest'
    ],
    version='0.1.3'
)
