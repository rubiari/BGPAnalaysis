#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
VISIBILITY: FRACTION OF EVERY UNIQUE PATH
"""

import os
import matplotlib.ticker as ticker
import math
import numpy as np
import pandas as pd
import warnings
import matplotlib
import ipaddress
import csv

matplotlib.use('Agg')

from matplotlib import pyplot as plt
from os.path import expanduser

warnings.filterwarnings("ignore")


def _visibility_path():
    print('Visibility Path analysis...')
    path_clus = expanduser("~") + '/tfmcode/clustering/2015/2015_3/'
    path_vis = expanduser("~") + '/tfmcode/visibility/2015_3/'
    path_save = expanduser("~") + '/figures/'
    f_1 = path_clus + 'df_2015_3.csv'

    f_rib = path_vis + "rib.20151201.0000.csv"
    colnames = ['table', 'ts', 'type', 'srcip', 'srcasn', 'CIDR', 'aspath', 'origin', 'nexthop', 'seq', 'med',
                'community', 'a', 'b', 'c']
    df_rib = pd.read_csv(f_rib, sep="|", names=colnames, skiprows=1, error_bad_lines=False, encoding="ISO-8859-1")
    df_rib.reset_index(drop=True, inplace=True)

    df_rib.rename(columns={'CIDR': 'prefix', 'ts': 'time', 'srcip': 'vp', 'aspath': 'path'}, inplace=True)
    df_rib = df_rib[['prefix', 'time', 'vp', 'path', 'origin', 'community']]

    df = pd.read_csv(f_1, sep="|", names=['prefix', 'time', 'vp', 'path', 'origin', 'community', 'cluster'], skiprows=1)
    df['community'] = df['community'].astype('str')
    print(df)


    vps = ['202.249.2.169', '2001:200:0:fe00::9c4:11', '202.249.2.86', '2001:200:0:fe00::9d4:0', '202.249.2.83']
    # Elimination of prefixes (if the data for the vp is less than 400000 prefixes)
    final_vps = []
    for vp in vps:
        # print(vp)
        df_v = df_rib.loc[((df_rib['vp'] == vp))]
        if (len(df_v) < 400000):
            df_rib = df_rib[df_rib['vp'] != vp]
            df = df[df['vp'] != vp]
        else:
            final_vps.append(vp)


    for i_vp in range(0, len(final_vps)):

        f_rib = path_clus + 'rib_final_' + str(i_vp) + '_2015.csv'
        df_rib = pd.read_csv(f_rib, sep="|", names=['prefix', 'time', 'path', 'origin', 'community', 'traffic', 'per_traffic'], skiprows = 1)
        _vp = final_vps[i_vp]


        df_v2 = df.loc[(df['vp'] == _vp)]
        df_v2.reset_index(drop=True, inplace=True)
        print(df_v2)

        _paths = {}
        last_t = 0

        # Save all the information about RIB prefixes
        for ix, row in df_rib.iterrows():
            p_i = row.prefix
            as_i = row.path
            last_t = row.time

            if p_i not in _paths.keys():
                _paths.setdefault(p_i, [])
                _paths[p_i].append(list())
                _paths[p_i][0].append(as_i)
                _paths[p_i][0].append(last_t)
                _paths[p_i][0].append(0)

                as_len = as_i.split(" ")
                _paths[p_i][0].append(int(len(as_len)))

                _paths[p_i][0].append(row.origin)
                _paths[p_i][0].append(row.community)
                _paths[p_i][0].append('IN')

        for ix, row in df_v2.iterrows():
            p_i = row.prefix
            as_i = row.path
            last_t = row.time

            if (isinstance(as_i, str) == True):
                if p_i not in _paths.keys():

                    _paths.setdefault(p_i, [])
                    _paths[p_i].append(list())
                    _paths[p_i][0].append(as_i)
                    _paths[p_i][0].append(last_t)
                    _paths[p_i][0].append(0)

                    as_len = as_i.split(" ")
                    _paths[p_i][0].append(int(len(as_len)))

                    _paths[p_i][0].append(row.origin)
                    _paths[p_i][0].append(row.community)
                    _paths[p_i][0].append('IN')

                else:

                    # If the AS PATH is not in the list...
                    if ((any(as_i == _paths[p_i][id][0] for id in range(0, len(_paths[p_i])))) == False):
                        # Calculation of the Usage Time
                        start_t = _paths[p_i][0][1]
                        usage_t = last_t - start_t
                        _paths[p_i][0][2] += usage_t
                        _paths[p_i][0][6] = 'OUT'

                        # We introduce the new AS PATHA in
                        # the new position

                        _paths[p_i].insert(0, list())
                        _paths[p_i][0].append(as_i)
                        _paths[p_i][0].append(last_t)
                        _paths[p_i][0].append(0)

                        as_len = as_i.split(" ")
                        _paths[p_i][0].append(int(len(as_len)))

                        _paths[p_i][0].append(row.origin)
                        _paths[p_i][0].append(row.community)
                        _paths[p_i][0].append('IN')

                    else:
                        n = 0
                        for id in range(0, len(_paths[p_i])):
                            if (_paths[p_i][id][0] == as_i):
                                n = id
                                break

                        start_t = _paths[p_i][0][1]
                        usage_t = last_t - start_t
                        _paths[p_i][0][2] += usage_t
                        _paths[p_i][0][6] = "OUT"

                        usage_t = _paths[p_i][n][2]
                        del _paths[p_i][n]

                        _paths[p_i].insert(0, list())
                        _paths[p_i][0].append(as_i)
                        _paths[p_i][0].append(last_t)
                        _paths[p_i][0].append(usage_t)

                        as_len = as_i.split(" ")
                        _paths[p_i][0].append(int(len(as_len)))

                        _paths[p_i][0].append(row.origin)
                        _paths[p_i][0].append(row.community)
                        _paths[p_i][0].append("IN")

            else:
                # The AS is a WITHDRAWAL (is empty)
                if p_i in _paths.keys():
                    start_t = _paths[p_i][0][1]
                    usage_t = last_t - start_t
                    _paths[p_i][0][2] += usage_t
                    _paths[p_i][0][6] = "OUT"

                else:
                    # This prefix was announced before all the gathered data
                    continue

        for key in _paths.keys():
            if (_paths[key][0][6] == 'IN'):
                start_t = _paths[key][0][1]
                usage_t = last_t - start_t
                _paths[key][0][2] += usage_t

        f_path = path_vis + 'path_usage_time_' + str(i_vp) + '_3.csv'
        with open(f_path, 'w') as f:
            for key in _paths.keys():
                for id in range(0, len(_paths[key])):
                    f.writelines("%s|%s|%d|%d|%s|%s\n" % (
                    key, _paths[key][id][0], _paths[key][id][2], _paths[key][id][3], _paths[key][id][4],
                    _paths[key][id][5]))
            f.close()
            
        del _paths

    for i_vp in range(0, len(final_vps)):
        f_path = path_vis + 'path_usage_time_' + str(i_vp) + '_3.csv'
        df_path = pd.read_csv(f_path, sep="|",
                              names=['prefix', 'as_path', 'usage_time', 'as_path_length', 'origin', 'community'])

        df_path['usage_time'] = df_path['usage_time'].astype(int)
        df_path.sort_values(by=['usage_time'], ascending=False, inplace=True)

        df_path = df_path.loc[(df_path['usage_time'] < 259201)]
        print(df_path)

        ID = np.linspace(1, (len(df_path['usage_time'])), (len(df_path['usage_time'])))

        plt.plot(ID, df_path['usage_time'], 'r-')
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        plt.yscale('log')
        plt.grid(True)
        plt.show()
        plt.xlabel('Path ID')
        plt.ylabel('Path Usage Time (s)')

        plt.savefig(path_save + 'Path_Visibility_' + str(i_vp) + '3.png')
        print('Saved plot image\n')
        plt.close()


