#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests_cache
import requests
import csv
import sys
from pyjstat import pyjstat
import requests
from collections import OrderedDict
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

def kjorelengde():
    url = 'http://data.ssb.no/api/v0/no/table/07301'
    payload = {"query": [{"code": "Kjoretoytype", "selection": {"filter": "item", "values": ["TOT",]}}, {"code": "ContentsCode", "selection": {"filter": "item", "values": ["Kjorekm"]}}, {"code": "Tid", "selection": {"filter": "all", "values": ["*"        ]}}], "response": {"format": "json-stat"}}
    data = requests.post(url, json = payload)
    result = pyjstat.from_json_stat(data.json(object_pairs_hook=OrderedDict))
    frame = result[0]
    frame[u'år'] = pd.to_numeric(frame[u'år'])
    frame.index = frame[u'år']
    frame[u'kjorelengde'] = pd.to_numeric(frame.value)
    return frame

def folkemengde():
    url = 'http://data.ssb.no/api/v0/no/table/06913'
    payload = {"query": [{"code": "Region", "selection": {"filter": "item", "values": ["0"]}}, {"code": "ContentsCode", "selection": {"filter": "item", "values": ["Folkemengde"]}}, {"code": "Tid", "selection": {"filter": "all", "values": ["*"]}}], "response": {"format": "json-stat"}}
    data = requests.post(url, json = payload)
    result = pyjstat.from_json_stat(data.json(object_pairs_hook=OrderedDict))
    frame = result[0]
    frame[u'år'] = pd.to_numeric(frame[u'år']) - 1
    frame.index = frame[u'år']
    frame[u'folkemengde'] = pd.to_numeric(frame[u'value'])
    return frame

if __name__=="__main__":
    folk = folkemengde()
    kjor = kjorelengde()
    aar = u'år'
    m = pd.merge(folk, kjor, on=u'år')
    m.index = m[aar]
    m['koyrelengde_per_person'] = (m.kjorelengde * 1000000) / m.folkemengde
    desc = u'Køyrelengde per person, 100=' + str(m.koyrelengde_per_person.index[0])
    m[desc] = (m.koyrelengde_per_person*100.0) / m.koyrelengde_per_person.values[0]
    ss = m.loc[:, [desc]]
    plot = ss.plot()
    (xmin, xmax, _, _) = plot.axis()
    plot.axis((xmin, xmax, 0.0, 120.0))
    import pylab
    pylab.savefig('foo.png', bbox_inches='tight')

