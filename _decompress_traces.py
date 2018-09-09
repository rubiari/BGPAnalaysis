#!/usr/bin/env python

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
Once we have download our BGP Update stream we decompress the files to obtain the 
intern files, we saved them in zompopo./srv/agarcia/TFM/BGP_TRACES
"""

import os
import bz2
import warnings
warnings.filterwarnings("ignore")

def _decompress_traces(period):

    print('Decompressing files...')
    MRAI_BIN_DIR = "/srv/agarcia/TFM/" #path to save files

    if (period == 0):
        dir = MRAI_BIN_DIR + "ONE_DAY_BGP_TRACES_BZ2/"
        dir2 = MRAI_BIN_DIR + "ONE_DAY_BGP_TRACES/"
    elif (period == 1):
        dir = MRAI_BIN_DIR + "THREE_DAY_BGP_TRACES_BZ2/"
        dir2 = MRAI_BIN_DIR + "THREE_DAY_BGP_TRACES/"
    else:
        dir = MRAI_BIN_DIR + "BGP_TRACES_BZ2/"
        dir2 = MRAI_BIN_DIR + "BGP_TRACES/"

    if not os.path.exists(dir2):
        os.makedirs(dir2)

    f = []
    for file in os.listdir(dir):
            f.append(file)

    for filename in f:
        print("Decompressing file "+filename)
        filepath = os.path.join(dir,filename)
        newfilepath = os.path.join(dir2, filename[:-4])
        with open(newfilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
            for data in iter(lambda: file.read(100 * 1024), b''):
                new_file.write(data)
