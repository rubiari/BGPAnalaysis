#!/usr/bin/env python

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/perfix'
David Arias Rubio
"""

"""
Once we have decompressed our BGP Update stream files, we read them using
the command bgpdump and save the output in files as .csv to let us work
in the future with it
"""

import os
import csv
import subprocess

def _trace_to_csv(period):

    print("Reading traces with bgpdump...")
    MRAI_BIN_DIR = "/srv/agarcia/TFM/" #path to obtain files

    if (period == 0):
        dir = MRAI_BIN_DIR + "ONE_DAY_BGP_TRACES/"
        dir2 = MRAI_BIN_DIR + "ONE_DAY_UPDATES/"
        dir3 = "/home/darias/ONE_DAY_UPDATES/"
    elif (period == 1):
        dir = MRAI_BIN_DIR + "THREE_DAY_BGP_TRACES/"
        dir2 = MRAI_BIN_DIR + "THREE_DAY_UPDATES/"
        dir3 = "/home/darias/THREE_DAY_UPDATES/"
    else:
        dir = MRAI_BIN_DIR + "BGP_TRACES/"
        dir2 = MRAI_BIN_DIR + "UPDATES/"
        dir3 = "/home/darias/UPDATES/"

    if not os.path.exists(dir2):
        os.makedirs(dir2)

    if not os.path.exists(dir3):
        os.makedirs(dir3)

    tr = []
    for file in os.listdir(dir):
        tr.append(file)


    for filename in tr:
        print(filename)
        f_name = dir + filename

        update_lines = subprocess.check_output([MRAI_BIN_DIR + '/bgpdump', '-m', f_name],
                                               stderr=subprocess.STDOUT).strip().split('\n')

        fname = dir2 + filename + ".csv"
        with open(fname, 'wb') as myfile:
            wr = csv.writer(myfile, delimiter='\n', quoting=csv.QUOTE_NONE)
            wr.writerow(update_lines)


        fname2 = dir3 + filename + ".csv"
        with open(fname2, 'wb') as myfile:
            wr = csv.writer(myfile, delimiter='\n', quoting=csv.QUOTE_NONE)
            wr.writerow(update_lines)

