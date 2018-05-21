# -*- coding: utf-8 -*-
"""
Created on Mon May 21 15:30:26 2018



@author: user
"""

from Lib_SP_Min import get_file_list, read_df



filelist = get_file_list("Z:\\")

for file in filelist:
    df = read_df(file)
    if (df.empty == False):         # df is empty if it is not valid
        print(file, df.shape)
        df.columns=['datetime','open','high','low','close','volume']