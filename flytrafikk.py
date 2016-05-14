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
pd.set_option('display.width', 1000)
import codecs
import json

def flytrafikk():
    url = 'http://data.ssb.no/api/v0/no/table/08507'
    with codecs.open('payload_8507.json', 'r', encoding='utf-8') as ff:
        payload = json.loads(ff.read())
    data = requests.post(url, json = payload)
    result = pyjstat.from_json_stat(data.json(object_pairs_hook=OrderedDict))
    frame = result[0]
    #frame[u'maaned'] = frame[u'måned']
    #frame = frame.drop(u'måned', 1)
    frame = frame.drop(u'trafikktype', 1)
    frame = frame.drop(u'trafikk', 1)
    frame = frame.drop(u'passasjergruppe', 1)
    frame = frame.drop(u'lufthavn', 1)
    ss = frame.groupby(u'måned').sum().rolling(window=12).sum()
    ss = ss[ss.value > 0] # remove NaNs
    ss = ss[ss.index >= '2010'] # let's start at 2010
    desc = u'Passasjerer, lufttransport. Glidande 12 måneders gjennomsnitt. 100=' + str(ss.index[0])
    ss[desc] = (ss.value * 100.0) / ss.value.values[0]
    ss = ss.drop(u'value', 1)
    plot = ss.plot()
    (xmin, xmax, ymin, ymax) = plot.axis()
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(10.0, 6.0)
    plot.axis((xmin, xmax, 0, 140.0))
    pylab.savefig('flytrafikk.png', bbox_inches='tight')
    print ss

if __name__=="__main__":
    fly = flytrafikk()
