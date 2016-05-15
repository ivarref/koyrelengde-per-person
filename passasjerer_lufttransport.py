#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd, pylab, sys, datetime, helpers
import matplotlib, matplotlib.pyplot, matplotlib.dates as mdates
matplotlib.style.use('ggplot')
pd.set_option('display.width', 1000)

if __name__=="__main__":
    frame = helpers.get_table('http://data.ssb.no/api/v0/no/table/08507', 'payload_8507.json')
    frame[u'Tid'] = pd.to_datetime(frame[u'måned'], format='%YM%m')
    frame = frame.drop(u'måned', 1).drop(u'trafikktype', 1).drop(u'trafikk', 1).drop(u'passasjergruppe', 1).drop(u'lufthavn', 1)
    ss = frame.groupby(u'Tid').sum().rolling(window=12).sum()
    ss = ss[ss.value > 0] # remove NaNs
    ss.index = ss.index.astype(datetime.datetime)
    ss = ss[ss.index >= datetime.datetime(2010, 1,1)]
    desc = u'Passasjerer, lufttransport. Glidande 12 måneders gjennomsnitt. %s=100' % (str(ss.index[0].year))
    ss[desc] = (ss.value * 100.0) / ss.value.values[0]
    ss = ss.drop(u'value', 1)
    plot = ss.plot()
    (xmin, xmax, ymin, ymax) = plot.axis()
    plot.axis((xmin, xmax, 0, 140.0))
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(10.0, 6.0)
    ax = fig.axes[0]
    txt = "%d-%02d=%.f" % (ss.index[-1].year, ss.index[-1].month, ss[desc].values[-1])
    ax.annotate(txt, (mdates.date2num(ss.index.values[-1]), ss[desc].values[-1]),
                xytext=(-10, -20), textcoords='offset points',
                ha='right', va='baseline',
                arrowprops={"arrowstyle" : '-|>', "mutation_scale":500**.5})
    pylab.savefig('passasjerer_lufttransport.png', bbox_inches='tight')
