# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 13:02:58 2018

Leading indicator
Check if the first df is leading the second df in time

@author: Nelson
"""
import pandas as pd
from read_sp import Read_SP_Ticker_Period, Read_SP_Min_File
from stockstats import StockDataFrame as Sdf
import matplotlib.pyplot as plt


def Leading(df1, df2):
    print(type(df1))
    print(type(df2))
#    a=pd.Series(range(1,10))
#    b=pd.Series(range(10,20))
    
    df = pd.concat([df1, df2], axis=1)
    df.columns = ['first', 'second']
    df.dropna(inplace=True)
      
    period = 10
    direction1 = None
    count_direction1 = 0
    trend1 = []
    direction2 = None
    count_direction2 = 0
    trend2 = []
    
    direction_change = False
    hit = 0
    for i in range(period, len(df)):
#        print(df.index[i])
#        if (df.iloc[i,0] > df.iloc[i-period,0]) & (df.iloc[i,1] > df.iloc[i-period,1]) :
#            print("+ +",df.iloc[i,0], df.iloc[i-period,0] )
#        if (df.iloc[i,0] > df.iloc[i-period,0]) & (df.iloc[i,1] < df.iloc[i-period,1]) :
#            print("+ -",df.iloc[i,0], df.iloc[i-period,0])        
#        if (df.iloc[i,0] < df.iloc[i-period,0]) & (df.iloc[i,1] < df.iloc[i-period,1]) :
#            print("- -",df.iloc[i,0], df.iloc[i-period,0])
#        if (df.iloc[i,0] < df.iloc[i-period,0]) & (df.iloc[i,1] > df.iloc[i-period,1]) :
#            print("- +",df.iloc[i,0], df.iloc[i-period,0])  
            
        if df.iloc[i,0] > df.iloc[i-period,0]:
            if direction1 == "Up":
                count_direction1 +=1
            else:
                trend1.append(count_direction1)
                count_direction1 = 1
                direction1 = "Up"
                direction_change = True
        elif df.iloc[i,0] < df.iloc[i-period,0]:
            if direction1 == "Down":
                count_direction1 +=1
            else:
                trend1.append(count_direction1)
                count_direction1 = 1
                direction1 = "Down"
                direction_change = True
        
        if df.iloc[i,1] > df.iloc[i-period,1]:
            if direction2 == "Up":
                count_direction2 +=1
            else:
                trend2.append(count_direction2)
                count_direction2 = 1
                direction2 = "Up"
                if direction_change == True:
                    if direction1 == "Up":
                        hit +=1
                    direction_change = False    
                    
        elif df.iloc[i,1] < df.iloc[i-period,1]:
            if direction2 == "Down":
                count_direction2 +=1
            else:
                trend2.append(count_direction2)
                count_direction2 = 1
                direction2 = "Down"
                if direction_change == True:
                    if direction1 == "Down":
                        hit +=1
                    direction_change = False
                    
    print(trend1)
    plt.hist(trend1,20)
    print(trend2)
    plt.hist(trend2, 20)
    plt.plot()
    print("Hit %.2f%%" %(hit/len(trend2)*100))
    print("trend1: %d  trend2: %d"%(len(trend1), len(trend2)))
#    print(df)    
    
#    print ("percentage: %.2f" % (count/len(df)*100))
        

if __name__ == '__main__':
#    df1 = Read_SP_Ticker_Period('1m','2018','6','8', index='datetime')
    df1 = Read_SP_Min_File('2018','6','13')
    s_df = Sdf.retype(df1)
    
    df1['sma'] = s_df['close_30_sma']

#    print(df1[['close', 'close_3_sma']])
    
    Leading(df1['close'], df1['close_30_sma'])