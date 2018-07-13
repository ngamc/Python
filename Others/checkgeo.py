# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 08:46:06 2018
This problem is aimed to fulfilled SFC's guidline:
    1.2: Implement monitoring and surveillance mechanisms

Program parameters:
    -b: number of days to day back. Default is 0
    -d: number of days to compare. Default is 90

By default, program will read <-d> number of days user log, since the day before yesterday
It will form a unsorted database (df_db) that each user's log-in location during the last 90 days (since 2 days ago)
It then read in yesterday's log file (action log file)and filtered with safe country list (country_safe) and then compare 
with the df_db. If there is record that does not exist before, it will list out

The IP Geo database file is provided by IP2location: https://lite.ip2location.com using its
IP-COUNTRY-REGION-CITY database and can be downloaded for free

SP Log file should be in /mnt/
@author: Nelson Cheung
"""

import ipaddress
import pandas as pd
import IP2Location
import re
from datetime import date, datetime, timedelta
import os
import sys, getopt

backday = 0
daycompare = 90
country_safe = [b'-', b'Hong Kong', b'China']

tmpfile = '/tmp/checkgeo.tmp'

file = 'D:\\IP2LOCATION-LITE-DB3.CSV'

# change IP address to a long integer for comparisions
def dot2LongIP(ip):
	return int(ipaddress.IPv4Address(ip))

def printhelp():
    print('checkgeo.py -b <num of days> -d <num of days>')
    print('-b: number of days to day back. Default 0')
    print('-d: number of days to compare. Default 90')

if __name__ == '__main__':
    argv = sys.argv[1:]
    
    try:
        opts, args = getopt.getopt(argv,"hb:d:")
    except getopt.GetoptError:
        printhelp()
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            printhelp()
            sys.exit()
        elif opt == '-b':
            backday = int(arg)
        elif opt == '-d':
            daycompare = int(arg)
        else:
             printhelp()
             sys.exit()

    # action day is the date we want to compare with previous days
    # this is usually yesterday because we haven't have today's record
    # that's why we add +1 in backday
    actionday = datetime.now().date() - timedelta(days=backday+1)
    
    IP2LocObj = IP2Location.IP2Location();
    IP2LocObj.open('IP2LOCATION-LITE-DB3.BIN')

    rows=[]
    for i in range(1, daycompare + 1):
        
        datetime = actionday - timedelta(i)
        yy = datetime.strftime('%Y')
        mm = datetime.strftime('%m')
        dd = datetime.strftime('%d')
        
        sp_log = '/mnt/user_log_'+str(datetime)+'.csv'
        print(sp_log)
#        sys.exit()
        os.system("grep ClientIP " + sp_log + "|grep RetCode=0 >" + tmpfile)
    
        try:    
            df = pd.read_csv(tmpfile, header=None, encoding = "ISO-8859-1", names =['datetime', 'user','account', 'content', 'nouse'])
        except:
            print('skipping ', sp_log)
            continue
    
        for row in df.itertuples(index=True, name='Pandas'):
            
            try:
                content = getattr(row, "content")
                ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}', content )        #find all ip and into a list
                for ip in ips:
    
                    ip2 = ipaddress.ip_address(ip)
                    if (ip2 in ipaddress.ip_network('192.168.0.0/16')) or (ip2 in ipaddress.ip_network('10.0.0.0/8')):
                        pass
                    else:
        
        
                        rec = IP2LocObj.get_all(ip)
                        if (rec.country_short != b'-'):
                            row1 = [datetime,getattr(row, "user"),ip,rec.country_long,rec.region ]
                            rows.append(row1)
            except:
                continue
            
    # df_db is the final db we use to compare with today record
    df_db = pd.DataFrame(rows, columns=['datetime','user','ip','country','region'])
#    print(df_db)
    
    print('='*30)
    
    # read in the action log file. This is usually yesterday's log file
    sp_log = '/mnt/user_log_'+str(actionday)+'.csv'
    print('Loading inspection file', sp_log)
    os.system("grep ClientIP " + sp_log + "|grep RetCode=0 >" + tmpfile)
    df_action = pd.read_csv(tmpfile, header=None, encoding = "ISO-8859-1", names =['datetime', 'user','account', 'content', 'nouse'])
    
    num_result = 0
    print('Comparing...')
    for row in df_action.itertuples(index=True, name='Pandas'):
        
        try:
            content = getattr(row, "content")
            ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}', content )        #find all ip and into a list
            for ip in ips:

                ip2 = ipaddress.ip_address(ip)
                if (ip2 in ipaddress.ip_network('192.168.0.0/16')) or (ip2 in ipaddress.ip_network('10.0.0.0/8')):
                    pass
                else:
                    rec = IP2LocObj.get_all(ip)
                    if rec.country_long in country_safe:
                        pass
                    # We will inspect IPs one by one with the df_db now
                    else:
#                        print(rec.country_long)
                        df_tmp = df_db.loc[df_db.user == getattr(row, "user") ]
                        df_result = df_tmp.loc[df_tmp.country == rec.country_long]
                        # if user has logged in before from same location, df_result should not be empty
                        if len(df_result) >0:
                            pass
                        else:
                            print('%s %s with IP: %s (%s)' % (getattr(row, "datetime"), getattr(row, "user") , ip, rec.country_long))
                            num_result+=1
        except:
            continue
    
    print('Totally: %d record(s) found' % num_result)