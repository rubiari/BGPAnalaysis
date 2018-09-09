#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
CLUSTERING UPDATES INTO EVENTS BY TIME THRESHOLD
"""

import os
import datetime as datetime
import pandas as pd
import warnings
import matplotlib
import ipaddress
import csv
import matplotlib.dates as md
import math
import numpy as np
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from os.path import expanduser

warnings.filterwarnings("ignore")


def _clustering_updates(frame):

    print('TEST CLUSTERING...\n')
    _T = 241  # threshold time for clustering (4 minutes)
    df = pd.DataFrame(frame)
    df.rename(columns={'CIDR': 'prefix', 'ts': 'time', 'srcip': 'vp', 'aspath': 'path'}, inplace=True)

    df_test = df.copy()
    df['cluster'] = 0

    # Different vantage points in our dataset
    _vps = ['202.249.2.169', '2001:200:0:fe00::9c4:11', '202.249.2.86', '2001:200:0:fe00::9d4:0', '202.249.2.83']

    c_num = 0  # number of the cluster
    prefix = {}  # prefix per number of events/prefix
    n_updates = {}  # prefix per number of updates/prefix
    prefix_sum = 0  # number of total prefixes

    for ix_i, row_i in df_test.iterrows():
        p_i = row_i.prefix

        #if(ix_i == 100):
        #    break

        if p_i not in prefix.keys():
            c_num += 1
            prefix_sum += 1

            prefix.setdefault(p_i, 0)
            n_updates.setdefault(p_i, 0)
            df.set_value(ix_i, 'cluster', c_num)

            df_t = df_test.loc[((df_test['prefix'] == p_i))]
            prefix[p_i] = 1
            n_updates[p_i] = len(df_t)

            for vp in _vps:
                df_t_2 = df_t.loc[((df_t['vp'] == vp))]

                if (df_t_2.empty == False):
                    t_i = df_t_2['time'].iloc[0]

                    for ix_j, row_j in df_t_2.iterrows():
                        t_j = row_j['time']  # Timestamp of update j
                        diff = abs(t_j - t_i)

                        if (diff < _T):
                            df.set_value(ix_j, 'cluster', c_num)
                            t_i = t_j
                        else:
                            # Difference of time > Threhold
                            # We assume that a new event begins
                            prefix[p_i] += 1  # Increment number of event/prefix
                            c_num += 1  # Increment number of cluster
                            df.set_value(ix_j, 'cluster', c_num)
                            t_i = t_j

            print(len(prefix))

    print(df)

    #Write the clustering results in several csv files
    path = expanduser("~") + '/tfmcode/clustering/2015/2015_3/'
    #time_name = str(df['time'].iloc[0])
    time_name = "2015"
    filename = "df_" + time_name + '_3.csv'
    df.to_csv(path + filename, sep='|', encoding='utf-8')

    print('prefix_sum: ', prefix_sum)

    file_dict1 = 'events_' + time_name + '_3.csv'
    with open(path + file_dict1, 'w') as f:
        for key in prefix.keys():
            f.write("%s,%d\n" % (key, prefix[key]))

    file_dict2 = 'updates_' + time_name + '_3.csv'
    with open(path + file_dict2, 'w') as f:
        for key in n_updates.keys():
            f.write("%s,%d\n" % (key, n_updates[key]))

