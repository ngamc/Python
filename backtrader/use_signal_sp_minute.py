# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 14:23:26 2018

@author: user
"""
import sys
sys.path.append('../')
from  HKStock.read_sp import Read_SP_Min_File_No_LastNight 
import backtrader as bt
from HKStock.getyahoodata import SPPandasData
import pandas as pd
import collections
import matplotlib
import matplotlib.pyplot as plt

MAINSIGNALS = collections.OrderedDict(
    (('longshort', bt.SIGNAL_LONGSHORT),
     ('longonly', bt.SIGNAL_LONG),
     ('shortonly', bt.SIGNAL_SHORT),)
)


EXITSIGNALS = {
    'longexit': bt.SIGNAL_LONGEXIT,
    'shortexit': bt.SIGNAL_LONGEXIT,
}

class SMACloseSignal(bt.Indicator):
    lines = ('signal',)
    params = (('period', 50),)

    def __init__(self):
        self.lines.signal = self.data - bt.indicators.SMA(period=self.p.period)


#class SMAExitSignal(bt.Indicator):
#    lines = ('signal',)
#    params = (('p1', 5), ('p2', 30),)
#
#    def __init__(self):
#        sma1 = bt.indicators.SMA(period=self.p.p1)
#        sma2 = bt.indicators.SMA(period=self.p.p2)
#        self.lines.signal = sma1 - sma2



def runstrat(df, smaperiod=10):
    signal="longonly"

    data = SPPandasData(dataname=df) 
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0) 

    cerebro.adddata(data)

    cerebro.add_signal(MAINSIGNALS[signal],
                       SMACloseSignal, period=smaperiod)


#    cerebro.add_signal(EXITSIGNALS[args.exitsignal],
#                       SMAExitSignal,
#                       p1=args.exitperiod,
#                       p2=args.smaperiod)
    cerebro.addsizer(bt.sizers.FixedSize, stake=1)
    cerebro.run()
#    cerebro.plot()
    return cerebro.broker.getvalue()


if __name__ =="__main__":
    df=Read_SP_Min_File_No_LastNight('2018', '6', '8')
    print(df)
    for i in range(3,50):
        value=runstrat(df, i)
        print("Final Value: ", i, ": ", value)
