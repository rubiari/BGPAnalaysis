#!/usr/bin/env python

"""
MASTER'S FINAL PROJECT
'ANALYSIS BGP rate of prefix VS traffic/prefix'
David Arias Rubio
"""

"""
Download of the BGP Updatr traces from WIDE for a period of days 
between the day selected
(i.e., two days before and after 02-12-2015
We save this data in zompopo./srv/agarcia/TFM/BGP_TRACES_BZ2
"""

import os
import datetime as datetime
import requests
import idna
import warnings
from robobrowser import RoboBrowser

warnings.filterwarnings("ignore")

def _download_traces(dates, period):

    url = "http://archive.routeviews.org/route-views.wide/bgpdata/"

    MRAI_BIN_DIR = "/srv/agarcia/TFM/" #path to save files
    if(period == 0):
        dir = MRAI_BIN_DIR + "ONE_DAY_BGP_TRACES_BZ2/"
    elif (period == 1):
        dir = MRAI_BIN_DIR + "THREE_DAY_BGP_TRACES_BZ2/"
    else:
        dir = MRAI_BIN_DIR + "BGP_TRACES_BZ2/"

    if not os.path.exists(dir):
        os.makedirs(dir)

    for _dt in dates:

        dt = datetime.datetime.strptime(_dt, "%Y-%m-%d")
        dt_web = dt.strftime("%Y")+"."+dt.strftime("%m")+"/"

        print("Opening browser...")
        br = RoboBrowser()
        br.open(url)

        #Buscamos la fecha que queremos y hacemos click
        link_date= br.get_link(dt_web)
        br.follow_link(link_date)

        #Buscamos el link UPDATES y hacemos click
        link_update = br.get_link("UPDATES/")
        br.follow_link(link_update)

        #Obtenemos los 2 DIAS antes y despues de la fecha deseada
        #(5 dias en total)
        days = []
        days.append(dt)
        if (period != 0):
            for day_p in range(1, period+1):
                d_before =  dt - datetime.timedelta(days=day_p)
                d_after = dt + datetime.timedelta(days=day_p)
                days.insert(0, d_before)
                days.append(d_after)

        print(days)

        #Para cada dia descargamos todos los BGP update traces
        for day in days:
            print("Downloading files of day "+ day.strftime("%Y-%m-%d")+"\n")
            elem = "updates."+day.strftime("%Y")+day.strftime("%m")+day.strftime("%d")
            _dt_web = day.strftime("%Y") + "." + day.strftime("%m") + "/"
            br.back()
            br.back()
            br.follow_link(br.get_link(dt_web))
            br.follow_link(br.get_link("UPDATES/"))
            links = br.get_links(elem)
            for link in links:
                file = (str(link).split('"'))[1]
                url_dw = "http://archive.routeviews.org/route-views.wide/bgpdata/"+_dt_web+"UPDATES/"+file
                filename = dir+file

                r = requests.get(url_dw)
                with open(filename, "wb") as code:
                    code.write(r.content)