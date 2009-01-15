#!/usr/bin/env python

from distutils.core import setup

setup(
  name         = 'PySch',
  version      = '0.1',
  description  = 'Scheme in Python',
  author       = 'Paul Driver',
  author_email = 'frodwith@gmail.com',
  packages     = ['pysch'],
  package_dir  = {'': 'lib'},
)

