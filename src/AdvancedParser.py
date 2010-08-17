#
# Author: Dennis Stam
# Date  : 09-04-2009
# Desc. : This class allows you use ranges within the given arguments. Very
#         useful for specifying mutliple hosts. This class extends the
#         OptionParser class.
#
# SVN Info:
#       $Id: AdvancedParser.py 3667 2009-04-15 12:02:04Z dennis $
#       $URL: https://subtrac.sara.nl/hpcv/svn/beowulf/trunk/sara_python_modules/AdvancedParser.py $
#
from optparse import OptionParser
import re
import types

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

if __name__ == "__main__":
        import doctest
        print 'Starting doctest'
        doctest.testmod()
