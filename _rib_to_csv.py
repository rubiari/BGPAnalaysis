#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
RIB TO CSV
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

warnings.filterwarnings("ignore")
import datetime as datetime
import requests
from robobrowser import RoboBrowser

def _rib_to_csv(filename):
    MRAI_BIN_DIR = "/srv/agarcia/TFM/"
    update_lines = subprocess.check_output([MRAI_BIN_DIR + '/bgpdump', '-m', filename],
                                           stderr=subprocess.STDOUT).strip().split('\n')

    fname = filename + ".csv"
    with open(fname, 'wb') as myfile:
        wr = csv.writer(myfile, delimiter='\n', quoting=csv.QUOTE_NONE)
        wr.writerow(update_lines)

    # Remove TRACE file
    try:
        os.remove(filename)
    except OSError:
        pass

    return fname