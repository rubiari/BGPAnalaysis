#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
ANALYSIS OF TRAFFIC POPULARITY 
"""

import os
import pandas as pd
import warnings
import matplotlib
import ipaddress
import csv
import matplotlib.ticker as ticker
import math
import numpy as np
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from os.path import expanduser

warnings.filterwarnings("ignore")


def _traffic_popularity():

    path_traffic = "/srv/agarcia/TFM/WIDE_TRAFFIC/"
    path_vis = expanduser("~") + '/tfmcode/visibility/2014_3/'
    path_clus = expanduser("~") + '/tfmcode/clustering/2014/2014_3/'
    path_save = expanduser("~") + '/figures/'
    f_1 = path_traffic + 'day_bytes_per_prefix_2014.csv'
    f_2 = path_traffic + 'day_packets_per_prefix_2014.csv'

    vps = ['202.249.2.169', '2001:200:0:fe00::9c4:11', '202.249.2.86', '2001:200:0:fe00::9d4:0', '202.249.2.83']

    print('Traffic Popularity analysis...')

    print('Getting RIB file...')
    f_rib = path_vis + "rib.20141209.0000.csv"
    colnames = ['table', 'ts', 'type', 'srcip', 'srcasn', 'CIDR', 'aspath', 'origin', 'nexthop', 'seq', 'med',
                'community', 'a', 'b', 'c']
    df_rib = pd.read_csv(f_rib, sep="|", names=colnames, skiprows=1, error_bad_lines=False, encoding="ISO-8859-1")

    df_rib.rename(columns={'CIDR': 'prefix', 'ts': 'time', 'srcip': 'vp', 'aspath': 'path'}, inplace=True)
    df_rib = df_rib[['prefix', 'time', 'vp', 'path', 'origin', 'community']]
    df_rib['time'] = df_rib['time'].astype(int)
    t_rib = df_rib['time'][0]
    df_rib['time'] = t_rib

    final_vps = []
    for vp in vps:
        df_v = df_rib.loc[((df_rib['vp'] == vp))]
        print(len(df_v))
        if (len(df_v) < 400000):
            df_rib = df_rib[df_rib['vp'] != vp]
        else:
            final_vps.append(vp)
    df_rib.reset_index(drop=True, inplace=True)

    print('Getting Traffic file...')
    df_bytes = pd.read_csv(f_1, sep = ";", names = ['prefix', 'bytes', 'percentage'], skiprows = 1)
    print('LEN DF BYTES: '+ str(len(df_bytes)))

    total_bytes = 0
    for ix, row in df_bytes.iterrows():
        total_bytes += int(row.bytes)

    df_bytes['percentage'] = df_bytes.apply(lambda row: (int(row.bytes)/(total_bytes))*100, axis=1)
    df_bytes.sort_values(by = 'percentage', ascending = False, inplace = True)
    df_bytes['bytes'] = df_bytes['bytes'].astype(int)
    df_bytes.reset_index(drop=True, inplace=True)
    ID = np.linspace(1, (len(df_bytes)), (len(df_bytes)))

    plt.plot(ID, df_bytes['percentage'], 'g-')
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter("{x}"))
    plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter("{x}"))
    plt.grid(True)
    #plt.yscale('log')
    plt.xscale('log')
    plt.show()
    plt.xlabel('ID Prefix')
    plt.ylabel('Traffic Volume (%)')

    plt.savefig(path_save + 'RouteViews_Prefix_vs_TrafficVolume_2015.png')
    print('Saved plot image\n')
    plt.close()

    ############################################
    f_eve = path_clus + 'events_2014_3.csv'

    df_eve = pd.read_csv(f_eve, sep=",", names=['prefix', 'n_events', 'per_events'], skiprows = 1)
    df_eve.reset_index(drop=True, inplace=True)

    _events = {}
    for ix_i, row in df_eve.iterrows():
        p_i = row.prefix
        n_i = row.n_events
        per_i = row.per_events

        if p_i not in _events.keys():
            _events.setdefault(p_i, [])
            _events[p_i].append(n_i)
            _events[p_i].append(per_i)

    #####################################
    _traffic = {}
    for ix_i, row in df_bytes.iterrows():
        p_i = row.prefix
        tr_i = row.bytes
        per_i = row.percentage

        if p_i not in _traffic.keys():
            _traffic.setdefault(p_i, [])
            _traffic[p_i].append(tr_i)
            _traffic[p_i].append(per_i)

            if p_i in _events.keys():
                n_j = _events[p_i][0]
                per_j = _events[p_i][1]
                _traffic[p_i].append(n_j)
                _traffic[p_i].append(per_j)
            else:
                _traffic[p_i].append(0)
                _traffic[p_i].append(0)

    ############################################
    visi_files = []
    for file in os.listdir(path_vis):
        if file.endswith(".csv") and ('prefix_usage_time_' in file):
            visi_files.append(file)

    list_1 = []
    for file in visi_files:
        f_path = path_vis + file
        df = pd.read_csv(f_path, sep="|", names=['prefix', 'usage_time'])
        list_1.append(df)

    df_visi = pd.concat(list_1)
    df_visi['usage_time'] =  df_visi['usage_time'].astype(int)

    _visib = {}
    for ix_i, row in df_visi.iterrows():
        p_i = row.prefix
        t_i = row.usage_time

        if p_i not in _visib.keys():
            print(ix_i)
            _visib.setdefault(p_i, 0)
            _visib[p_i] = t_i

    #############################################
    for i_vp in range(0, len(final_vps)):
        _vp = final_vps[i_vp]
        df_v = df_rib.loc[(df_rib['vp'] == _vp)]
        df_v.reset_index(drop=True, inplace=True)
        _rib = {}

        for ix_i, row in df_v.iterrows():
            p_i = row.prefix
            t_i = row.time
            as_i = row.path
            or_i = row.origin
            com_i= row.community

            if p_i not in _rib.keys():
                print(ix_i)
                _rib.setdefault(p_i, [])

                if p_i in _traffic.keys():
                    _rib[p_i].append(t_i)
                    _rib[p_i].append(as_i)
                    _rib[p_i].append(or_i)
                    _rib[p_i].append(com_i)
                    _rib[p_i].append(_traffic[p_i][0])
                    _rib[p_i].append(_traffic[p_i][1])
                    _rib[p_i].append(_traffic[p_i][2])
                    _rib[p_i].append(_traffic[p_i][3])

                else:
                    _rib[p_i].append(t_i)
                    _rib[p_i].append(as_i)
                    _rib[p_i].append(or_i)
                    _rib[p_i].append(com_i)
                    _rib[p_i].append(0)
                    _rib[p_i].append(0)
                    _rib[p_i].append(0)
                    _rib[p_i].append(0)

                if p_i in _visib.keys():
                    _rib[p_i].append(_visib[p_i])

        f_all = path_clus + 'rib_traffic_' + str(i_vp) +'_2015.csv'
        with open(f_all, 'w') as f:
            for key in _rib.keys():
                f.writelines("%s|%d|%s|%s|%s|%d|%.8f|%d|%.8f|%d\n" % (key, _rib[key][0], _rib[key][1], _rib[key][2], _rib[key][3], _rib[key][4], _rib[key][5], _rib[key][6], _rib[key][7], _rib[key][8]))


    for i_vp in range(0, len(final_vps)):
        f_all = path_clus + 'rib_traffic_' + str(i_vp) + '_2015.csv'
        df_all = pd.read_csv(f_all, sep="|",
                              names=['prefix', 'time', 'path', 'origin', 'community', 'traffic', 'per_traffic', 'events', 'per_events', 'usage_time'])

        print('TRAFFIC vs EVENTS...')
        df_all.sort_values(by=['traffic'], ascending = False, inplace=True)
        y = (df_all['events'].values)
        cdf = (np.cumsum(y))
        cdf = (cdf / cdf[-1]) * 100

        ID = np.linspace(0, 100, len(df_all['per_traffic']) )

        plt.plot(ID, cdf, 'r-')
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        #plt.yscale('log')
        plt.xscale('log')
        plt.grid(True)
        plt.show()
        plt.xlabel('Traffic Volume (%)')
        plt.ylabel('BGP Events (%)')

        plt.savefig(path_save + 'Traffic_vs_Events' + str(i_vp) + '_3.png')
        print('Saved plot image\n')
        plt.close()

        ##############################################
        print('EVENTS vs TRAFFIC...')
        df_all.sort_values(by=['events'], inplace=True)

        y = (df_all['traffic'].values)
        cdf = (np.cumsum(y))
        cdf = (cdf / cdf[-1]) * 100

        ID = np.linspace(0, 100, len(df_all['events']))

        plt.plot(ID, cdf, 'r-')
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        plt.yscale('log')
        plt.xscale('log')
        plt.grid(True)
        plt.show()
        plt.ylabel('Traffic Volume (%)')
        plt.xlabel('BGP Events (%)')

        plt.savefig(path_save + 'Events_vs_Traffic' + str(i_vp) + '_3.png')
        print('Saved plot image\n')
        plt.close()

        #WE SAVE THE NEW FILE
        df_all_final = df_all[['prefix', 'time', 'path', 'origin', 'community', 'traffic', 'per_traffic']]
        f_all = path_clus + 'rib_final_' + str(i_vp) + '_2015.csv'
        df_all_final.to_csv(f_all, sep='|', encoding='utf-8')

        ################################################
        print('VISIBILITY vs TRAFFIC...')

        df_all['usage_time'] = df_all['usage_time'].astype(int)

        total_time = 259200
        df_all['per_usage'] = df_all.apply(lambda row: (int(row.usage_time)/(total_time))*100, axis=1)
        df_all.sort_values(by=['per_usage'], inplace=True)

        y = (df_all['per_traffic'].values)
        #y.sort()
        cdf = (np.cumsum(y))
        cdf = (cdf / cdf[-1]) * 100

        plt.plot(cdf, df_all['usage_time'] , 'r-')
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        plt.yscale('log')
        plt.xscale('log')
        plt.grid(True)
        plt.show()
        plt.xlabel('Traffic Volume(%)')
        plt.ylabel('Path Usage Time (s)')

        plt.savefig(path_save + 'Traffic_vs_Visibility' + str(i_vp) + '3.png')
        print('Saved plot image\n')
        plt.close()



