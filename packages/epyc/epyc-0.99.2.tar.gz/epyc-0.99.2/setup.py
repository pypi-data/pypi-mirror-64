#!/usr/bin/env python

# Setup for epyc
#
# Copyright (C) 2016--2019 Simon Dobson
#
# This file is part of epyc, experiment management in Python.
#
# epyc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epyc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epyc. If not, see <http://www.gnu.org/licenses/gpl.html>.

from setuptools import setup

with open('README.rst') as f:
    longDescription = f.read()

setup(name = 'epyc',
      version = '0.99.2',
      description = 'Python computational experiment management',
      long_description = longDescription,
      url = 'http://github.com/simoninireland/epyc',
      author = 'Simon Dobson',
      author_email = 'simon.dobson@computer.org',
      license = 'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
      classifiers = [ 'Development Status :: 4 - Beta',
                      'Intended Audience :: Science/Research',
                      'Intended Audience :: Developers',
                      'Programming Language :: Python :: 2.7',
                      'Programming Language :: Python :: 3.7',
                      'Topic :: Scientific/Engineering' ],
      packages = [ 'epyc' ],
      scripts = [  ],
      zip_safe = True,
      install_requires = [  ])


