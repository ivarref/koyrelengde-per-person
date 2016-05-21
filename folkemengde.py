#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyjstat import pyjstat
import requests
from collections import OrderedDict
import pandas as pd
import pylab
import sys
import matplotlib.pyplot
import matplotlib.dates as mdates
import matplotlib
import datetime
matplotlib.style.use('ggplot')

def folkemengde():
    url = 'http://data.ssb.no/api/v0/no/table/06913'
    payload = {"query": [{"code": "Region", "selection": {"filter": "item", "values": ["0"]}}, {"code": "ContentsCode", "selection": {"filter": "item", "values": ["Folkemengde"]}}, {"code": "Tid", "selection": {"filter": "all", "values": ["*"]}}], "response": {"format": "json-stat"}}
    data = requests.post(url, json = payload)
    result = pyjstat.from_json_stat(data.json(object_pairs_hook=OrderedDict))
    frame = result[0]
    frame[u'år'] = pd.to_numeric(frame[u'år']) - 1
    frame[u'folkemengde'] = pd.to_numeric(frame[u'value'])
    return frame

if __name__=="__main__":
    folk = folkemengde()
    folk = folk[folk[u'år'] >= 1990]
    folk[u'Tid'] = pd.to_datetime(folk[u'år'], format='%Y')
    folk.index = folk[u'Tid']
    desc = 'Folkemengde, Noreg. 1990=100'
    folk[desc] = (100.0 * folk.folkemengde) / folk.folkemengde.values[0]
    ss = folk.loc[:, [desc]]
    ss.index = ss.index.astype(datetime.datetime)
    plot = ss.plot()
    (xmin, xmax, _, ymax) = plot.axis()
    plot.axis((xmin, xmax, 0.0, ymax))
    fig = matplotlib.pyplot.gcf()
    ax = fig.axes[0]
    txt = "%4d=%.f" % (ss.index[-1].year, ss[desc].values[-1])
    ax.annotate(txt, (mdates.date2num(ss.index.values[-1]), ss[desc].values[-1]),
                xytext=(-10, -20),
                textcoords='offset points',
                ha='right',
                va='baseline',
                arrowprops={"arrowstyle" : '-|>', "mutation_scale":500**.5})
    pylab.savefig('folkemengde.png', bbox_inches='tight')
