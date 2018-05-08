import pandas as pd
import csv
import io
from  datetime import date
import time
import requests
import matplotlib.pyplot as plt
import numpy as np
from stockstats import StockDataFrame as Sdf

plot_graph = True

start=date(2017,4,1)
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

df_id_to_list=pd.DataFrame.from_csv('D:\\allstocklist.csv')
print(df_id_to_list)
##df_id_to_list.set_index('ID')

with open('D:\\stocklist.ini', 'r') as f:
  reader = csv.reader(f)
  list_stock = list(reader)

##for i in range(len(list_stock)):
##    print (list_stock[i][0], 'has', list_stock[i][1:])

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

def getYahooData(id):
    print('Getting',id)
    url = 'https://query1.finance.yahoo.com/v7/finance/download/'+str(id[1:])+'.HK?period1='+str(timestamp_start)+'&period2='+str(timestamp_end).split('.')[0]+'&interval=1d&events=history&crumb=ucSAmXZjrNg'
    cookiesB = dict(B='foovk4hcji2u4&b=3&s=7b')

    try:
        urlData=requests.get(url, cookies=cookiesB).content
        df=pd.read_csv(io.StringIO(urlData.decode('utf-8')))
    ##    print(df)

        df.set_index('Date', inplace=True)
        df=df[['Adj Close']]
        df.replace('null',np.nan,inplace=True)
        df.replace('0.000000',np.nan, inplace=True)
        df.fillna(method='ffill',inplace=True)

        df=df.astype(float)
          
#        df['pctchange']=(df['Adj Close']-df['Adj Close'][0])/df['Adj Close'][0]*100.0
        df=df[['Adj Close']]
        df.columns=['close']
#        df.columns=[df_id_to_list.loc[int(str(id).lstrip('0'))]['Name']]   # set column name to stock name
        return df
    except Exception as e:
        print(e)
        print ('Skipping',id)
        raise

main_df=pd.DataFrame()
try:
    df = getYahooData('00005')

    main_df=df
    print (main_df.tail())
    stock = Sdf.retype(main_df)
    
#        stock2=stock.get_stock().within(20170101, 20170620)
    print('====== macd ==========')        
#    print(stock.get('rsi_6'))
    print('====== bollinger ==========')        
#        print(stock.get('boll_ub'))
#        print(stock.get('boll_lb'))
#        print(stock2['cr'].tail())
    print(stock.tail())

except Exception as e:
    pass
               
if plot_graph == True:
     ax1 = plt.subplot2grid((10,1), (0,0), rowspan=2)
     ax2 = plt.subplot2grid((10,1), (3,0), rowspan=7, sharex=ax1)
     stock['close'].plot(ax=ax1)
     stock[['rsi_14','rsi_41']].plot(ax=ax2)
     print(stock.tail())
#     main_df.iloc[:,:-1].plot(ax=ax1)
#     main_df.iloc[:,-1:].plot(color='k',ax=ax1, linewidth=3)
     plt.title('RSI')
     plt.show()
    


