# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 15:49:43 2018

@author: user
"""

import pandas as pd
import sys, getopt

d1=20180502
d2=20180702

if __name__ == '__main__':
    argv = sys.argv[1:]
    
    try:
        opts, args = getopt.getopt(argv,"hs:e:")
    except getopt.GetoptError:
        print('test.py -s <startdate> -e <enddate>')
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -s <startdate> -e <enddate>')
            sys.exit()
        elif opt == '-s':
            d1 = arg
        elif opt == '-e':
            d2 = arg
        else:
             print('test.py -s <startdate> -e <enddate>')
             sys.exit()
            
    
    print ('d1 is ', d1)
    print ('d2 is ', d2)
  



