#!/usr/bin/env python
#
"""
 Author: Bas van der Vlies
 Date  : 1 June 2012
 Desc. : Standard python module to parse accounting files for TORQUE

 SVN Info:
    $Id$
    $URL$

Torque Info:
 abort   Job has been aborted by the server
  C   checkpoint  Job has been checkpointed and held
  D   delete  Job has been deleted
  E   exit    Job has exited (either successfully or unsuccessfully)
  Q   queue   Job has been submitted/queued
  R   rerun   Attempt to rerun the job has been made
  S   start   Attempt to start the job has been made (if the job fails to properly start, it may have multiple job start records)
  T   restart     Attempt to restart the job (from checkpoint) has been made (if the job fails to properly start, it may have multiple job start records)

 ctime   Time job was created
 etime   Time job became eligible to run
 qtime   Time job was queued
 start   Time job started to run

  05/30/2012 23:59:46;E;6155805.batch1.irc.sara.nl;user=rvosmeer group=rvosmeer jo
  bname=grid_ef_GROUP18 queue=serial ctime=1338411242 qtime=1338411242 etime=13384
  11242 start=1338414827 owner=rvosmeer@login4.irc.sara.nl exec_host=gb-r3n8/7+gb-r3n8/6+gb-r3n8/5+gb-r3n8/4+gb-r3n8/3+gb-r3n8/2+gb-r3n8/1+gb-r3n8/0 Resource_List.arch=x86_64 Resource_List.ncpus=1 Resource_List.neednodes=1:cores8:ppn=8 Resource_List.nodect=1 Resource_List.nodes=1:cores8:ppn=8 Resource_List.walltime=00:20:00 session=22781 end=1338415186 Exit_status=0 resources_used.cput=00:05:49 resources_used.mem=238052kb resources_used.vmem=351124kb resources_used.walltime=00:06:00

"""
import os
import string
import re
import sys

def get_nodes(nodes, unique=None):
    """
    Returns a list of the nodes which run this job
    format:
    * exec_host: gb-r10n14/5+gb-r10n14/4+gb-r10n14/3+gb-r10n14/2+gb-r10n14/1+gb-r10n14/0
    * split on '+' and if uniq is set split on '/'
"""

    if nodes:
        nodelist = string.split(nodes,'+') 
        if not unique:
             return nodelist
        else:
            l = list()

            for n in nodelist:
                t = string.split(n,'/')
                if t[0] not in l:
                    l.append(t[0])

            return l

def get_racks( host_l ):

    NODE_EXPR = "gb-r(?P<racknr>[0-9]+)n(?P<nodenr>[0-9]+)"

    racks = list()
    for h in host_l:
        parts = re.search( r'%s' % NODE_EXPR, h, re.VERBOSE )

        try:

            racknr = parts.group( 'racknr' )
            if not racknr in racks:
                racks.append(racknr)

        except Exception: 
            pass

        return racks
            



def parse_key_value( d, state, line):
    """
    user=rvosmeer group=rvosmeer jobname=FRAME_398_SPq.adf.job ...
    a value can also contain a '=' character
    """
    key_value_pairs = line.split()

    for entry in key_value_pairs:
        key_value_l = entry.split('=')
        k = key_value_l[0].strip()
        v = ''.join(key_value_l[1:]).strip()
        d[state][ k ] = v

        if k in ['exec_host']:
            d[state]['host_list'] = get_nodes( v, True)
            d[state]['rack_list'] = get_racks( d[state]['host_list'] )


def read_file(file, d):

    fd = open(file, 'r')

    go = True
    while go:
        line = fd.readline() 
        
        l = line.split(';') 
        
        if not line: 
            break
   
        jobid = l[2].strip()
        if not d.has_key( jobid ):
            d[ jobid ] = dict()
   

        if l[1] == 'S':

            try:
                d[ jobid ]['start']['retry_count'] += 1
                parse_key_value( d[ jobid ], 'start', ' '.join(l[3:])) 

            except KeyError:
                d[ jobid ]['start'] = dict()
                d[ jobid ]['start']['retry_count'] = 0
                parse_key_value( d[ jobid ], 'start', ' '.join(l[3:])) 

        elif l[1] == 'C':
            d[ jobid ]['checkpoint'] =  l[3:]
            parse_key_value( d[ jobid ], 'checkpoint', ' '.join(l[3:])) 

        elif l[1] == 'D':
            d[ jobid ]['deleted'] = dict()
            parse_key_value( d[ jobid ], 'deleted', ' '.join(l[3:])) 

        elif l[1] == 'E':
            d[ jobid ]['exit'] = dict()
            parse_key_value( d[ jobid ], 'exit', ' '.join(l[3:])) 

        elif l[1] == 'Q':
            d[ jobid ]['queued'] = dict()
            parse_key_value( d[ jobid ], 'queued', ' '.join(l[3:])) 

        elif l[1] == 'R':
            d[ jobid ]['rerun'] = dict()
            parse_key_value( d[ jobid ], 'rerun', ' '.join(l[3:])) 

        elif l[1] == 'T':
            d[ jobid ]['restart'] = dict()
            parse_key_value( d[ jobid ], 'restart', ' '.join(l[3:])) 



serial_jobs = 0
parallel_jobs = 0
express_jobs = 0
serial_jobs_on_parallel_node = 0
total_jobs = 0

jobs = dict()
parallel_job_len = dict()

for f in sys.argv[1:] :

    read_file(f, jobs)


for j in jobs.keys():

    if jobs[j].has_key('restart'):
        print j, jobs[j]['restart']

sys.exit(0)
for j in jobs.keys():

    if jobs[j].has_key('exit'):

        record = jobs[j]['exit']

        total_jobs += 1

        if record['queue'] in [ 'serial']:
            serial_jobs += 1 

            if record['rack_list'][0] in [ '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13' ]:
                serial_jobs_on_parallel_node += 1

        elif record['queue'] in [ 'parallel']:
            parallel_jobs += 1
            try:
                number_of_hosts = len(record['host_list']) 
                parallel_job_len[ number_of_hosts ]['number'] += 1
                #parallel_job_len[ number_of_hosts ] ['walltime'].append(record['Resource_List.walltime'])

            except KeyError:
                parallel_job_len[ number_of_hosts ] = dict()
                parallel_job_len[ number_of_hosts ] ['number'] = 1
                #parallel_job_len[ number_of_hosts ] ['walltime'] = list()
                #parallel_job_len[ number_of_hosts ] ['walltime'].append(record['Resource_List.walltime'])

        elif record['queue'] in [ 'express']:
            express_jobs += 1



print 'total_jobs :', total_jobs 
print 'serial_jobs :', serial_jobs
print 'parallel_jobs :', parallel_jobs
print 'express_jobs :', express_jobs
print 'serial_jobs_on_parallel_node :', serial_jobs_on_parallel_node

for p in parallel_job_len:
    print p, parallel_job_len[p]
