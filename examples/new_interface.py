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

def main():

  p = PBSQuery()
  p.new_data_structure()

  jobs = p.getjobs()
  for id in jobs:
     print id + ':'
     for attr in jobs[id]:
        print '\t' + attr, jobs[id][attr]
     
  l = ['state', 'np' ]
  nodes = p.getnodes(l)
  for id in nodes:
     print id + ': ', nodes[id].state, nodes[id].np

     for attrib in nodes[id]:
     	print attrib, nodes[id][attrib]

main()
