# -*- coding: utf-8 -*-
"""
Created on Mon May 21 15:31:49 2018

Process SP Min Files

@author: user
"""
import os
from pandas import read_csv
import pandas as pd

root_path="Z:\\2018\\2"
min_file_list=[]
df_size_min=100         # if min_file size is too small, it is ignored

# return a list of valid minute file for the path given
def get_file_list(path=root_path):
    for root, directories, filenames in os.walk(path):
    #    for directory in directories:
    #        print (os.path.join(root, directory) )
        for filename in filenames: 
            min_file_list.append(os.path.join(root,filename))      
    
    min_files = [i for i in min_file_list if 'one_min' in i]   # Sort so only filename with one_min are included
    
    print("Number of minute files: ", len(min_files))
    
    return min_files

# read a sp min data file and return a dataframe
# return empty dataframe if the size of the file is too small < df_size_min
def read_df(file):
    if is_non_zero_file(file):
        df = read_csv(file, header=None,  delimiter=';', engine='python')
        if (df.shape[0] > df_size_min):
            return df
        else:
           return pd.DataFrame({'A' : []}) 
    else:
        return pd.DataFrame({'A' : []})
    

# check if the file is empty
def is_non_zero_file(fpath):  
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False



if __name__ == "__main__":
    filelist = get_file_list()
    print(filelist)