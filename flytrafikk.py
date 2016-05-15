#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyjstat import pyjstat
import requests
from collections import OrderedDict
import pandas as pd
import numpy as np
import pylab
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
matplotlib.style.use('ggplot')
pd.set_option('display.width', 1000)
import codecs
import json
import datetime
import helpers

def flytrafikk():
    frame = helpers.get_table('http://data.ssb.no/api/v0/no/table/08503', 'payload_8503.json')
    frame[u'Tid'] = pd.to_datetime(frame[u'måned'], format='%YM%m')
    frame = frame.drop(u'måned', 1)
    frame = frame.drop(u'trafikktype', 1)
    frame = frame.drop(u'trafikk', 1)
    frame = frame.drop(u'flybevegelse', 1)
    frame = frame.drop(u'lufthavn', 1)
    ss = frame.groupby(u'Tid').sum().rolling(window=12).sum()
    ss = ss[ss.value > 0] # remove NaNs
    ss.index = ss.index.astype(datetime.datetime)
    ss = ss[ss.index >= datetime.datetime(2010, 1,1)]
    desc = u'Flybevegelser, total ankomst og avgang, innland og utland. 12 måneders gjennomsnitt. ' + str(ss.index[0].year) + '=100'
    ss[desc] = (ss.value * 100.0) / ss.value.values[0]
    ss = ss.drop(u'value', 1)
    plot = ss.plot()
    (xmin, xmax, ymin, ymax) = plot.axis()
    plot.axis((xmin, xmax, 0, ymax))
    fig = matplotlib.pyplot.gcf()
    ax = fig.axes[0]
    fig.set_size_inches(12.0, 6.0)

    txt = "%4d-%02d=%.f" % (ss.index[-1].year, ss.index[-1].month, ss[desc].values[-1])
    ax.annotate(txt, (mdates.date2num(ss.index.values[-1]), ss[desc].values[-1]),
                xytext=(-10, -20),
                textcoords='offset points',
                ha='right',
                va='baseline',
                arrowprops={"arrowstyle" : '-|>', "mutation_scale":500**.5})
    pylab.savefig('flytrafikk.png', bbox_inches='tight')

if __name__=="__main__":
    print "[%s] generating flytrafikk.png ... " % (str(datetime.datetime.now()))
    fly = flytrafikk()
    print "[%s] generating flytrafikk.png ... OK" % (str(datetime.datetime.now()))


