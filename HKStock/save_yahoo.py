# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 13:39:18 2018

@author: user
"""

import pandas as pd
import os
from getyahoodata import GetYahooData, StockCode
import datetime
import sys

allstockfilename = 'D:\\allstocklist.csv'
savepath = 'D:\\user\\Documents\\Python\\Ignore\\yahoo\\'
start = datetime.date(2000,1,1)
end = datetime.date.today()
yesterday = end - datetime.timedelta(1)
# sometimes there are empty lines in the file. This is to remove it
def remove_empty_lines(stock):
    filename = savepath + str(stock) +".csv"
    if os.path.isfile(filename):    
        with open(filename) as infile, open('tmpfile.csv', 'w') as outfile:
            for line in infile:
                if not line.strip(): continue  # skip the empty line
                outfile.write(line)  # non-empty line. Write it to output
        os.replace('tmpfile.csv', filename)
        
def load_one_stock(stock): 
    filename = savepath + str(stock) +".csv"
    if os.path.isfile(filename):
#        print(stock, "file exists")
        try:
            df = pd.read_csv(filename, sep=',') 
        
            record_date = datetime.datetime.strptime(df['Date'].iloc[-1], '%Y-%m-%d')
            
            if record_date.date() == (datetime.date.today() - datetime.timedelta(1)):
                
                # since the file is up to date. We need to do nothing
                print (stock, "file is up to date. Skipping")
            else:
                
                start_t = (record_date + datetime.timedelta(days=1)).date()
                df_new = GetYahooData(StockCode(stock), sd=start_t, ed=yesterday)
                df_new['DateTime'] = pd.to_datetime(df_new['Date'])
                df_new = df_new[(df_new['DateTime'].dt.date >= start_t) & (df_new['DateTime'].dt.date < end) ]

#                print("df_new", start_t)
#                print(df_new)
#                sys.exit()
                if len(df_new) > 0:
                    df_new = df_new.drop(['DateTime'], axis=1)
                    if isinstance(df_new, pd.DataFrame):
                        with open(filename, 'a') as f:
                            df_new.to_csv(f, header=False, sep=',', index=False)
                        print(stock, 'file exists. update %d lines'% len(df_new))
                    else:
                        print(stock, "file exists. df no update")
                else:
                    print(stock, "file exists. df no update")
        except Exception as e:
            print (stock, "file exists. Error catched", e)
            pass
    else:
        print(stock, "file not exist. Getting from Yahoo")
        df = GetYahooData(StockCode(stock), sd=start, ed=yesterday)
        if isinstance(df, pd.DataFrame):
            df.to_csv(filename, sep=',', index=False)

if __name__ == "__main__":
    df_allstock=pd.DataFrame.from_csv(allstockfilename)
    
    count = 0
#    for stock in df_allstock.index:
#
#        if count == 100:
#            break
#        print(stock)
#        count += 1
#        load_one_stock(stock)
#        remove_empty_lines(stock)
    
    load_one_stock(8350)
    remove_empty_lines(8350)