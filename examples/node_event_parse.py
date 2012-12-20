#!/usr/bin/env python
#
# Author: Bas van der Vlies <basv@sara.nl>
# Date  : 17 Aug 2001 
# Desc. : Simple pbsnodes -a
#
# SVN info:
#   $Id$
#   $URL$ 
#
#
#


import pbs
import sys
from PBSQuery import PBSQuery

p = PBSQuery()
node = p.getnode('gb-r7n3')
print node['event']
