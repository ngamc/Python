# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 16:34:03 2019

@author: user
"""
import fix_yahoo_finance as yf

msft = yf.Ticker("MSFT")

# get stock info
msft.info

# get historical market data
hist = msft.history(period="max")

# show actions (dividends, splits)
msft.actions

# show dividends
msft.dividends

# show splits
msft.splits

