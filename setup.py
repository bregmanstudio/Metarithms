#!/usr/bin/env python
import glob

from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib'] 

setup(name='metarithms',
      version='0.00',
      description='Metamusic creation by algorithms',
      long_description="""This package provides tools for representing musical sequences as lists and arrays, and for manipulating such sequences into multiple-viewpoint scores that can be rendered by external software. Requires numpy, some functionality depends on the Music21 python toolkit.""",

      author='Michael Casey',      
      author_email='mcasey [AT] dartmouth [DOT] edu',
      url='http://bregman.dartmouth.edu/',
      license='Apache v. 2.0 or higher',
      platforms=['OS X (any)', 'Linux (any)', 'Windows (any)'],
      packages=['metarithms']
     )
