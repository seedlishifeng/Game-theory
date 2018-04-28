import numpy as np
import sys

# limitations
#   1. no 1xn or mx1 payoff matrix
#   2. integer payoff element only

# what this script does
#   if run with 1 parameter:
#       $ python3  converter.py  payoff.csv
#   convert and write a payoff.nfg
#
#   if run without parameter
#       read 100 csv files from ./tests directory
#       convert them to and save in ./nfg directory


def convert_to_nfg(fn=None):
    # convert payoff matrix to gamebit zero sum game format
    total_files = 100
    ip_prefix = './tests/test_'
    ip_suffix = '.txt'
    op_prefix = './nfg/test_'
    op_suffix = '.nfg'

    for i in range(0, total_files):
        ip_filename = ip_prefix+str(i)+ip_suffix
        op_filename = op_prefix+str(i)+op_suffix

        if fn != None:
            ip_filename = fn
            op_filename = fn.split('.')[0]+'.nfg'

        payoff = np.genfromtxt(ip_filename, delimiter=',')
        (num_row, num_col) = payoff.shape # error here if 1xn or mx1

        # format
        f = open(op_filename, 'w')
        f.write('NFG 1 R \"converted test file\"\n')
        f.write('{ \"player1\" \"player2\" } ')
        f.write('{ '+str(num_row)+' '+str(num_col)+' }\n')
        for col in range(0, num_col):
            for row in range(0, num_row):
                if payoff[row, col]==0.0:
                    f.write('0 0')
                else:
                    f.write(str(int(payoff[row, col]))+' '+str(-int(payoff[row, col])))
                if not (col==num_col-1 and row==num_row-1):
                    f.write(' ')
        f.close()

        if fn!= None:
            return

if __name__ == '__main__':
    if len(sys.argv)==2:
        filename = sys.argv[1]
        convert_to_nfg(filename)
    else:
        convert_to_nfg()