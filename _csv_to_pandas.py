#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
We read the different .csv for every year dataset and save this
data in panda dataframes
"""

import os
import datetime as datetime
import pandas as pd
import warnings
from os.path import expanduser
warnings.filterwarnings("ignore")

def _csv_to_pandas():

    dir =  expanduser("~") + '/THREE_DAY_UPDATES/'

    updates1 = []
    updates2 = []

    _years = []
    for file in os.listdir(dir):
        name = file.split(".")
        year = name[1][0:4]
        if year not in _years:
            _years.append(year)

    _years.sort()

    for file in os.listdir(dir):
        if file.endswith(".csv") and str(_years[0]) in file:
            updates1.append(file)
        elif file.endswith(".csv") and str(_years[1]) in file:
            updates2.append(file)

    updates1.sort()
    updates2.sort()

    colnames = ['bgp', 'ts', 'type', 'srcip', 'srcasn', 'CIDR', 'aspath', 'origin', 'nexthop', 'seq', 'med', 'community']

    print("Reading traces of " + str(_years[0]) +"...")
    list_1 = []
    for file in updates1:
        fname = dir + file
        df = pd.read_csv(fname, names=colnames, delimiter="|",error_bad_lines=False, encoding="ISO-8859-1")
        df = df.drop(df.index[0])  #The first row is info that we dont need
        list_1.append(df)

    frame1 = pd.concat(list_1)

    print("Reading traces of " + str(_years[1]) + "...")
    list_2 = []
    for file in updates2:
        fname = dir + file
        df = pd.read_csv(fname, names=colnames, delimiter="|", error_bad_lines=False, encoding="ISO-8859-1")
        df = df.drop(df.index[0])  #We drop the first row of data
        list_2.append(df)

    frame2 = pd.concat(list_2)

    print('frame1: ' + str(len(frame1)) + ', frame2: ' + str(len(frame2)))

    _FRAMES = [frame1,frame2]

    return _FRAMES
