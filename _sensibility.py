#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
SENSIBILITY: how sensible are routing events and sensibility to the period
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

def _data_visibility(path, file):

    _files = []
    for f in os.listdir(path+file):
        if f.endswith(".csv") and ('path_usage_time_' in f):
            _files.append(f)

    _list = []
    for _file in _files:
        f_path = path + file + _file
        df = pd.read_csv(f_path, sep="|", names=['prefix', 'as_path', 'usage_time', 'as_path_length', 'origin', 'community'])
        _list.append(df)

    df_all = pd.concat(_list)
    df_all.sort_values(by='usage_time', ascending=False, inplace=True)

    _ID = []
    n = 0
    for ix, row in df_all['prefix'].iteritems():
        _ID.append(n)
        n += 1

    return df_all, _ID

#####################################

def _data_clustering(file):

    df = pd.read_csv(file, sep=",", names=['cluster', 'per_updates', 'usage_time'])
    df.sort_values(by='per_updates', ascending=False, inplace = True)

    perc = np.linspace(0, 99.9999, len(df))

    return perc, df

######################################

def _sensibility():
    print('Analyzing Sensibility for Visibility...')

    path = expanduser("~") + '/tfmcode/visibility/'
    path_save = expanduser("~") + '/figures/'

    #file1 = '2014/'
    file2 = '2015_3day/'
    file3 = '2015_1day/'

    #df_1, ID_1 = _data_visibility(path, file1)

    #Gathering of first files
    df_2, ID_2 = _data_visibility(path, file2)

    #Gathering of second files
    df_3, ID_3 = _data_visibility(path, file3)

    #plt.plot(ID_1, df_1['usage_time'], 'r-', label = '5 day period')
    plt.plot(ID_2, df_2['usage_time'], 'b-', label = '3 day period')
    plt.plot(ID_3, df_3['usage_time'], 'g-', label = '1 day period')
    plt.legend(loc='best')
    plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    plt.yscale('log')
    plt.grid(True)
    plt.show()
    plt.xlabel('Path ID')
    plt.ylabel('Path Usage Time (s)')

    plt.savefig(path_save + 'Sensibility_Visibility.png')
    print('Saved plot image\n')
    plt.close()
    ##############################################

    print('Analyzing Sensibility of Clustering...')
    path = expanduser("~") + '/tfmcode/clustering/2015/'
    #file1 = path + '2014/events_vs_updates_2014.csv'
    file2 = path + '2015_3/events_vs_updates_2015_3.csv'
    file3 = path + '2015_1/events_vs_updates_2015_1.csv'

    #Gathering of info
    #perc1, df1 = _data_clustering(file1)
    perc2, df2 = _data_clustering(file2)
    perc3, df3 = _data_clustering(file3)

    #plt.plot(perc1, df1['per_updates'], 'r-', label = '5 day period')
    plt.plot(perc2, df2['per_updates'], 'b-', label = '3 day period')
    plt.plot(perc3, df3['per_updates'], 'g-', label = '1 day period')
    plt.legend(loc='best')
    plt.yscale('log')
    plt.xscale('log')
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter("{x}"))
    plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter("{x}"))
    plt.grid(True)
    plt.xlabel('BGP Events (%)')
    plt.ylabel('BGP Updates (%)')
    plt.show()

    path = expanduser("~") + '/figures/'
    plt.savefig(path_save + 'Sensibility_Clustering.png')
    print('Saved plot image\n')
    plt.close()
