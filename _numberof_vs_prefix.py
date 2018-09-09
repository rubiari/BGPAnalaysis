#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
ANALYSIS OF UPDATES AND EVENTES IN RELATION WITH PREFIXES
"""

import os
import pandas as pd
import warnings
import matplotlib
import csv
import matplotlib.ticker as ticker
import math
import numpy as np
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from os.path import expanduser
warnings.filterwarnings("ignore")


def _numberof_vs_prefix():

    path = expanduser("~") + '/tfmcode/clustering/2015/2015_3/'
    path_save = expanduser("~") + '/figures/'
    f_1 = path+'updates_2015_3.csv'
    f_2 = path+'events_2015_3.csv'

    print('Updates analysis...')
    df_upd = pd.read_csv(f_1, sep = ",", names = ['prefix', 'n_updates'], skiprows = 1)
    df_upd = df_upd.sort_values(by = 'n_updates', ascending=False)

    # We calculate the percentage of updates
    total_upd = 0
    for ix, value in df_upd['n_updates'].iteritems():
        total_upd += value
    print('Total #Updates: '+ str(total_upd))

    df_upd['per_updates'] = df_upd.apply(lambda row: (row.n_updates/(total_upd))*100, axis=1)
    df_upd.to_csv(f_1, sep=',', encoding='utf-8')

    prefix_ID = np.linspace(1, len(df_upd), len(df_upd))

    plt.plot(prefix_ID, df_upd['n_updates'], 'r-')
    plt.yscale('log')
    plt.xscale('log')
    plt.grid(True)
    plt.show()
    plt.xlabel('Prefix ID')
    plt.ylabel('Number of Updates')

    plt.savefig(path_save+'Prefix_vs_Updates_3day.png')
    print('Saved plot image\n')
    plt.close()


    ######################################################################

    print('Events analysis...')
    df_eve = pd.read_csv(f_2, sep=",", names=['prefix', 'n_events'], skiprows = 1)
    df_eve = df_eve.sort_values(by='n_events', ascending=False)

    # Calculation of percentage of events (for every prefix)
    total_eve = 0
    for ix, value in df_eve['n_events'].iteritems():
        total_eve += value

    df_eve['per_events'] = df_eve.apply(lambda row: (row.n_events/(total_eve))*100, axis=1)
    df_eve.to_csv(f_2, sep=',', encoding='utf-8')

    print('Total #Events: '+ str(total_eve))

    plt.plot(prefix_ID, df_eve['n_events'], 'r-')
    plt.yscale('log')
    plt.xscale('log')
    plt.grid(True)
    plt.show()
    plt.xlabel('Prefix ID')
    plt.ylabel('Number of Events')

    plt.savefig(path_save + 'Prefix_vs_Events_3day.png')
    print('Saved plot image\n')
    plt.close()