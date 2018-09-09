#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
MAIN PROGRAM OF OUR PROJECT FROM WHICH WE CALL TO THE DIFFERENT
FUNCTIONS THAT IMPLEMENT THE SEVERAL STEPS TO OBTAIN THE RESULTS
"""

from _download_traces import _download_traces
from _decompress_traces import _decompress_traces
from _trace_to_csv import _trace_to_csv
from _csv_to_pandas import _csv_to_pandas
from _ts_to_date import _ts_to_date
from _cleaning_updates import _cleaning_updates
from _clustering_updates import _clustering_updates
from _numberof_vs_prefix import _numberof_vs_prefix
from _events_vs_updates import _events_vs_updates
from _visibility import _visibility
from _sensibility import _sensibility
from _traffic_popularity import _traffic_popularity
from _visibility_path import _visibility_path
from _best_path import _best_path
from _final_graph import _final_graph


import os
import shutil
import csv
import sys
import locale
import datetime as datetime
from dateutil.relativedelta import relativedelta
import requests
import bz2
import urllib3
import warnings
import subprocess
import re
import pandas as pd
from robobrowser import RoboBrowser

warnings.filterwarnings("ignore")

# We read the dates desired by command
if len(sys.argv) == 1:
	print("Running ./BGPWIDE.py...")
# We use this mode if we already have downloaded and processed
# the BGP Update stream
elif len(sys.argv) == 2:
	print("Not enough arguments passed...")
	sys.exit(1)
elif (len(sys.argv) > 2):
	print("Running ./BGPWIDE.py...")
	date1 = str(sys.argv[1])
	date2 = str(sys.argv[2])
	period = 0

	if (len(sys.argv) == 3):
		period = 0
	elif (len(sys.argv) == 4):
		period = int(sys.argv[3])

	dates = [date1, date2]
	print("Requested dates: " + dates[0] + " and " + dates[1])

	_download_traces(dates, period)
	_decompress_traces(period)
	_trace_to_csv(period)



print("Converting traces in pandas dataframes...")
_frames = _csv_to_pandas()

# PREPROCESSING - CLEANING and CLUSTERING DATA
_frames_ = []

for frame in _frames:
	print("Cleaning data...")
	frame1 = _cleaning_updates(frame)

	print('Clustering updates...')
	_clustering_updates(frame1)


# UPDATES/EVENTS ANALYSIS
_numberof_vs_prefix()

# UPDATES vs EVENTS ANALYSIS
_events_vs_updates()

# VISIBILITY (FRACTION OF TIME/DESTINATION PREFIX)
_visibility()

# SENSIBILITY of VISIBILTY AND CLUSTERING
_sensibility()

# TRAFFIC POPULARITY vs ROUTING EVENTS AND VISIBILITY
_traffic_popularity()

# VISIBILITY FOR PATH
_visibility_path()

# DEFINING BEST PATH FOR EVERY PREFIX
_best_path()

# FINAL GRAPH
_final_graph()


sys.exit()