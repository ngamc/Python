# -*- coding: utf-8 -*-
"""
Created on Mon May 21 15:30:26 2018
use Keras to try to predict if the next candle stick is go up/ go down / stay still
x is the hlcv number of n candlestick (defined by num_candle_stick)
y is simply buy / sell / no action
@author: user
"""

from Lib_SP_Min import get_file_list, read_df
import numpy
import sys

data_file_path = "c:\\spdata\\2018\\"
num_candlestick = 2       # number of candle stick submitted as x's features
cut_loss_pt = 5     # if next low < current close - cut_loss_pt we will not buy
target_pt   = 5     # if next high - target_pt > current close we will buy
day_start = '09/18/00'      # this is consider as the first candlestick

filelist = get_file_list(data_file_path)   # use \\ in subfolder

for file in filelist:
    df = read_df(file)
    if (df.empty == False):         # df is empty if it is not valid
        print(file, df.shape)
        df.columns=['datetime','open','high','low','close','volume']
        
        # remove all entries before 09:18
        num=df.loc[df['datetime'].str.contains(day_start)].index.values
        
        df=df[num[0]:]
#        print(df.iloc[0:5])
        
        x_raw=df.values[:,1:6]      # convert to numpy array
#        print(x_raw.shape)


        x = []
        y = []
        idx=0
        x_list=x_raw.tolist()
        
        for open, high, low, close, volume in x_list:
            x_instance = []
                   
            # we each n candlestick's hlcv
            for i in range(num_candlestick):
                x_list_next = x_list[idx+i]
                x_instance.append(x_list_next[1] - open)
                x_instance.append(x_list_next[2] - open)
                x_instance.append(x_list_next[3] - open)
                x_instance.append(x_list_next[4])
             
            x.append(x_instance)
                
                
            # obtain y value
            # action value: 0 - no action 1 - buy 2-sell
            x_list_target = x_list[idx+num_candlestick]
            p_close = x_list[idx + num_candlestick - 1][3]  # previous candlestick close
            action = 0          
            
            y_open   = x_list_target[0]
            y_high   = x_list_target[1]
            y_low    = x_list_target[2]
            y_close  = x_list_target[3]
            y_volume = x_list_target[4]
            
            if y_low + cut_loss_pt >= p_close and y_high > p_close + target_pt:
                action = 1
            elif (y_high - cut_loss_pt <= p_close) and (y_low < p_close - target_pt):
                action = -1
                
            y.append(action)
                    
            if (idx==len(x_list) - num_candlestick - 2):
                break
            else:
                idx=idx+1
       
        print(x)
        x_numpy = numpy.asarray(x)
        y_numpy = numpy.asarray(y)
        
        print(x_numpy.shape)
        print(x_numpy)
        print(y_numpy)
        
        sys.exit()
 