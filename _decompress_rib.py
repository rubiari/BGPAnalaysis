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

from _rib_to_csv import _rib_to_csv

warnings.filterwarnings("ignore")


def _decompress_rib(filename):
    newfile = filename[:-4]
    with open(newfile, 'wb') as new_file, bz2.BZ2File(filename, 'rb') as file:
        for data in iter(lambda: file.read(100 * 1024), b''):
            new_file.write(data)

    rib = _rib_to_csv(newfile)

    # Remove .BZ2 file
    try:
        os.remove(filename)
    except OSError:
        pass

    return rib
