#!/usr/bin/env python
#
# Author: Bas van der Vlies <basv@sara.nl>
# Date  : 17 Aug 2001 
# Desc. : Simple pbsnodes -a
#
# CVS info:
# $Author: sscpbas $
# $Date: 2001/12/07 19:01:18 $
# $Revision: 1.1 $
# $Log: pbsnodes-a.py,v $
# Revision 1.1  2001/12/07 19:01:18  sscpbas
# Initial revision
#
#


import pbs

def main():

  pbs_server = pbs.pbs_default()
  if not pbs_server:
    print "No default pbs server"
    sys.exit(1)

  con = pbs.pbs_connect(pbs_server)
  nodes = pbs.pbs_statnode(con, "", "NULL", "NULL")

  for node in nodes:
    print node.name
    for attrib in node.attribs:
      print '\t', attrib.name, '=', attrib.value

main()
