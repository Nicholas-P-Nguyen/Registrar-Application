#!/usr/bin/env python

#-----------------------------------------------------------------------
# testregoverviews.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import os
import sys

#-----------------------------------------------------------------------

MAX_LINE_LENGTH = 72
UNDERLINE = '-' * MAX_LINE_LENGTH

#-----------------------------------------------------------------------

def print_flush(message):
    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def exec_command(program, args):

    print_flush(UNDERLINE)
    command = 'python ' + program + ' ' + args
    print_flush(command)
    exit_status = os.system(command)
    if os.name == 'nt':  # Running on MS Windows?
        print_flush('Exit status = ' + str(exit_status))
    else:
        print_flush('Exit status = ' + str(os.WEXITSTATUS(exit_status)))

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 2:
        print('usage: ' + sys.argv[0] + ' regprogram', file=sys.stderr)
        sys.exit(1)

    program = sys.argv[1]
    exec_command(program, '')

    # Testing subsets of 4
    exec_command(program, '-d COS -a qr -n 2 -t intro')

    # Testing subsets of 3
    exec_command(program, '-d COS -n 2 -a qr')
    exec_command(program, '-d COS -n 2 -t intro')
    exec_command(program, '-d COS -a qr -t intro')
    exec_command(program, '-n 2 -a qr -t intro')

    # Testing subsets of 2
    exec_command(program, '-d COS -n 2')
    exec_command(program, '-d COS -a qr')
    exec_command(program, '-d COS -t intro')
    exec_command(program, '-n 2 -a qr')
    exec_command(program, '-n 2 -t intro')
    exec_command(program, '-a qr -t intro')

    # Testing subsets of 1
    exec_command(program, '-d COS')
    exec_command(program, '-a qr')
    exec_command(program, '-t intro')
    exec_command(program, '-n 2')

    # Testing wildcard characters
    exec_command(program, '-t c%S')
    exec_command(program, '-t C_S')



#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
