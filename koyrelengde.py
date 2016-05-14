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
    frame[u'kjorelengde'] = pd.to_numeric(frame.value)
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
    folk = folkemengde()
    kjor = kjorelengde()
    aar = u'år'
    m = pd.merge(folk, kjor, on=aar)
    m.index = m[aar]
    m['koyrelengde_per_person'] = (m.kjorelengde * 1000000) / m.folkemengde
    desc = u'Køyrelengde per person, 100=' + str(m.koyrelengde_per_person.index[0])
    m[desc] = (m.koyrelengde_per_person*100.0) / m.koyrelengde_per_person.values[0]
    ss = m.loc[:, [desc]]
    plot = ss.plot()
    (xmin, xmax, _, _) = plot.axis()
    plot.axis((xmin, xmax, 0.0, 125.0))
    if "--docker" in sys.argv:
        pylab.savefig('output/koyrelengde_per_person.png', bbox_inches='tight')
    else:
        pylab.savefig('koyrelengde_per_person.png', bbox_inches='tight')
