# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 13:39:52 2018


@author: user
"""

import datetime
import pandas as pd
import pytz


product="HSI"
thisyear=datetime.datetime.today().year
thismonth=datetime.datetime.today().month
thisday=datetime.datetime.today().day


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
        
    return "P:\\" + product + "\\" + y  +"\\" + m + "\\" + y + "-" + m + "-" + d + "-one_min.txt"

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
        
    return "P:\\" + product + "\\" + y  +"\\" + m + "\\" + y + "-" + m + "-" + d + "-tkr.txt"

def Read_SP_Min_File(filepath=None):
    if filepath is None:
        filepath=File_Path_Min(year=thisyear, month=thismonth, day=thisday)
    df_file=pd.read_csv(filepath, sep=";", header=None)   # read ID to Name list
    df_file[0]=pd.to_datetime(df_file[0], format="%Y/%m/%d/%H/%M/%S")
    df_file.columns=['DateTime','Open','High','Low','Close', 'Volume']
    df_file['DateTime'] = df_file['DateTime'].astype(str)  # Convert timestamp to string
    return df_file

def Read_SP_Min_File_No_LastNight(filepath=None):
    if filepath is None:
        filepath=File_Path_Min(year=thisyear, month=thismonth, day=thisday)
    df_file=pd.read_csv(filepath, sep=";", header=None)   # read ID to Name list
    df_file[0]=pd.to_datetime(df_file[0], format="%Y/%m/%d/%H/%M/%S")
    df_file.columns=['DateTime','Open','High','Low','Close', 'Volume']
    df_file=Remove_Last_Night(df_file)
    df_file['DateTime'] = df_file['DateTime'].astype(str)  # Convert timestamp to string
    return df_file


# return close and volume columns and datetime as index
def Read_SP_Ticker(filepath=None):
    if filepath is None:
        filepath=File_Path_Ticker(year=thisyear, month=thismonth, day=thisday)
        
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
        y=year
    else:
        y=thisyear
    
    if month:
        m=month
    else:
        m=thismonth
    
    if day:
        d=day
    else:
        d=thisday
        
    df=df[df['DateTime']>datetime.datetime(y,m,d,5,10,0)]
    return df
    
if __name__ == "__main__":
#    df=Read_SP_Min_File()
    df=Read_SP_Ticker_2()
    print(df)
    
  

