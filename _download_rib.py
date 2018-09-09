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

from  _decompress_rib import _decompress_rib

def _download_rib(dir, date):
    url = "http://archive.routeviews.org/route-views.wide/bgpdata/"

    dt_web = date.strftime("%Y") + "." + date.strftime("%m") + "/"

    print("Looking for RIB file...")
    br = RoboBrowser()
    br.open(url)

    link_date = br.get_link(dt_web)
    br.follow_link(link_date)

    link_rib = br.get_link("RIBS/")
    br.follow_link(link_rib)

    elem = "rib." + date.strftime("%Y") + date.strftime("%m") + date.strftime("%d")
    _dt_web = date.strftime("%Y") + "." + date.strftime("%m") + "/"
    links = br.get_links(elem)
    one_link = links[0]

    file = (str(one_link).split('"'))[1]
    url_dw = "http://archive.routeviews.org/route-views.wide/bgpdata/" + _dt_web + "RIBS/" + file
    filename = dir + file

    r = requests.get(url_dw)
    with open(filename, "wb") as code:
        code.write(r.content)

    rib = _decompress_rib(filename)

    return rib