import pandas as pd
import csv
import io
from  datetime import date
import time
import requests
import matplotlib.pyplot as plt
import numpy as np

plot_graph = True

start=date(2018,7,20)
DAY = 24*60*60                      # POSIX day in seconds (exact value)
timestamp_start = (start - date(1970, 1, 1)).days * DAY
timestamp_end = time.time()




##aa = pd.read_html('https://www.hkex.com.hk/eng/market/sec_tradinfo/stockcode/eisdeqty.htm')
##
##stocklist=aa[3][[0,1,2]]
##
##print(stocklist)
##stocklist.columns=['ID','Name','Lot']
##stocklist.drop(0,inplace=True)
##stocklist.set_index('ID',inplace=True)
##stocklist.to_csv('D:\\allstocklist.csv')
##print(stocklist)

df_id_to_list=pd.DataFrame.from_csv('D:\\allstocklist.csv') # read ID to Name list
#print(df_id_to_list)
##df_id_to_list.set_index('ID')


with open('D:\\stocklist.ini', 'r') as f:   # read sector and member list
  reader = csv.reader(f)
  list_stock = list(reader)

##for i in range(len(list_stock)):
##    print (list_stock[i][0], 'has', list_stock[i][1:])

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

def getYahooData(id):
#    print('Getting',id)
#    url = 'https://query1.finance.yahoo.com/v7/finance/download/'+str(id[1:])+'.HK?period1='+str(timestamp_start)+'&period2='+str(timestamp_end).split('.')[0]+'&interval=1d&events=history&crumb=ucSAmXZjrNg'
    #url = 'https://query1.finance.yahoo.com/v7/finance/download/'+str(id[1:])+'.HK?period1='+str(timestamp_start)+'&period2='+str(timestamp_end).split('.')[0]+'&interval=1d&events=history&crumb=m0XyDT8bLnH'
    url = 'https://query1.finance.yahoo.com/v7/finance/download/'+str(id[1:])+'.HK?period1='+str(timestamp_start)+'&period2='+str(timestamp_end).split('.')[0]+'&interval=1d&events=history&crumb=SgSOFMkgfgO'

    cookiesB = dict(B='foovk4hcji2u4&b=3&s=7b') 

    try:
        urlData=requests.get(url, cookies=cookiesB).content
        df=pd.read_csv(io.StringIO(urlData.decode('utf-8')),error_bad_lines=False)
#        print(df)

        df.set_index('Date', inplace=True)
        df=df[['Adj Close']]
        df.replace('null',np.nan,inplace=True)
        df.replace('0.000000',np.nan, inplace=True)
        df.fillna(method='ffill',inplace=True)
##        if id=='02800':
##            print_full(df)
         
##        df=df[~df['Adj Close'].isin(['null'])]          # remove null rows
##        df=df[~df['Adj Close'].isin(['0.000000'])]
        df=df.astype(float)
          
        df['pctchange']=(df['Adj Close']-df['Adj Close'][0])/df['Adj Close'][0]*100.0
        df=df[['pctchange']]
        df.columns=[df_id_to_list.loc[int(str(id).lstrip('0'))]['Name']]
        return df
    except Exception as e:
        print(e)
        print ('Skipping',id)
        raise

def print_sector(sector_id=0):
    stocks=list_stock[sector_id][1:]
    stocks.append('02800')

    main_df=pd.DataFrame()

    for eachstock in stocks:
        if eachstock == '-':
            pass
        else:
            try:
                df = getYahooData(eachstock)
                if main_df.empty:
                    main_df=df
                else:
                    main_df=main_df.join(df)
            except Exception as e:
                pass
               
    if plot_graph == True:
         ax1 = plt.subplot2grid((1,1), (0,0))
         main_df.index=pd.to_datetime(main_df.index)
         main_df.iloc[:,:-1].plot(ax=ax1)
         main_df.iloc[:,-1:].plot(color='k',ax=ax1, linewidth=3)
         ax1.legend(loc='upper left', bbox_to_anchor=(-0.1, -0.2), fancybox=True, shadow=True, ncol=main_df.shape[1])
         plt.title(list_stock[sector_id][0])
         plt.show()
    

for i in range(30):
    print('Starting sector',i)
    print_sector(i)
    
