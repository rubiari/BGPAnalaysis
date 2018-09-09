#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
VISIBILITY: FRACTION OF TIME/ROUTE TO DESTINATION PREFIX
"""

import os
import datetime as datetime
import pandas as pd
import warnings
import matplotlib
import ipaddress
import csv

matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from scipy.spatial import distance
import matplotlib.dates as md
import math
import numpy as np
import seaborn as sns
from os.path import expanduser

warnings.filterwarnings("ignore")
from itertools import islice


def _best_path():
    path_vis = expanduser("~") + '/tfmcode/visibility/2014_3/'
    path_clus = expanduser("~") + '/tfmcode/clustering/2014/2014_3/'
    path_save = expanduser("~") + '/figures/'

    final_vps = ['202.249.2.169', '202.249.2.86']

    print('Best path analysis...')

    for i_vp in range(0, len(final_vps)):
        f_rib = path_clus + 'rib_final_' + str(i_vp) + '_2014.csv'
        df_rib = pd.read_csv(f_rib, sep="|", names=['prefix', 'time', 'path', 'origin', 'community', 'traffic', 'per_traffic'], skiprows = 1)

        _traffic = {}
        for ix, row in df_rib.iterrows():
            p_i = row.prefix
            if p_i not in _traffic.keys():
                _traffic.setdefault(p_i,[])
                _traffic[p_i].append(row.traffic)
                _traffic[p_i].append(row.per_traffic)

        f_path = path_vis + 'path_usage_time_' + str(i_vp) + '_3.csv'
        df_all = pd.read_csv(f_path, sep="|",
                              names=['prefix', 'as_path', 'usage_time', 'as_path_length', 'origin', 'community'])

        _bestpath = {}
        for ix, row in df_all.iterrows():
            print(ix)
            p_i = row.prefix
            if p_i not in _bestpath.keys():
                _bestpath.setdefault(p_i, [])
                _bestpath[p_i].append(row.as_path)
                _bestpath[p_i].append(row.usage_time)
                _bestpath[p_i].append(row.as_path_length)
                _bestpath[p_i].append(row.origin)
                _bestpath[p_i].append(row.community)

            else:
                t_i = row.usage_time
                t_j = _bestpath[p_i][1]
                if (t_i > t_j):
                    _bestpath[p_i][0] = row.as_path
                    _bestpath[p_i][1] = t_i
                    _bestpath[p_i][2] = row.as_path_length
                    _bestpath[p_i][3] = row.origin
                    _bestpath[p_i][4] = row.community

                else:
                    continue


        for key in _bestpath.keys():
            if key in _traffic.keys():
                _bestpath[key].append(_traffic[key][0])
                _bestpath[key].append(_traffic[key][1])
            else:
                _bestpath[key].append(0)
                _bestpath[key].append(0)


        filename = path_vis + "best_paths_"+ str(i_vp) +"_2014.csv"
        with open(filename, 'w') as f:
            for key in _bestpath.keys():
                f.writelines("%s|%s|%d|%d|%s|%s|%d|%.8f\n" % (
                    key, _bestpath[key][0], _bestpath[key][1],_bestpath[key][2], _bestpath[key][3], _bestpath[key][4], _bestpath[key][5], _bestpath[key][6]))
            f.close()

    # FINAL CORRELATIONS
    for i_vp in range(0, len(final_vps)):
        filename = path_vis + "best_paths_" + str(i_vp) + "_2014.csv"
        df_best = pd.read_csv(filename, sep = "|", names = ['prefix', 'as_path', 'usage_time', 'as_path_length', 'origin', 'community', 'traffic', 'per_traffic'])


        # TRAFFIC vs PATH LENGTH
        df_best.sort_values(by = 'as_path_length', ascending = False, inplace = True)

        plt.plot(df_best['as_path_length'], df_best['per_traffic'], 'ro')
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        plt.yscale('log')
        plt.grid(True)
        plt.show()
        plt.xlabel('Path Length')
        plt.ylabel('Volume of Traffic (%)')

        plt.savefig(path_save + 'PathLength_vs_Traffic' + str(i_vp) + '_3.png')
        print('Saved plot image\n')
        plt.close()
        
        # TRAFFIC vs ORIGIN
        _IGP = 0
        _EGP = 0
        _INC = 0

        for ix, row in df_best.iterrows():
            print(ix)
            origin = row.origin

            if (origin == 'IGP'):
                _IGP += row.per_traffic
            elif (origin == 'EGP'):
                _EGP += row.per_traffic
            else:
                _INC += row.per_traffic

        height = [_IGP, _EGP, _INC]
        bars = ('IGP', 'EGP', 'INCOMPLETE')
        y_pos = np.arange(len(bars))

        plt.bar(y_pos, height, color=['red', 'orange', 'gold'])
        plt.xticks(y_pos, bars)
        plt.grid(True)
        plt.yscale('log')
        plt.show()
        plt.xlabel('ORIGIN Attribute')
        plt.ylabel('Volume of Traffic (%)')
        plt.savefig(path_save + 'Origin_vs_Traffic' + str(i_vp) + '_3.png')
        print('Saved plot image\n')
        plt.close()


        # TRAFFIC vs COMMUNITY
        _CERO = 0
        _UNO = 0
        _DOS = 0
        for ix, row in df_best.iterrows():
            c_i = row.community
            if (isinstance(c_i, str) == True):
                len_i = len(c_i.split(" "))
                if len_i == 1:
                    _UNO += row.per_traffic
                elif len_i == 2:
                    _DOS += row.per_traffic
            else:
                _CERO += row.per_traffic

        height = [_CERO, _UNO, _DOS]
        bars = ('NO COMMUNITY', '1 COMMUNITY', '2 COMMUNITIES')
        y_pos = np.arange(len(bars))

        plt.bar(y_pos, height, color=['red', 'orange', 'gold'])
        plt.xticks(y_pos, bars)
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        plt.grid(True)
        plt.yscale('log')
        plt.show()
        plt.xlabel('COMMUNITY Attribute')
        plt.ylabel('Volume of Traffic (%)')
        plt.savefig(path_save + 'Community_vs_Traffic' + str(i_vp) + '_3.png')
        print('Saved plot image\n')
        plt.close()