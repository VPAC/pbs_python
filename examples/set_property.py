#!/usr/bin/env python
#
# Author: Bas van der Vlies <basv@sara.nl>
# Date  : 17 Aug 2001
# Desc. : Set a node property
#
# CVS info:
# $Id: set_property.py,v 1.1 2002/02/27 14:35:51 sscpbas Exp $
#
#
#
import sys
import pbs

def main():
  pbs_server = pbs.pbs_default()
  if not pbs_server:
    print 'No default server'
    sys.exit(1)

  con = pbs.pbs_connect(pbs_server)

  attrop_l = pbs.new_attropl(1)
  attrop_l[0].name  = 'properties'
  attrop_l[0].value = 'set_something_useful'
  attrop_l[0].op    = pbs.INCR

  r =  pbs.pbs_manager(con, pbs.MGR_CMD_SET, pbs.MGR_OBJ_NODE, 
                    "e2", attrop_l, 'NULL')

  if r > 0:
    print r, ";", pbs.pbs_geterrmsg(con) 

main()
