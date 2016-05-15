#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyjstat import pyjstat
import requests
from collections import OrderedDict
import pandas as pd
import pylab
import sys
import matplotlib.pyplot
import matplotlib
matplotlib.style.use('ggplot')

def kjorelengde():
    url = 'http://data.ssb.no/api/v0/no/table/07301'
    payload = {"query": [{"code": "Kjoretoytype", "selection": {"filter": "item", "values": ["15",]}}, {"code": "ContentsCode", "selection": {"filter": "item", "values": ["Kjorekm"]}}, {"code": "Tid", "selection": {"filter": "all", "values": ["*"        ]}}], "response": {"format": "json-stat"}}
    data = requests.post(url, json = payload)
    result = pyjstat.from_json_stat(data.json(object_pairs_hook=OrderedDict))
    frame = result[0]
    frame[u'år'] = pd.to_numeric(frame[u'år'])
    frame[u'koyrelengde'] = pd.to_numeric(frame.value)
    return frame

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
    print u'building koyrelengde ...'
    folk = folkemengde()
    kjor = kjorelengde()
    aar = u'år'
    m = pd.merge(folk, kjor, on=aar)
    m = m[m[aar] >= 2007]
    m.index = m[aar]
    m['koyrelengde_per_person'] = (m.koyrelengde * 1000000) / m.folkemengde

    m.tmp = (m.koyrelengde_per_person*100.0) / m.koyrelengde_per_person.values[0]
    desc = u'Køyrelengde per person, %d=100, %d=%.f' % (m.index[0], m.index.values[-1], m.tmp.values[-1])
    m[desc] = m.tmp

    m.tmp = (m.koyrelengde*100.0) / m.koyrelengde.values[0]
    desc2 = u'Køyrelengde, %d=100, %d=%.f' % (m.index[0], m.index.values[-1], m.tmp.values[-1])
    m[desc2] = m.tmp

    m.tmp = (m.folkemengde*100.0) / m.folkemengde.values[0]
    desc3 = u'Folkemengde, %d=100, %d=%.f' % (m.index[0], m.index.values[-1], m.tmp.values[-1])
    m[desc3] = m.tmp

    ss = m.loc[:, [desc3, desc2, desc]]
    plot = ss.plot()
    (xmin, xmax, _, _) = plot.axis()
    plot.axis((xmin, xmax, 0.0, 130.0))
    fig = matplotlib.pyplot.gcf()
    ax = fig.axes[0]
    x_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
    ax.xaxis.set_major_formatter(x_formatter)
    pylab.savefig('koyrelengde_per_person.png', bbox_inches='tight')
    print u'building koyrelengde ... OK'
