#!/usr/bin/env python
#
# Author: Bas van der Vlies <basv@sara.nl>
# Date  : 02 March 2005
# Desc. : Usage of the new PBSQuery module
#
# SVN info:
# $Id$
#
#
#

from PBSQuery import PBSQuery


import sys

def main():

  p = PBSQuery()

  nodes = p.getnodes()
  for name, node in nodes.items():
  	print node
	if node.is_free():
		print "%s : Found an free node" %name

  jobs = p.getjobs()
  for name, job in jobs.items():
     for key in job.keys():
        print '%s = %s', %(key, job[key])
 
  l = ['state', 'np' ]
  nodes = p.getnodes(l)
  for node in nodes.values():
     print node

main()
