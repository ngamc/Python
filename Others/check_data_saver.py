# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 10:34:53 2018
This program is to be run in the datasaver server to check if the ticker files are getting updated
If outdated ticker file is found, it will send out warning message to defined address for alert

@author: Nelson Cheung
"""

import time
from datetime import datetime
import pandas as pd
import sys
sys.path.append('D:\\user\\Documents\\Python\\')
from trial.email import sendm

# this is the root directory for all different products
folder = 'P:\\'

# timestamp offset from 00:00 e.g. 9.5 means 9.5 hours from start of the day
# it is the [start_time, end_time]
# program only check if now is within this period everyday
schedule = [9.5*3600, 23.9*3600]

# timestamp time.time() need to add this time offset
timezone = 8

# a list of product to check
products = ['HSI','HHI','CL','GC','6E']

# if a file is found number of seconds not updated, email alert is triggered
nsec_behind = 35*60

if __name__ == '__main__':
    nowT     = time.time() + timezone*3600     # we add 8 hours because we are gmt+8
    yearNow  = str(datetime.today().year)
    monthNow = str(datetime.today().month)
    dayNow   = str(datetime.today().day)
    offsetT  = int(nowT) % int(86400)       # offsetT is the timestamp now - timestamp of today at 00:00
    

    if offsetT > int(schedule[0]) & offsetT < int(schedule[1]):
        print("It is time to run. Time right now: %.2f" % (offsetT))        
        print(yearNow, monthNow, dayNow)        
        for product in products:
            path = folder+product +"\\"+yearNow+"\\"+monthNow+"\\"+yearNow+"-"+monthNow+"-"+dayNow+"-tkr.txt"
            print(path)         
            with open(path, 'r') as f:
                lines = f.read().splitlines()
                timestampinfile = lines[-1].split(',')[0]
                t = int(timestampinfile) % 86400 + timezone*3600
                if (t + nsec_behind) > offsetT:
                    print('Product %s is updated' % product)
                else:
                    subjtext = "Please check " + product
                    sendm(subject=subjtext, body="")
