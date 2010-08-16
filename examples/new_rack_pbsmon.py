#! /usr/bin/env python
#
# This version of pbsmon is base on the new_rack_pbsmon.py
# 
# Authors:
#   Bas van der Vlies
#   Dennis Stam
#
#      SVN Info:
#              $Id$
#              $URL$
#

"""
Usage: pbsmon [hosts]....

Specifying hostnames:
  To specify a range use the [] to indicate a range, a couple of examples:

  The first five nodes of rack 16
      - gb-r16n[1-5]

  The first five nodes and node 12 and 18 of rack 16 to 20
      - gb-r[16-20]n[1-5,12,18]

  The first five nodes de in rack 16 with padding enabled
      - gb-r[16]n[01-5]

The ranges ([]) are not only limited to numbers, letters can also be used.
"""

import sys
import re
import re
import types
from optparse import OptionParser

import pbs
from PBSQuery import PBSQuery
from PBSQuery import PBSError

# Remark: When both are True, extended view is being printed
PRINT_TABLE = True
PRINT_EXTENDED = False

# Which nodes must be skipped
EXCLUDE_NODES = [ 'login' ]

# Some global OPTS
OPT_SKIP_EMPTY_RACKS = True
OPT_SERVERNAME = None

## Begin: TABLE view opts

# A node has the following syntax gb-r10n10
#  r10 is rack name -> skip one char --> gives us rack number = 10
#  n10 is node name -> skip one char --> gives us node number = 10
# Then we have to set these variables to determine automatically the 
# number of nodes and racks 
#
NODE_EXPR = "gb-r(?P<racknr>[0-9]+)n(?P<nodenr>[0-9]+)" 

START_RACK = 1 

## End: TABLE view opts

## Begin: EXTENDED view opts

LENGTH_NODE  = 0
LENGTH_STATE = 0

EXTENDED_PATTERNS = {
    'header' : ' %-*s | %-*s | %s', 
    'row': ' %-*s | %-*s | %s',
    'line': ' %s',
    'line_char': '-',
}

## End: EXTENDED view opts

pbs_ND_single           = 'job (single)'
pbs_ND_total            = 'total'
pbs_ND_free_serial      = 'free serial'
pbs_ND_free_parallel    = 'free parallel'

PBS_STATES = {
    pbs.ND_free             : '_',
    pbs.ND_down             : 'X',
    pbs.ND_offline          : '.',
    pbs.ND_reserve          : 'R',
    pbs.ND_job_exclusive    : 'J',
    pbs.ND_job_sharing      : 'S',
    pbs.ND_busy             : '*',
    pbs.ND_state_unknown    : '?',
    pbs.ND_timeshared       : 'T',
    pbs.ND_cluster          : 'C',
    pbs_ND_single           : 'j',
    pbs_ND_free_serial      : '_',
    pbs_ND_free_parallel    : '_',
    pbs_ND_total            : ' '
}

###### Some Useful Class ##################
#
# Author: Dennis Stam
# Date  : 09-04-2009
# Desc. : This class allows you use ranges within the given arguments. Very
#         useful for specifying mutliple hosts. This class extends the
#         OptionParser class.
#
# SVN Info:
#       $Id$
#

class AdvancedParser(OptionParser):
        """
        This class extends from OptionParser, where the method check_values has been
        overrided.

        In this function a extra parsing is done on the the rest of the arguments. This
        extra parsing is the creating of multiple hostnames from a pattern/range.

        When a user specifies this argument dr-r[15,17-20]n[1-5,10] then this class
        returns 24 hosts. Besides using numbers you can also specify lower cased
        letters from a-z.

        Doctest:
        >>> parser = AdvancedParser()
        >>> parser.return_range('12-15,20')
        [12, 13, 14, 15, '20']

        >>> option, args = parser.parse_args(['dr-r7n[1-5]'])
        >>> print args
        ['dr-r7n1', 'dr-r7n2', 'dr-r7n3', 'dr-r7n4', 'dr-r7n5']
        """

        def return_range(self, string):
                """
                This method uses the given numbers and converts them to ranges. When
                ower cased letters are specified they will be converted to integer 
                ordinal of a one-character string.
                (ie. a = 97, z = 122)

                The ranges will be return as lists
                """
                parts = string.split( ',' )
                numbers_chars = list()
                equal_width_length = 0

                for part in parts:
                        part_range = part.split( '-' )
                        if len( part_range ) == 2:
                                try:
                                        if part_range[0][0] == '0' or part_range[1][0] == '0':
                                                if len( part_range[0] ) > len( part_range[1] ):
                                                        equal_width_length = len( part_range[0] )
                                                else:
                                                        equal_width_length = len( part_range[1] )

                                        numbers_chars += range( int( part_range[0] ), int( part_range[1] ) + 1 )
                                except ValueError:
                                        begin = ord( part_range[0] )
                                        end = ord( part_range[1] )
                                        tmplist = list()

                                        if begin > 96 and end < 123:
                                                tmplist = range( begin, end + 1)

                                                for letter in tmplist:
                                                        numbers_chars.append( chr( letter ) )
                        else:
                                if equal_width_length != 0 and len( part ) > equal_width_length:
                                        equal_width_length = len( part )

                                numbers_chars.append( part )

                if equal_width_length > 0:
                        tmplist = list()

                        for number_char in numbers_chars:
                                try:
                                        nnum = int( number_char )
                                        tmplist.append( '%0*d' % (equal_width_length, nnum) )
                                except ValueError:
                                        tmplist.append( number_char )
                        
                        numbers_chars = tmplist

                return numbers_chars

        def combine( self, pre, post):
                '''
                This method is used to combine a possibility of a combination
                '''
                if pre == '':
                        return post
                else:
                        return '%s %s' % (pre, post)

        def combinations( self, listin, prefix=''):
                '''
                This method creates from the given ranges all possible combinations
                '''
                outlist = list()

                if len( listin ) > 1:
                        for item in listin[0]:
                                outlist += self.combinations( listin[1:], self.combine( prefix, str( item ) ) )
                else:
                        for item in listin[0]:
                                outlist.append( tuple( self.combine( prefix, str( item ) ).split( ' ') ) )

                return outlist

        def args_parser(self, args):
                '''
                This method checks all given extra arguments for the given ranges between the
                [ and ]
                '''
                findregex = re.compile( r'\[([0-9a-z\-,]+)\]', re.VERBOSE )
                nodenames = list()

                for arg in args:
                        found = findregex.findall( arg )
                        ranges = list()

                        if found:
                                pattern = findregex.sub( '%s', arg )

                                for part in found:
                                        ranges.append( self.return_range( part ) )

                                combs = self.combinations( ranges )

                                for comb in combs:
                                        # Here the %s in the pattern are
                                        # replaced by the correct value
                                        nodenames.append( pattern % comb )
                        else:
                                nodenames.append( arg )

                return nodenames

        def check_values(self, values, args):
                '''
                Here we override the default method in OptionParser to
                enable our extra parsing on the given Arguments
                '''
                return values, self.args_parser( args )

#### End Useful Class #####

def sanitize_jobs( jobs ):

    ljobs = list()

    for job in jobs:
        ljobs.extend( re.findall( r'[0-9]+\/([0-9]+)\.*.', job ) )

    return list( set( ljobs ) )

def parse_nodename( nodename ):
    global NODE_EXPR

    parts = re.search( r'%s' % NODE_EXPR, nodename, re.VERBOSE )

    try:
        racknr = parts.group( 'racknr' )
    except Exception:
		racknr = 0

    try:
        nodenr = parts.group( 'nodenr' )
    except Exception:
        nodenr = 0

    return int( racknr ), int( nodenr )

def get_nodes( racknode=False, hosts=None ):
    global LENGTH_NODE
    global LENGTH_STATE
    global OPT_SERVERNAME

    nodes_dict = dict()

    try:
        if not OPT_SERVERNAME:
            p = PBSQuery()
        else:
            p = PBSQuery( OPT_SERVERNAME )
    except PBSError, reason:
        print 'Error: %s' % reason
        sys.exit( -1 )

    p.new_data_structure()

    attr = [ 'state', 'jobs', 'properties' ]

    try:
        nodes = p.getnodes( attr )
    except PBSError, reason:
        print 'Error: %s' % reason
        sys.exit( -1 )

    number_of_racks = 0
    nodes_per_rack = 0
    hosts_list = list()
    
    for node, attr in nodes.items():
        if node in EXCLUDE_NODES:
            continue

        if hosts and node not in hosts:
            continue

        if pbs.ND_down in attr.state:
            state = pbs.ND_down
        else:
            state = attr.state[ 0 ]

        state_char = PBS_STATES[ state ]

        if attr.is_free() and attr.has_job():
            state = pbs.ND_busy 
            state_char = PBS_STATES[ pbs_ND_single ]

        if not nodes_dict.has_key( node ):
            nodes_dict[ node ] = dict()

        # Setting the longest lenght
        if len( node ) > LENGTH_NODE:
            LENGTH_NODE = len( node )

        if len( state ) > LENGTH_STATE:
            LENGTH_STATE = len( state )

        if racknode:
            racknr, nodenr = parse_nodename( node )

            if racknr > number_of_racks:
                number_of_racks = racknr

            if nodenr > nodes_per_rack:
                nodes_per_rack = nodenr
            
            if not nodes_dict.has_key( racknr ):
                nodes_dict[ racknr ] = dict()

            if not nodes_dict[ racknr ].has_key( nodenr ):
                nodes_dict[ racknr ][ nodenr ] = dict()

            nodes_dict[ racknr ][ nodenr ][ 'state_char' ] = state_char
            nodes_dict[ racknr ][ nodenr ][ 'state' ] = state
        
            if attr.has_key( 'jobs' ):
                nodes_dict[ racknr ][ nodenr ][ 'jobs' ] = sanitize_jobs( attr.jobs )
            else:
                nodes_dict[ racknr ][ nodenr ][ 'jobs' ] = []
        else:
            hosts_list.append( node )
            nodes_dict[ node ][ 'state_char' ] = state_char
            nodes_dict[ node ][ 'state' ] = state
        
            if attr.has_key( 'jobs' ):
                nodes_dict[ node ][ 'jobs' ] = sanitize_jobs( attr.jobs )
            else:
                nodes_dict[ node ][ 'jobs' ] = []

    if not racknode:
        return nodes_dict, hosts_list

    return nodes_dict, number_of_racks, nodes_per_rack

def _generate_index( str ):
    index = []

    def _append( fragment, alist=index ):
        if fragment.isdigit():
            fragment = int( fragment )
        alist.append( fragment )

    prev_isdigit = str[0].isdigit()
    current_fragment = ''

    for char in str:
        curr_isdigit = char.isdigit()

        if curr_isdigit == prev_isdigit:
            current_fragment += char
        else:
            _append( current_fragment )
            current_fragment = char
            prev_isdigit = curr_isdigit

    _append( current_fragment )

    return tuple( index )

def real_sort( inlist ):
    indices = map(_generate_index, inlist )
    decorated = zip( indices, inlist )
    decorated.sort()

    return [ item for index, item in decorated ]

def print_table():
    global START_RACK 
    global OPT_SKIP_EMPTY_RACKS

    nodes, racknr, nodenr = get_nodes( True )

    ## Code herebelow has been taken from the new_rack_pbsmon.py
    save_column = None
    
    print    
    print '  ',
    for rack in xrange( START_RACK, racknr + 1 ):
        
        if not ( rack % 10 ):
            char = '%d' % ( rack / 10 )
            save_column = char
        else:
            char = ' '

        if OPT_SKIP_EMPTY_RACKS:
            if nodes.has_key( rack ):
                if save_column:
                    char = save_column
                    save_column = None
                print char,
        else:
            print char,
    print    

    print '  ',
    for rack in xrange( START_RACK, racknr + 1 ):
        
        char = rack % 10
        if OPT_SKIP_EMPTY_RACKS:
            if nodes.has_key( rack ):
                print char,
        else:
            print char,
    print

    for node in xrange( 1, nodenr + 1 ):
        print '%2d' % node,

        for rack in xrange( START_RACK, racknr + 1 ):
            if OPT_SKIP_EMPTY_RACKS:
                if not nodes.has_key( rack ):
                    continue
            try:
                print nodes[ rack ][ node ][ 'state_char' ],
            except KeyError:
                print ' ',
        print
    print

def print_table_summary():
    global PBS_STATES
    global OPT_SERVERNAME

    try:
        if not OPT_SERVERNAME:
            p = PBSQuery()
        else:
            p = PBSQuery( OPT_SERVERNAME )
    except PBSError, reason:
        print 'error: %s' % reason
        sys.exit(-1)

    # get the state of the nodes
    attr = [ 'state', 'jobs', 'properties' ]
    try:
        nodes = p.getnodes(attr)
    except PBSError, reason:
        print 'error: %s' % reason
        sys.exit(-1)

    node_dict = {}

    count_states = {}
    for key in PBS_STATES.keys():
        count_states[key] = 0

    for nodename, node in nodes.items():

        # Skip login nodes in status display
        #
        if not nodename.find('login'):
            continue

        state = node['state'][ 0 ]

        state_char = PBS_STATES[state]
        count_states[state] += 1
        count_states[pbs_ND_total] += 1

        if node.is_free():                          # can happen for single CPU jobs
            if node.has_job():
#               print 'TD: %s' % nodename, node
                state_char = PBS_STATES[pbs_ND_single]
                count_states[pbs.ND_free] -=  1
                count_states[pbs_ND_single] += 1
            else:
                if  'infiniband' in node['properties']:
                    count_states[pbs_ND_free_parallel] +=  1 
                elif  'ifiniband' in node['properties']:
                    count_states[pbs_ND_free_serial] +=  1 
                #else:
                #   count_states[pbs_ND_free_serial] +=  1 
                
#       print 'TD: %s %s' % (nodename, state_char)
        dummy = nodename.split('-')
        if len( dummy ) > 1:
            node_dict[dummy[1]] = state_char
        else:
            node_dict[dummy[0]] = state_char

    legend = PBS_STATES.keys()
    legend.sort()

    n = 0
    for state in legend:
        print '  %s  %-13s : %-5d' % (PBS_STATES[state], state, count_states[state]),

        n = n + 1
        if not (n & 1):
            print

def print_extended( hosts=None ):
    global LENGTH_NODE
    global LENGTH_STATE 
    global EXTENDED_PATTERNS
    
    nodes, ihosts = get_nodes( hosts=hosts )
    row_header = EXTENDED_PATTERNS[ 'header' ] % ( ( LENGTH_NODE + 2 ), 'Node', ( LENGTH_STATE + 2 ), 'State', 'Jobs' )
    LENGTH_ROW = len( row_header )

    rows_str = list()
    ihosts = real_sort( ihosts )

    for node in ihosts:
        attr = nodes[ node ]
        row_str = EXTENDED_PATTERNS[ 'row' ] % ( ( LENGTH_NODE + 2 ), node, ( LENGTH_STATE + 2 ), attr[ 'state' ], ','.join( attr[ 'jobs' ] ) )

        if len( row_str ) > LENGTH_ROW:
            LENGTH_ROW = len( row_str )

        rows_str.append( row_str )

    print
    print row_header
    print EXTENDED_PATTERNS[ 'line' ] % ( EXTENDED_PATTERNS[ 'line_char' ] * LENGTH_ROW )
    print '\n'.join( rows_str )
    print

if __name__ == '__main__':
    
    parser = AdvancedParser(usage=__doc__)

    parser.add_option( "-t", "--table", dest="table", action="store_true", help="Show an table" )
    parser.add_option( "-l", "--list", dest="extended", action="store_true", help="Show node rows with state and jobinfo" )
    parser.add_option( "-s", "--summary", dest="summary", action="store_true", help="Display a short summary" )
    parser.add_option( "-w", "--wide", dest="wide", action="store_true", help="Wide display for node status ( only when -t is used )" )
    parser.add_option( "-S", "--servername", dest="servername", help="Change the default servername" )

    parser.set_defaults( table=PRINT_TABLE )
    parser.set_defaults( summary=False )
    parser.set_defaults( extended=PRINT_EXTENDED )
    parser.set_defaults( servername=None )

    ( options, args ) = parser.parse_args()

    if options.servername:
        OPT_SERVERNAME = options.servername

    if options.wide:
        OPT_SKIP_EMPTY_RACKS = False

    if args:
        options.extended = True

    if options.extended and PRINT_TABLE:
        options.table = False

    if options.table and PRINT_EXTENDED:
        options.extended = False

    if options.extended:
        print_extended( args ) 
    elif options.table:
        print_table()
    else:
        print 'Something is wrong, bye!'
        sys.exit( -1 )

    if options.summary:
        print_table_summary()
