#!/usr/bin/env python
#
# $Id$

import sys
import os

from distutils.core import setup, Extension 

# The location of the pbs libraries. If left blank
# then we try to find out where the libraries are
#
PBS_LIB_DIR=''
LIBS = ['log', 'net', 'pbs'] 

if not PBS_LIB_DIR:
  for dir in ['/usr/lib', '/usr/local/lib', '/opt/pbs/usr/lib', '/usr/lib/torque', '/opt/pbs/lib', '/opt/torque/lib' ]:
    dummy = os.path.join(dir, 'libpbs.a')
    if os.path.exists(dummy):
      PBS_LIB_DIR=dir
      break

if not PBS_LIB_DIR:
  print 'Please specify where the PBS libraries are!!'
  print 'edit setup.py and fill in the PBS_LIB_DIR variable'
  sys.exit(1)

# Test if we have all the libs:
#
for lib in LIBS:
  library = 'lib%s.a' %(lib) 
  dummy = os.path.join(PBS_LIB_DIR, library)
  if not os.path.exists(dummy):
    print 'You need to install "%s" in %s' %(library, PBS_LIB_DIR)
    sys.exit(1)

setup ( name = 'pbs_python',
        version = '2.7.10',
	description = 'openpbs/torque python interface',
	author = 'Bas van der Vlies',
	author_email = 'basv@sara.nl',
	url = 'http://www.sara.nl/index_eng.html',

	extra_path = 'pbs',
        package_dir = { '' : 'src' }, 
	py_modules = [ 'pbs', 'PBSQuery' ],

	ext_modules = [ 
	  Extension( '_pbs', ['src/pbs_wrap.c'],
	  library_dirs = [ PBS_LIB_DIR ],
	  libraries = LIBS
	  ) 
	]
)

