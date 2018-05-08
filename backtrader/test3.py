# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 23:06:48 2018

@author: user
"""

from stock_hsi_diff_sqn import Stock_Hsi_Diff_Sqn
from datetime import date

if __name__ == "__main__":

    stock_list=["0005.HK","0006.HK", "0027.HK","0066.HK","0700.HK","0799.HK","2318.HK"]
    startdate=date(2017,1,1)
    
    for stock in stock_list:
        Stock_Hsi_Diff_Sqn(stock, startdate, period=20)