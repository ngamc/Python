# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 13:39:52 2018

Various method can be used to read SP's minute file or ticker file

@author: user
"""
import time
import datetime
import pandas as pd
import pytz
import sys


product="HSI"
path = 'P:\\' + product 
thisyear=datetime.datetime.today().year
thismonth=datetime.datetime.today().month
thisday=datetime.datetime.today().day
# break time is 1am - 9:15am and 4:30pm to 5:15pm
#breaktime = [[1*60*60, 9*60*60+15*60], [16*60*60+30*60, 17*60*60+15*60]]

def File_Path_Min(year="", month="", day=""):
    if year:
        y=str(year)
    else:
        y=str(thisyear)
    
    if month:
        m=str(month)
    else:
        m=str(thismonth)
    
    if day:
        d=str(day)
    else:
        d=str(thisday)
        
    return  path + "\\" + y  +"\\" + m + "\\" + y + "-" + m + "-" + d + "-one_min.txt"

def File_Path_Ticker(year="", month="", day=""):
    if year:
        y=str(year)
    else:
        y=str(thisyear)
    
    if month:
        m=str(month)
    else:
        m=str(thismonth)
    
    if day:
        d=str(day)
    else:
        d=str(thisday)
        
    return path + "\\" + y  +"\\" + m + "\\" + y + "-" + m + "-" + d + "-tkr.txt"

def Read_SP_Min_File(y='', m='', d=''):
    if y == "":
        filepath=File_Path_Min(year=thisyear, month=thismonth, day=thisday)
    else:
        filepath=File_Path_Min(year=y, month=m, day=d)
        
    df_file=pd.read_csv(filepath, sep=";", header=None)   # read ID to Name list
    df_file[0]=pd.to_datetime(df_file[0], format="%Y/%m/%d/%H/%M/%S")
    df_file.columns=['DateTime','Open','High','Low','Close', 'Volume']
    df_file['DateTime'] = df_file['DateTime'].astype(str)  # Convert timestamp to string
    return df_file

def Read_SP_Min_File_No_LastNight(y='', m='', d=''):
    if y == "":
        filepath=File_Path_Min(year=thisyear, month=thismonth, day=thisday)
    else:
        filepath=File_Path_Min(year=y, month=m, day=d)
        
    df_file=pd.read_csv(filepath, sep=";", header=None)   # read ID to Name list
    
    df_file[0]=pd.to_datetime(df_file[0], format="%Y/%m/%d/%H/%M/%S")
    df_file.columns=['DateTime','Open','High','Low','Close', 'Volume']
    if y=="":
        df_file=Remove_Last_Night(df_file)
    else:
        df_file=Remove_Last_Night(df_file, y, m, d)
    df_file['DateTime'] = df_file['DateTime'].astype(str)  # Convert timestamp to string
    return df_file

# Check if period is valid
# period has to be multiple of 5 seconds, 1 minutes, 5 minutes, 15 minutes, 30 minutes
# 1s, 5s, 10s, 15s, 30s, 1m, 5m, 10m, 15m, 30m, 1h
def valid_period(period):
    valid = ['1s', '5s', '10s', '15s', '30s', '1m', '5m', '10m', '15m', '30m', '1h' ]
    sec = [1, 5, 10, 15, 30, 60, 5*60, 10*60, 15*60, 30*60, 60*60]
    
    for i in range(len(valid)):
        if period == valid[i]:
            return sec[i]
    return None
  
# return close and volume columns and datetime as index
def Read_SP_Ticker(y='', m='', d=''):
    filepath=File_Path_Ticker(year=y, month=m, day=d)
        
    df_ticker=pd.DataFrame.from_csv(filepath, header=None)
    df_ticker.drop([1,4,5],inplace=True, axis=1)
#    print(df_ticker)
    
    df_ticker.columns=[['close', 'volume']]

    # remove duplicate entries
#    df_ticker=df_ticker[df_ticker.shift(1)!=df_ticker]
    
    df_ticker.dropna(inplace=True)
#    print('Number of rows >',df_ticker.shape[0])
#    print(df_ticker.head())
    df_ticker.index=pd.to_datetime(df_ticker.index, unit='s')
    tz = pytz.timezone('Asia/Shanghai')
    df_ticker.index=df_ticker.index.tz_localize('UTC').tz_convert(tz)
    return df_ticker

class ohlc():
    def __init__(self):
        self.count = 0
        self.open = 0
        self.high = 0
        self.low = 0
        self.close = 0 
        self.volume = 0
        
    def update(self, price, vol):
        if self.open == 0:
            self.open = price
        if price > self.high:
            self.high = price
        if self.low == 0 or price < self.low:
            self.low = price
        self.close = price
        self.volume +=vol
        self.count +=1
        
        

# return close and volume columns and datetime as index
# period e.g. 5s, 15m, 1h
# index: num or unixtime or datetime
def Read_SP_Ticker_Period(period='1m', y='', m='', d='', index='num'):
    # Check if period is valid
    p = valid_period(period)
    if p == None:
        return "Error: invalid period"
        
    filepath=File_Path_Ticker(year=y, month=m, day=d)
        
    df_ticker=pd.read_csv(filepath, header=None, )
    df_ticker.drop([1,4,5],inplace=True, axis=1)
    df_ticker.columns=[[ 'unixtime', 'close', 'volume']]
    
    s = '%s/%s/%s' %(m,d,y)
    start_ut= time.mktime(datetime.datetime.strptime(s, "%m/%d/%Y").timetuple())
    df_ticker.dropna(inplace=True)
#    print('Number of rows >',df_ticker.shape[0])
#    print(df_ticker.head())
    df_result = pd.DataFrame(columns=['unixtime', 'Open', 'High', 'Low', 'Close', 'Volume', 'TradeNum'])
    # 
    idx = 0   # this is the nth number of period since 00:00
    written = False
#    print(df_ticker)
#    sys.exit()
    
    for tickernum in range(len(df_ticker)):
        if tickernum == 0:
            obj = ohlc()
        if (df_ticker.iloc[tickernum, 0] < start_ut):
#        print(df_ticker['close'])
#        if df_ticker['unixtime'][tickernum] < start_ut:
            continue            # remove previous day records
        else:
            while True:
                if df_ticker.iloc[tickernum, 0] < start_ut+(idx+1)*p:
                    break
                else:
                    if written:
                        rdate = start_ut+idx*p
                        ropen = obj.open
                        rhigh = obj.high
                        rlow = obj.low
                        rclose = obj.close
                        rvolume = obj.volume
                        rcount = obj.count
                        df_result.loc[len(df_result)] = [rdate, ropen, rhigh, rlow, rclose, rvolume, rcount]
                        del obj
                        obj = ohlc()
                        written = False
                    idx +=1
                
#            if df_ticker.iloc[tickernum, 0] < start_ut+(idx+1)*p:
            obj.update(df_ticker.iloc[tickernum, 1], df_ticker.iloc[tickernum, 2])
            written = True
        if tickernum == (len(df_ticker) - 1):    # if this is the last ticker, we write last record
            rdate = start_ut+idx*p
            ropen = obj.open
            rhigh = obj.high
            rlow = obj.low
            rclose = obj.close
            rvolume = obj.volume
            rcount = obj.count
            df_result.loc[len(df_result)] = [rdate, ropen, rhigh, rlow, rclose, rvolume, rcount]
            del obj
                       
            
#        if tickernum > 200:
    df_result['DateTime'] = pd.to_datetime(df_result['unixtime'], unit='s') + pd.Timedelta('08:00:00')
#        
#    df_ticker.index=pd.to_datetime(df_ticker.index, unit='s')
#    tz = pytz.timezone('Asia/Shanghai')
#    df_ticker.index=df_ticker.index.tz_localize('UTC').tz_convert(tz)
    
    if index == 'unixtime':
        df_result = df_result.set_index('unixtime')
    elif index == 'datetime':
        df_result = df_result.set_index('DateTime')
        
    return df_result

# return indexmean, indexstd, diff and total volume columns, datetime as index
def Read_SP_Ticker_2(filepath=None):
    df_ticker=Read_SP_Ticker(filepath)
    print(df_ticker)
    
    eventdate=df_ticker.index[0]        # we need to get the year and month, maybe from first entry is good
    eventyear=eventdate.year
    eventmonth=eventdate.month
    eventday=eventdate.day
    
    market_start_hour=9
    market_end_hour=24
    df=pd.DataFrame(columns=['datetime', 'indexmean', 'indexstd', 'diff', 'volume'])
    
    df_selected=pd.DataFrame()
    for hour in range(market_start_hour, market_end_hour):
        for minute in range(0,60):
            df_selected=df_ticker[(df_ticker.index.hour==hour) & (df_ticker.index.minute==minute)]
            if df_selected.empty:
                pass
            else:
                pass
                df_selected['CxV']=df_selected['close'] * df_selected['volume']
                totalvolume=df_selected['volume'].sum()
                indexmean=df_selected['CxV'].sum()/totalvolume
                indexstd=df_selected['close'].std()
                max=df_selected['close'].max()
                min=df_selected['close'].min()
                
                df.loc[len(df.index)]=[datetime.datetime(eventyear, eventmonth, eventday, hour, minute),
                       indexmean, indexstd, (max-min), totalvolume]

    
    return(df)

# use with Minute df to remove last night's trade records
def Remove_Last_Night(df, year="", month="", day="" ):
    if year:
        y=int(year)
    else:
        y=thisyear
    
    if month:
        m=int(month)
    else:
        m=thismonth
    
    if day:
        d=int(day)
    else:
        d=thisday

    df=df[df['DateTime']>datetime.datetime(y,m,d,5,10,0)]
    return df
    
if __name__ == "__main__":
#    df=Read_SP_Min_File()
#    df=Read_SP_Ticker('2018','6','8')
    df = Read_SP_Ticker_Period('1m','2018','6','25', index='num')
#    df = Read_SP_Min_File_No_LastNight('2018','6','8')
    print(df)
    
  

