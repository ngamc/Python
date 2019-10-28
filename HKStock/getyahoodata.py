# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 08:37:54 2018

@author: user
"""

import pandas as pd
import io
from  datetime import  date
import requests
import backtrader.feeds as btfeeds
from dateutil import parser
from backtrader import date2num
import datetime
import warnings
import backtrader as bt
import os
import sys

plot_graph = True
cookiesB = dict(B='foovk4hcji2u4&b=3&s=7b')
crumb="SgSOFMkgfgO"
yahoofilepath = 'D:\\user\\Documents\\Python\\Ignore\\yahoo\\'


start=date(2018,3,1)
DAY = 24*60*60                      # POSIX day in seconds (exact value)

end=datetime.date.today()

warnings.simplefilter(action='ignore', category=FutureWarning)

# imput a number e.g. 27 and output 0027.HK
def StockCode(id):
    if isinstance(id, int):
        sid = str(id)
    else:
        sid = id
    if len(sid) > 4:
        sid = sid[-4:]
    return sid.zfill(4)+".HK" 

# input stock code and return a number e.g. input 0027.HK and return 27
def CodeToNum(code):
    return (str(code).lstrip('0').rstrip('.HK'))
    
    
def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

def GetYahooData(id, sd=start, ed=end):
    timestamp_start = (sd - date(1970, 1, 1)).days * DAY
    timestamp_end = (ed - date(1970, 1, 1)).days * DAY 
#    print('Getting',id)
#    url = 'https://query1.finance.yahoo.com/v7/finance/download/'+str(id[1:])+'.HK?period1='+str(timestamp_start)+'&period2='+str(timestamp_end).split('.')[0]+'&interval=1d&events=history&crumb='+crumb

    url = 'https://query1.finance.yahoo.com/v7/finance/download/'+str(id)+'?period1='+str(timestamp_start)+'&period2='+str(timestamp_end).split('.')[0]+'&interval=1d&events=history&crumb='+crumb
#    print(url)

    try:
        urlData=requests.get(url, cookies=cookiesB).content
        df=pd.read_csv(io.StringIO(urlData.decode('utf-8')))
        

#        df.set_index('Date', inplace=True)
#        df=df[['Adj Close']]
#        df.replace('null',np.nan,inplace=True)
#        df.replace('0.000000',np.nan, inplace=True)
#        df.fillna(method='ffill',inplace=True)
###        if id=='02800':
###            print_full(df)
#         
###        df=df[~df['Adj Close'].isin(['null'])]          # remove null rows
###        df=df[~df['Adj Close'].isin(['0.000000'])]
#        df=df.astype(float)
#          
#        df['pctchange']=(df['Adj Close']-df['Adj Close'][0])/df['Adj Close'][0]*100.0
#        df=df[['pctchange']]
#        df.columns=[df_id_to_list.loc[int(str(id).lstrip('0'))]['Name']]
#        

        try:
            df=df[df.Close != 'null']
        except:
            pass
        
#        print(df)
        df[['Open','High','Low','Close','Adj Close','Volume']] = df[['Open','High','Low','Close','Adj Close','Volume']].apply(pd.to_numeric)  # Convert string to numeric
        df = df.reset_index(drop=True)
#        print(df)
        return df
    except Exception as e:
#        print(e)
        print ('Skipping',id)
#        raise

# id is e.g. 1, 27, 700
def GetYahooDataFromFile(id, sd=start, ed=end):
    if id[-2:] == 'HK':
        id = CodeToNum(id)
    filename = yahoofilepath + str(id) +".csv"
    print(filename)
    if os.path.isfile(filename):        
        try:
            
            df = pd.read_csv(filename, sep=',') 
            print(df)
            df['Date'] = pd.to_datetime(df['Date'])
            print(df)
            df = df[(df['Date'].dt.date >= sd) & (df['Date'].dt.date <= ed)]
            return df

        except:
            print ("Skipping", id)
            pass

# MyPandaData can be used by reading yahoo data feed 
class MyPandasData(btfeeds.PandasData):
    params = (
       # ('fromdate', datetime.datetime(2000, 1, 1)),
       # ('todate', datetime.datetime(2000, 12, 31)),
       # ('nullvalue', 0.0),
        ('dtformat', ('%Y-%m-%d')),
       # ('tmformat', ('%H.%M.%S')),
    
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close',4),   # use this for real close
#        ('close', 5),   # use this for adj close
        ('volume', 6),
        ('openinterest', None),
        
    )

    def _load(self):
        self._idx += 1

        if self._idx >= len(self.p.dataname):
            # exhausted all rows
            return False

        # Set the standard datafields
        for datafield in self.getlinealiases():
            if datafield == 'datetime':
                continue

            colindex = self._colmapping[datafield]
            if colindex is None:
                # datafield signaled as missing in the stream: skip it
                continue

            # get the line to be set
            line = getattr(self.lines, datafield)
#            print(self.lines)
#            print(datafield)
#            print(line)
#            print(self._idx)
#            print(colindex)
#            print(self.p.dataname)
#            a=(self.p.dataname.iloc[0,5])
#            print(a)

            # indexing for pandas: 1st is colum, then row
            if (type(self.p.dataname.iloc[self._idx, colindex]).__name__=='str'):
#                print("str", self.p.dataname.iloc[self._idx, colindex] )
                if (self.p.dataname.iloc[self._idx, colindex]=='null'):
#                    continue
                    line[0] = 0
                
                else:
                    line[0] = float(self.p.dataname.iloc[self._idx, colindex])
            else:
#                print("Not str", type(self.p.dataname.iloc[self._idx, colindex]))
                line[0] = self.p.dataname.iloc[self._idx, colindex]

        # datetime conversion
        coldtime = self._colmapping['datetime']

        if coldtime is None:
            # standard index in the datetime
            tstamp = self.p.dataname.index[self._idx]
        else:
            # it's in a different column ... use standard column index
            tstamp = self.p.dataname.iloc[self._idx, coldtime]


        dt = parser.parse(tstamp)
        
        dtnum = date2num(dt)
        self.lines.datetime[0] = dtnum

        # Done ... return
        return True

    
# After reading SP min data use this function to convert
class SPPandasData(btfeeds.PandasData):
    params = (
       # ('fromdate', datetime.datetime(2000, 1, 1)),
       # ('todate', datetime.datetime(2000, 12, 31)),
       # ('nullvalue', 0.0),
        ('dtformat', ('%Y-%m-%d %H:%M:%S')),
       # ('tmformat', ('%H.%M.%S')),
    
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close',4),   # use this for real close
#        ('close', 5),   # use this for adj close
        ('volume', 5),
        ('openinterest', None),
        ('timeframe', bt.TimeFrame.Minutes)
    )


    def _load(self):
        self._idx += 1

        if self._idx >= len(self.p.dataname):
            # exhausted all rows
            return False

        # Set the standard datafields
        for datafield in self.getlinealiases():
            if datafield == 'datetime':
                continue

            colindex = self._colmapping[datafield]
            if colindex is None:
                # datafield signaled as missing in the stream: skip it
                continue

            # get the line to be set
            line = getattr(self.lines, datafield)
#            print(self.lines)
#            print(datafield)
#            print(line)
#            print(self._idx)
#            print(colindex)
#            print(self.p.dataname)
#            a=(self.p.dataname.iloc[0,5])
#            print(a)

            # indexing for pandas: 1st is colum, then row
            if (type(self.p.dataname.iloc[self._idx, colindex]).__name__=='str'):
#                print("str", self.p.dataname.iloc[self._idx, colindex] )
                if (self.p.dataname.iloc[self._idx, colindex]=='null'):
#                    continue
                    line[0] = 0
                
                else:
                    line[0] = float(self.p.dataname.iloc[self._idx, colindex])
            else:
#                print("Not str", type(self.p.dataname.iloc[self._idx, colindex]))
                line[0] = self.p.dataname.iloc[self._idx, colindex]

        # datetime conversion
        coldtime = self._colmapping['datetime']

        if coldtime is None:
            # standard index in the datetime
            tstamp = self.p.dataname.index[self._idx]
        else:
            # it's in a different column ... use standard column index
            tstamp = self.p.dataname.iloc[self._idx, coldtime]


        dt = parser.parse(tstamp)
        
        dtnum = date2num(dt)
        self.lines.datetime[0] = dtnum

        # Done ... return
        return True 
        
if __name__=='__main__':
#    print("\r\n\r\n     ==== Testing with stock 00700 ====\r\n")
    df=pd.DataFrame()
    df=GetYahooDataFromFile('0001.HK', date(2018,6,1), date(2018,6,4))
    print(df)