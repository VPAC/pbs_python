#!/usr/bin/env python
#
# Author: Bas van der Vlies <basv@sara.nl>
# Date  : 27 Feb 2002
# Desc. : This will query the pbs_mom daemon about its resources
#
import pbs
import sys
import time
import socket

def main():
  server = pbs.pbs_default()
  c      = pbs.pbs_connect(server)

  nodes = pbs.pbs_statnode(c, '', 'NULL', 'NULL')

  for node in nodes:
    print node.name, ' :'
    attrs = node.attribs
    for attr in attrs:
      print '\t%s = %s' %(attr.name, attr.value)

    mom_port = socket.getservbyname('pbs_resmom', 'tcp')
    if mom_port:
      mom_id = pbs.openrm(node.name, mom_port)
    else:
      mom_id = pbs.openrm(node.name, pbs.PBS_MANAGER_SERVICE_PORT)

    mom_keys = pbs.get_mom_values(mom_id)
    for key in mom_keys.keys():
      print '\t%s = %s' %(key, mom_keys[key])

    print '\nTesting list with user supplied keywords'

    l = [ 'ncpus', 'loadave' ]
    mom_keys = pbs.get_mom_values(mom_id, l)
    for key in mom_keys.keys():
      print '\t%s = %s' %(key, mom_keys[key])
    print ''
    pbs.closerm(mom_id)


main()
