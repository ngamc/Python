# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 17:22:32 2018

@author: user
"""

import pandas as pd
import csv
import io
from  datetime import date
import time
import requests
import matplotlib.pyplot as plt
import numpy as np

allstocklistfile = "..\\configs\\allstocklist.csv"
stocklistinifile = "..\\configs\\stocklist.ini"

df_id_to_list=pd.DataFrame.from_csv(allstocklistfile)

#print(df_id_to_list)

with open(stocklistinifile, 'r') as f:   # read sector and member list
  reader = csv.reader(f)
  list_stock = list(reader)
  print(list_stock)