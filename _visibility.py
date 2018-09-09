#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
VISIBILITY: FRACTION OF TIME OF A PREFIX IN THE ROUTING TABLE
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

import os
import bz2
import sys
import idna
import subprocess
import warnings
from matplotlib import pyplot as plt
from os.path import expanduser
import datetime as datetime
import requests
from robobrowser import RoboBrowser

warnings.filterwarnings("ignore")



def _ts_to_date(tstamp):
    tdate = datetime.datetime.fromtimestamp(tstamp)
    return tdate


#############################################################
def _visibility():
    print('Visibility analysis...')
    path = expanduser("~") + '/tfmcode/clustering/2015/2015_3/'
    path_vis = expanduser("~") + '/tfmcode/visibility/2015_3/'
    path_save = expanduser("~") + '/figures/'

    if not os.path.exists(path_vis):
        os.makedirs(path_vis)

    f_1 = path + 'df_2015_3.csv'
    df = pd.read_csv(f_1, sep="|", names=['prefix', 'time', 'vp', 'path', 'origin', 'community', 'cluster'], skiprows=1)

    # FIRST WE DOWNLOAD THE RIB FILE FOR THE MOMENT OF START
    t_rib = df['time'][0]
    date_rib = _ts_to_date(t_rib)

    f_rib = _download_rib(path_vis, date_rib)

    #f_rib = path_vis + "rib.20151201.0000.csv"

    colnames = ['table', 'ts', 'type', 'srcip', 'srcasn', 'CIDR', 'aspath', 'origin', 'nexthop', 'seq', 'med',
                'community', 'a', 'b', 'c']
    df_rib = pd.read_csv(f_rib, sep="|", names=colnames, skiprows=1, error_bad_lines=False, encoding="ISO-8859-1")
    df_rib.reset_index(drop=True, inplace=True)
    df_rib.rename(columns={'CIDR': 'prefix', 'ts': 'time', 'srcip': 'vp', 'aspath': 'path'}, inplace=True)
    df_rib = df_rib[['prefix', 'time', 'vp', 'path', 'origin', 'community']]
    t_rib = df_rib['time'][0]
    df_rib['time'] = t_rib

    """
    vps = []
    for ix, row in df.iterrows():
        if row.vp not in vps:
            vps.append(row.vp)
    print(vps)
    """

    # We skip the step above by creating already the list of vps
    vps = ['202.249.2.169', '2001:200:0:fe00::9c4:11', '202.249.2.86', '2001:200:0:fe00::9d4:0', '202.249.2.83']

    # We remove those traces from RIB from the VPs that gather information about less than 400000 prefixes
    final_vps = []
    for vp in vps:
        df_v = df_rib.loc[((df_rib['vp'] == vp))]
        if (len(df_v) < 400000):
            df_rib = df_rib[df_rib['vp'] != vp]
            df = df[df['vp'] != vp]
        else:
            final_vps.append(vp)

    # Lifetime of every prefix
    for i_vp in range(0, len(final_vps)):
        _vp = final_vps[i_vp]

        df_v1 = df_rib.loc[(df_rib['vp'] == _vp)]
        df_v1.reset_index(drop=True, inplace=True)

        df_v2 = df.loc[(df['vp'] == _vp)]
        df_v2.reset_index(drop=True, inplace=True)

        _paths = {}
        last_t = 0

        # Save all the information about RIB prefixes
        for ix, row in df_v1.iterrows():
            p_i = row.prefix
            last_t = row.time

            if p_i not in _paths.keys():
                _paths.setdefault(p_i, [])
                _paths[p_i].append(list())
                _paths[p_i][0].append(last_t)
                _paths[p_i][0].append(0)
                _paths[p_i][0].append('IN')


        for ix, row in df_v2.iterrows():
            p_i = row.prefix
            as_i = row.path
            last_t = row.time
            if (isinstance(as_i, str) == True):
                if p_i not in _paths.keys():
                    _paths.setdefault(p_i, [])
                    _paths[p_i].append(list())
                    _paths[p_i][0].append(last_t)
                    _paths[p_i][0].append(0)
                    _paths[p_i][0].append('IN')

                else:
                    if (_paths[p_i][0][2] == "OUT"):
                        _paths[p_i][0][0] = last_t
                        _paths[p_i][0][2] = "IN"

                    else:
                        continue
            else:
                # The AS is a WITHDRAWAL (is empty)
                if p_i in _paths.keys():
                    start_t = _paths[p_i][0][0]
                    usage_t = last_t - start_t
                    _paths[p_i][0][0] = last_t
                    _paths[p_i][0][1] += usage_t
                    _paths[p_i][0][2] = "OUT"

                else:
                    # This prefix was announced before all our data
                    continue


        print(len(_paths))

        for key in _paths.keys():
            if (_paths[key][0][2] == 'IN'):
                start_t = _paths[key][0][0]
                usage_t = last_t - start_t
                _paths[key][0][1] += usage_t

        f_path = path_vis + 'prefix_usage_time_' + str(i_vp) + '_3.csv'

        with open(f_path, 'w') as f:
            for key in _paths.keys():
                f.writelines("%s|%d\n" % (key, _paths[key][0][1]))
            f.close()

        del _paths

        f_path = path_vis + 'prefix_usage_time_' + str(i_vp) + '_3.csv'
        df_path = pd.read_csv(f_path, sep="|", names=['prefix', 'usage_time'])
        df_path['usage_time'] = df_path['usage_time'].astype(int)
        df_path.sort_values(by=['usage_time'], ascending=False, inplace=True)
        df_path.reset_index(drop=True, inplace=True)
        print(df_path)

        ID = np.linspace(1, (len(df_path['usage_time'])), (len(df_path['usage_time'])))

        plt.plot(ID, df_path['usage_time'], 'b-')
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        plt.yscale('log')
        plt.grid(True)
        plt.show()
        plt.xlabel('Prefix ID')
        plt.ylabel('Path Usage Time (s)')

        plt.savefig(path_save + 'Visibility_' + str(i_vp) + '3.png')
        print('Saved plot image\n')
        plt.close()


    #Representation of all prefixes together
    
    path_files = []
    for file in os.listdir(path_vis):
        if file.endswith(".csv") and ('prefix_usage_time_' in file):
            path_files.append(file)

    list_1 = []
    for file in path_files:
        f_path = path_vis + file
        df = pd.read_csv(f_path, sep="|", names=['prefix', 'usage_time'])

        list_1.append(df)

    df1 = list_1[0]
    df2 = list_1[1]
    df1.sort_values(by='usage_time', ascending=False, inplace=True)
    df2.sort_values(by='usage_time', ascending=False, inplace=True)

    ID1 = np.linspace(1, (len(df1['usage_time'])), (len(df1['usage_time'])))
    ID2 = np.linspace(1, (len(df2['usage_time'])), (len(df2['usage_time'])))

    plt.plot(ID1, df1['usage_time'], 'r-', label = final_vps[0])
    plt.plot(ID2, df2['usage_time'], 'b-', label = final_vps[1])
    plt.legend(loc='best')
    plt.yscale('log')
    # plt.xscale('log')
    plt.grid(True)
    plt.show()
    plt.xlabel('Prefix ID')
    plt.ylabel('Path Usage Time (s)')

    plt.savefig(path_save + 'Visibility_all_3day.png')
    print('Saved plot image\n')
    plt.close()

