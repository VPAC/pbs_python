#! /usr/bin/env python
#
#	pbsmon	WJ104
#	added START_RACK BvdV ;-)
#       added Total, pbs_serial_free and pbs_parallel free, BvdV
#
#	Hint: set ts=4
#
#	SVN Info:
#		$Id$
#
import os
import sys
import string

import pbs
from PBSQuery import PBSQuery

NODES_PER_RACK = 20
START_RACK = 16
N_RACKS = 36

pbs_ND_single			= 'job (single)'
pbs_ND_total			= 'total'
pbs_ND_free_serial		= 'free serial'
pbs_ND_free_parallel	= 'free parallel'

PBS_STATES = {
	pbs.ND_free				: '_',
	pbs.ND_down				: 'X',
	pbs.ND_offline			: '.',
	pbs.ND_reserve			: 'R',
	pbs.ND_job_exclusive	: 'J',
	pbs.ND_job_sharing		: 'S',
	pbs.ND_busy				: '*',
	pbs.ND_state_unknown	: '?',
	pbs.ND_timeshared		: 'T',
	pbs.ND_cluster			: 'C',
	pbs_ND_single			: 'j',
	pbs_ND_free_serial		: ' ',
	pbs_ND_free_parallel	: ' ',
	pbs_ND_total			: ' '
}

def pbsmon():
	global NODES_PER_RACK, N_RACKS, PBS_STATES

	if len(sys.argv) > 1:
		p = PBSQuery(sys.atgv[1])
	else:
		p = PBSQuery()

# get the state of the nodes
	attr = [ 'state', 'jobs', 'properties' ]
	nodes = p.getnodes(attr)

	node_dict = {}

	count_states = {}
	for key in PBS_STATES.keys():
		count_states[key] = 0

	for nodename, node in nodes.items():

		# Skip login nodes in status display
		#
		if not nodename.find('login'):
			continue

		# Only interested in the first state of a node
		#
		state = string.splitfields(node['state'], ',')[0]
		state_char = PBS_STATES[state]
		count_states[state] += 1
		count_states[pbs_ND_total] += 1

		if node.is_free(): 
			if node.has_job():
#				print 'TD: %s' % nodename, node
				state_char = PBS_STATES[pbs_ND_single]
				count_states[pbs.ND_free] -=  1
				count_states[pbs_ND_single] += 1
			else:
				if  node['properties'].find('gigabit') == 0:
					count_states[pbs_ND_free_serial] +=  1 
				else:
					count_states[pbs_ND_free_parallel] +=  1 
				
#		print 'TD: %s %s' % (nodename, state_char)
		dummy = string.split(nodename, '-')
		node_dict[dummy[1]] = state_char

	legend = PBS_STATES.keys()
	legend.sort()

# print nodes with r%dn%d naming scheme
	print '  ',
	for rack in xrange(START_RACK, N_RACKS+1):
		print '%2d' % rack,
	print

	for node_nr in xrange(1, NODES_PER_RACK+1):
		print '%2d' % node_nr,

		for rack in xrange(START_RACK, N_RACKS+1):
			node_name = 'r%dn%d' % (rack, node_nr)

			if node_dict.has_key(node_name):
				print ' %s' % node_dict[node_name],

				del node_dict[node_name]
			else:
				print '  ',

		if node_nr-1 < len(legend):
			state = legend[node_nr-1]
			print '  %s  %-13s : %d' % (PBS_STATES[state], state, count_states[state])
		else:
			print

	print

# any other nodes?
	arr = node_dict.keys()
	if arr:
		arr.sort()

		for node in arr:
			print '%s %s' % (node, node_dict[node])

		print

#	n = 0
#	for state in legend:
#		print '%s  %-13s : %-3d     ' % (PBS_STATES[state], state, count_states[state]),
#		n = n + 1
#		if n > 1:
#			n = 0
#			print


if __name__ == '__main__':
	pbsmon()


# EOB

