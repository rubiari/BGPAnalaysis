#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
FINAL PLOT BGP EVENTS/ TRAFFIC
"""

import os
import pandas as pd
import warnings
import matplotlib
import ipaddress
import csv
import matplotlib.ticker as ticker
import seaborn as sns
import math
import numpy as np
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from os.path import expanduser

warnings.filterwarnings("ignore")



def _final_graph():
    path_clus = expanduser("~") + '/tfmcode/clustering/2014/2014_3/'
    path_save = expanduser("~") + '/figures/'
    final_vps = ['202.249.2.169', '202.249.2.86']

    for i_vp in range(0, len(final_vps)):
        f_all = path_clus + 'rib_traffic_' + str(i_vp) + '_2014.csv'
        df_all = pd.read_csv(f_all, sep="|",
                             names=['prefix', 'time', 'path', 'origin', 'community', 'traffic', 'per_traffic', 'events',
                                    'per_events', 'usage_time'])

        #df_all = df_all.loc[df_all['events'] != 0]

        total_bytes = 0
        for ix, row in df_all.iterrows():
            total_bytes += int(row.traffic)

        df_all['per_traffic'] = df_all.apply(lambda row: (int(row.traffic) / (total_bytes)) * 100, axis=1)

        total_eve = 0
        for ix, row in df_all.iterrows():
            total_eve += int(row.events)

        df_all['per_events'] = df_all.apply(lambda row: (int(row.events) / (total_eve)) * 100, axis=1)


        print('BUBBLE PLOT...')
        df_all.sort_values(by=['traffic'], ascending = False, inplace=True)

        scat0 = sns.regplot(x=df_all['events'], y=df_all['per_traffic'], fit_reg=False)
        plt.yscale('log')
        #plt.xscale('log')
        plt.xlim((0, 150))
        plt.grid(True)
        plt.show()
        plt.ylabel('Traffic Volume (%)')
        plt.xlabel('BGP Events')
        fig = scat0.get_figure()
        fig.savefig(path_save + 'BubblePlot' + str(i_vp) + '_3.png')
        print('Saved plot image\n')
        plt.close()

        #print(len(df_all))
        df_all.sort_values(by=['traffic'], inplace=True)

        _evepref = {}
        per_total = 0
        n_events = 0
        n = 1
        per_eve = 0

        primer = False
        for ix, row in df_all.iterrows():
            per_i = row.per_traffic
            #n_events += row.events
            per_eve += row.per_events
            per_total += per_i

            if (per_total > 10):
                per_total = n * 10
                print (per_total)
                n += 1
                _evepref.setdefault(per_total, 0)
                #porc_events = n_events/n_prefix
                _evepref[per_total] = per_eve
                n_events = 0
                per_total = 0
                per_eve = 0

        print(_evepref)

        height = [_evepref[40],
                  _evepref[30], _evepref[20], _evepref[10]]

        bars = ('70%', '10%', '10%', '10%' )
        y_pos = np.arange(len(bars))

        plt.bar(y_pos, height, color=['hotpink', 'magenta', 'mediumorchid', 'purple'])
        plt.xticks(y_pos, bars)
        plt.grid(True)
        plt.yscale('log')
        plt.show()
        plt.ylabel('%Events')
        plt.xlabel('More to Less Volume of Traffic (%)')
        plt.savefig(path_save + 'Final_Graph' + str(i_vp) + '_3.png')
        print('Saved plot image\n')
        plt.close()