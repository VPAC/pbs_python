#!/usr/bin/env python

import sys
import os

from distutils.core import setup, Extension 

# The location of the pbs libraries. If left blank
# then we try to find out where the libraries are
#
PBS_LIB_DIR=''

if not PBS_LIB_DIR:
  for dir in ['/usr/local/lib', '/opt/pbs/usr/lib' ]:
    dummy = os.path.join(dir, 'libpbs.a')
    if os.path.exists(dummy):
      PBS_LIB_DIR=dir
      break

if not PBS_LIB_DIR:
  print 'Please specify where the PBS libraries are!!'
  print 'edit setup.py and fill in the PBS_LIB_DIR variable'

setup ( name = 'pbs_python',
        version = '2.3',
	description = 'pbs python interface',
	author = 'Bas van der Vlies',
	author_email = 'basv@sara.nl',
	url = 'http://www.sara.nl/beowulf',

	extra_path = 'pbs',
        package_dir = { '' : 'src' }, 
	py_modules = [ 'pbs' ],

	ext_modules = [ 
	  Extension( 'pbscmodule', ['src/pbs_wrap.c'],
	  library_dirs = [ PBS_LIB_DIR ],
	  libraries = ['log', 'net', 'pbs']
	  ) 
	]
)

