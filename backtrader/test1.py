# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 08:37:54 2018

@author: user
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
#import sys
import pandas as pd
from datetime import date
from getyahoodata import GetYahooData
from getyahoodata import MyPandasData
import backtrader as bt


# Create a Stratey
class TestStrategy(bt.Strategy):

    params=(
            ('maperiod', 10),
            ('printlog', False),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
               self.dataopen = self.datas[0].open
               self.datahigh = self.datas[0].high
               self.datalow = self.datas[0].low
               self.dataclose = self.datas[0].close
               self.datavolume = self.datas[0].volume
               self.sma=bt.indicators.SimpleMovingAverage(
                       self.datas[0].close, period=self.p.maperiod)
               self.order = None
               self.buyprice = None
               self.buycomm = None
               
    def notify_order(self,order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
               
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
        
    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:
                    # current close less than previous close

                    # BUY, BUY, BUY!!! (with default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.buy()

        else:

            # Already in the market ... we might sell
            if (self.sma[0] > self.dataclose[0]):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)




class SMA_CrossOver(bt.Strategy):

    params = (('fast', 10), ('slow', 30))

    def __init__(self):

        sma_fast = bt.indicators.SMA(period=self.p.fast)
        sma_slow = bt.indicators.SMA(period=self.p.slow)

        self.buysig = bt.indicators.CrossOver(sma_fast, sma_slow)

    def next(self):
        if self.position.size:
            if self.buysig < 0:
                self.sell()

        elif self.buysig > 0:
            self.buy()
            
def printTradeAnalysis(analyzer):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
    #Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total,2)
    strike_rate = (total_won / total_closed) * 100
    #Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate','Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed,total_won,total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    #Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    #Print the rows
    print_list = [h1,r1,h2,r2]
    row_format ="{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('',*row))
 
def printSQN(analyzer):
    sqn = round(analyzer.sqn,2)
    print('SQN: {}'.format(sqn))
        
if __name__=='__main__':
    #
    # Define equity and start date of equity data
    equity="0700.HK"
    startdate=date(2018,1,1)
         
    
    print("\r\n\r\n     ==== Testing with stock", equity, " ====\r\n")
    df=pd.DataFrame()
    df=GetYahooData(equity, startdate )
    print(df)
    df.to_csv("D:\\yes2.csv", sep=',')
#    if (len(df)<2):
#        print("Error getting data")
#        sys.exit()
    
    data = MyPandasData(dataname=df) 
    
    # Create a cerebro entity
    cerebro = bt.Cerebro(maxcpus=1)
    
#    strats = cerebro.optstrategy(
#        TestStrategy,
#        maperiod=range(10, 100),
#        )

    # Add a strategy
#    cerebro.addstrategy(TestStrategy)
    
    cerebro.addstrategy(TestStrategy)
    
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)
    
    cerebro.addsizer(bt.sizers.FixedSize, stake=200)

    # Print out the starting conditions
#    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.broker.setcommission(commission=0.0)
    
    cerebro.addanalyzer(bt.analyzers.AnnualReturn)
#    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
    
    # Run over everything
    mystrategy = cerebro.run()
    
    for x in mystrategy[0].analyzers:
        x.print()
    
#    printTradeAnalysis(mystrategy[0].analyzers.ta.get_analysis())
    printSQN(mystrategy[0].analyzers.sqn.get_analysis())
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    cerebro.plot(style='candle')
    
    