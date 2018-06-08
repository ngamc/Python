# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 10:46:42 2018

@author: user
"""

from stock_sqn import sqn
import pandas as pd
from operator import itemgetter
from getyahoodata import StockCode

df_allstock=pd.DataFrame.from_csv('D:\\allstocklist.csv')

def all_stock_sqn():
    

    result = []
    count = 0
    for stock in df_allstock.index:
        print(stock)
#        if count == 67:
#            break
        count += 1
        stockcode = str(stock).zfill(4) + ".HK"
        sqn_result = sqn(stockcode, graph=False)
        if sqn_result != None:
            result.append([stock, float(sqn_result)])
    
#    sorted_result = sorted(result, key = lambda result: result[1])
    sorted_result = sorted(result, key=itemgetter(1), reverse=True)

    count=0
    for (ID, sqn_number) in sorted_result:
        if count==20:
            break;
        count += 1
        print(ID, df_allstock.loc[int(str(ID).lstrip('0'))]['Name'], sqn_number)
 
def some_stock_sqn():
    stock_list = [1, 5, 27, 66, 388, 700, 772, 799, 2318]
    result = []
    for stock in stock_list:
        sqn_result = sqn(StockCode(stock))
        if sqn_result != None:
            result.append([stock, float(sqn_result)])
    sorted_result = sorted(result, key=itemgetter(1), reverse=True)
    for (ID, sqn_number) in sorted_result:   
        print(ID, df_allstock.loc[int(str(ID).lstrip('0'))]['Name'], sqn_number)
        
        
if __name__ == "__main__":
#    all_stock_sqn()
    some_stock_sqn()

        

