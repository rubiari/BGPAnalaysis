#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
ANALYSIS OF THE NUMBER OF UPDATES PER EVENT
"""

import os
import datetime as datetime
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

def _events_vs_updates():

    path = expanduser("~") + '/tfmcode/clustering/2015/2015_3/'
    path_save = expanduser("~") + '/figures/'
    f_1 = path + 'df_2015_3.csv'

    print('Updates vs Events analysis...')
    df = pd.read_csv(f_1, sep = "|", names = ['prefix', 'time', 'vp', 'path', 'origin', 'community', 'cluster'], skiprows = 1)
    time_name = str(df['time'].iloc[0])

    _events = {}

    for ix, row in df.iterrows():
        c_i = row.cluster

        if c_i not in _events.keys():
            print(c_i)
            _events.setdefault(c_i, [])
            df_cluster = df.loc[(df['cluster'] == c_i)]
            df_cluster.sort_index(inplace=True)

            clus_len = len(df_cluster)
            _events[c_i].append(clus_len)

            if(clus_len>1):
                t1 = df_cluster['time'].iloc[0]
                t2 = df_cluster['time'].iloc[-1]
                t_event = t2 - t1
                _events[c_i].append(t_event)
            else:
                _events[c_i].append(0)

    
    f_2 = path + "events_vs_updates_" + time_name + '.csv'
    
    with open(f_2, 'w') as f:
        for key in _events.keys():
            f.write("%d,%.5f,%d\n" % (key, _events[key][0], _events[key][1]))

    f_2 = path + "events_vs_updates_" + time_name + '.csv'

    df_eve = pd.read_csv(f_2, sep=",", names=['cluster', 'n_updates', 'usage_time'])
    df_eve.sort_values(by='n_updates', ascending=False, inplace = True)

    ID_event = np.linspace(1, len(df_eve), len(df_eve))

    plt.plot(ID_event, df_eve['n_updates'], 'g-')
    plt.yscale('log')
    plt.xscale('log')
    plt.grid(True)
    plt.xlabel('# BGP Events')
    plt.ylabel('# Updates')
    plt.show()

    plt.savefig(path_save + 'Events_VS_Updates_3day.png')
    print('Saved plot image\n')
    plt.close()

    ####################################################

    df_eve.sort_values(by='usage_time', inplace = True)

    plt.plot(df_eve['usage_time'], ID_event, 'g-')
    plt.yscale('log')
    plt.xscale('log')
    plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter("{x}"))
    plt.grid(True)
    plt.ylabel('# BGP Events')
    plt.xlabel('Usage Time (s)')
    plt.show()

    plt.savefig(path_save + 'UsageTime_vs_Events_3day.png')
    print('Saved plot image\n')
    plt.close()