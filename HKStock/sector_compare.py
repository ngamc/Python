import pandas as pd
import csv
import io
from  datetime import  date
import time
import requests
import matplotlib.pyplot as plt
import numpy as np
from getyahoodata import GetYahooDataFromFile, CodeToNum, GetYahooData, StockCode
import sys

plot_graph = True
cookiesB = dict(B='foovk4hcji2u4&b=3&s=7b')
crumb="SgSOFMkgfgO"

start=date(2019,1,1)
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
#print(df_id_to_list)
##df_id_to_list.set_index('ID')

with open('..\\configs\\stocklist.ini', 'r') as f:
  reader = csv.reader(f)
  list_stock = list(reader)

for i in range(len(list_stock)):
    print (list_stock[i][0], 'has', list_stock[i][1:])

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

#def getYahooData(id):
#    print('Getting',id)
##    url = 'https://query1.finance.yahoo.com/v7/finance/download/'+str(id[1:])+'.HK?period1='+str(timestamp_start)+'&period2='+str(timestamp_end).split('.')[0]+'&interval=1d&events=history&crumb=ucSAmXZjrNg'
#    url = 'https://query1.finance.yahoo.com/v7/finance/download/'+str(id[1:])+'.HK?period1='+str(timestamp_start)+'&period2='+str(timestamp_end).split('.')[0]+'&interval=1d&events=history&crumb='+crumb
#    #print(url)
#    #cookiesB = dict(B='foovk4hcji2u4&b=3&s=7b')
#    
#    try:
#        urlData=requests.get(url, cookies=cookiesB).content
#        df=pd.read_csv(io.StringIO(urlData.decode('utf-8')))
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
##        print(df)
#        return df
#    except Exception as e:
#        print(e)
#        print ('Skipping',id)
#        raise
        
def parsedf(df, id):
    try:
        df.set_index('Date', inplace=True)
        df=df[['Adj Close']]

        df.replace('null',np.nan,inplace=True)
        df.replace('0.000000',np.nan, inplace=True)
        df.fillna(method='ffill',inplace=True)
        df=df.astype(float)
         
        df['pctchange']=(df['Adj Close']-df['Adj Close'][0])/df['Adj Close'][0]*100.0
        df=df[['pctchange']]
        df.columns=[df_id_to_list.loc[int(str(id).lstrip('0'))]['Name']]
        return df
    except Exception as e:
        print(e)
        print ('Skipping',id)
#        sys.exit()
#        raise

def get_sector_data(sector_id=0):
    stocks=list_stock[sector_id][1:]
    
    main_df=pd.DataFrame()

    for eachstock in stocks:
        if eachstock == '-':
            pass
        else:
            try:
#                df = getYahooData(eachstock)       # calling local getYahooData function; depreciated
#                df = GetYahooData(StockCode(eachstock))     # Calling external getyahoodata function
                df = GetYahooDataFromFile(CodeToNum(eachstock))    # calling getyahoodata from file
                if not isinstance(df, pd.DataFrame):
                    raise Exception('Unexpected data size')
                df = parsedf(df, eachstock)
                if not isinstance(df, pd.DataFrame):
                    raise Exception('Unexpected data size')
#                print(df)
#                sys.exit()
                if main_df.empty:
                    main_df=df
                else:
                    main_df=main_df.join(df)
#                print(df)
            except Exception as e:
                print('Error: passing', eachstock, e)
#                print(df)
#                sys.exit()
                pass

    main_df.replace('null',np.nan,inplace=True)
    main_df.replace('0.000000',np.nan, inplace=True)
    main_df.fillna(method='ffill',inplace=True)
    main_df.fillna(method='bfill',inplace=True)
    rowcount=len(main_df.columns)
    main_df['mean']=main_df.mean(axis=1)
    main_df['std']=main_df.iloc[:,:-1].std(axis=1)
    df_mean=main_df[['mean']]
    df_std=main_df[['std']]
##    print (df_mean)
##    time.sleep(15)
    return df_mean, df_std, rowcount        

if __name__ == '__main__':
    
    
    df_all_mean=pd.DataFrame()
    df_all_std=pd.DataFrame()
#    all_row=[]
    
    for i in range(len(list_stock)):    # max 28
        if i>(len(list_stock)-1):
            print('Error: We do not have sector （%d）. Skipping'%(i))
        else:
            print('===== Starting sector',i,' (' , list_stock[i][0],') =====')
        ##    time.sleep(1)
            df_mean, df_std, rowcount = get_sector_data(i)
        ##    print(df_mean.head())
        ##    time.sleep(3)
            df_mean.columns=[list_stock[i][0]]
            df_std.columns=[list_stock[i][0]]
#            all_row.append(rowcount)
            if df_all_mean.empty:
                df_all_mean=df_mean
                df_all_std=df_std
            else:
                df_all_mean=df_all_mean.join(df_mean)
                df_all_std=df_all_std.join(df_std)
#        print(df_all_mean)
    
    #print(df_all_mean)
    print ("----------")
    df_all_mean_sorted = df_all_mean.sort_values(df_all_mean.last_valid_index(), axis=1, ascending=False)
    #print(df_all_mean_sorted)
    for name in df_all_mean_sorted.columns.values:
        print(name)
    
    
    if plot_graph == True:
    #    if df_all_mean.shape[1] < 11:       # if total 10 or less
    #        print("   === First choice ===")
    #        ax1 = plt.subplot2grid((1,1), (0,0))
    #        df_all_mean.plot(ax=ax1)
    #        plt.title('Compare HK Sectors')
    #        plt.show()
    #    
    #        ax2 = plt.subplot2grid((1,1), (0,0))
    #        df_all_std.plot(ax=ax2)
    #        plt.title('Compare HK Sectors (deviation)')
    #        plt.show()
    #    elif df_all_mean.shape[1] <21:     # if total 20 or less
    #        print("   === Second choice ===")
    #        ax1 = plt.subplot2grid((1,1), (0,0))             
    #        df_all_mean.iloc[:,0:10].plot(ax=ax1)
    #        df_all_mean.iloc[:,10:].plot(ax=ax1, ls=':')
    #        plt.title('Compare HK Sectors')
    #        plt.show()
    #        
    #        ax2 = plt.subplot2grid((1,1), (0,0))
    #        df_all_std.iloc[:,0:10].plot(ax=ax2)
    #        df_all_std.iloc[:,10:].plot(ax=ax2, ls=':')
    #        plt.title('Compare HK Sectors (deviation)')
    #        plt.show()
    #    else:
    #        print("   === Third choice ===")
        ax1 = plt.subplot2grid((1,1), (0,0))             
        df_all_mean_sorted.iloc[:,0:10].plot(ax=ax1, figsize=(15, 10))
    #        df_all_mean.iloc[:,10:20].plot(ax=ax1, ls='--')
    #        df_all_mean.iloc[:,20:].plot(ax=ax1, ls=':')
        plt.title('Compare HK Sectors')
        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=10)
        plt.show()
         
    #    ax2 = plt.subplot2grid((1,1), (0,0))
    #    df_all_std.iloc[:,0:10].plot(ax=ax2, figsize=(15, 10))
    ##        df_all_std.iloc[:,10:20].plot(ax=ax2, ls='--')
    ##        df_all_std.iloc[:,20:].plot(ax=ax2, ls=':')
    #    plt.title('Compare HK Sectors (deviation)')
    #    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=10)
    #    plt.show()
