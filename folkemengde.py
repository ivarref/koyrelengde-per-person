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

def sverige_folkemengde():
    url = 'http://api.scb.se/OV0104/v1/doris/en/ssd/BE/BE0101/BE0101A/BefolkningNy'
    payload = {"query": [
        {"code": "ContentsCode", "selection":
         {"filter": "item", "values": ["BE0101N1"]}},
        {"code": "Region", "selection":
         {"filter": "item", "values": ["00"]}},
        {"code": "Tid", "selection":
         {"filter": "all", "values": ["*"]}}],
               "response": {"format": "json-stat"}}
    data = requests.post(url, json = payload)
    result = pyjstat.from_json_stat(data.json(object_pairs_hook=OrderedDict))
    frame = result[0]
    frame[u'år'] = pd.to_numeric(frame[u'year']) 
    frame[u'folkemengde_sverige'] = pd.to_numeric(frame[u'value'])
    return frame

if __name__=="__main__":
    sv = sverige_folkemengde()
    folk = folkemengde()
    folk = folk[folk[u'år'] >= 1990]
    m = pd.merge(folk, sv, on=u'år')
    m[u'Tid'] = pd.to_datetime(m[u'år'], format='%Y')
    m.index = m[u'Tid']
    desc = 'Folkemengde, Noreg. 1990=100'
    m[desc] = (100.0 * m.folkemengde) / m.folkemengde.values[0]

    desc2 = 'Folkemengde, Sverige. 1990=100'
    m[desc2] = (100.0 * m.folkemengde_sverige) / m.folkemengde_sverige.values[0]

    ss = m.loc[:, [desc, desc2]]
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
    txt = "%4d=%.f" % (ss.index[-1].year, ss[desc2].values[-1])
    ax.annotate(txt, (mdates.date2num(ss.index.values[-1]), ss[desc2].values[-1]),
                xytext=(-10, -20),
                textcoords='offset points',
                ha='right',
                va='baseline',
                arrowprops={"arrowstyle" : '-|>', "mutation_scale":500**.5})
    pylab.savefig('folkemengde.png', bbox_inches='tight')
