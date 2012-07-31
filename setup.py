#!/usr/bin/env python

from distutils.core import setup

setup(name='rmodel',
      description='simple redis model',
      author='dsociative',
      author_email='admin@geektech.ru',
      packages=['rmodel', 'rmodel.fields', 'rmodel.models'],
      package_dir={'rmodel': 'rmodel'},
     )
