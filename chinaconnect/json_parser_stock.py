# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 09:48:37 2018

@author: user
"""

import urllib.request, json 
import codecs
import datetime
import glob
import sys
import ntpath
import os

dirChina = 'D:\\user\\Documents\\Python\\chinaconnect\\'
dirHK = 'D:\\user\\Documents\\Python\\hkconnect\\'

today_year = ""
today_month = "05"
today_day = "29"



def get_list(num, raw_data):
    str_data = ''
    for i in range(10):
        x = json.loads(raw_data)[num]['content'][1]['table']['tr'][i]['td'][0]
        str_data = str_data + "%s %s %s %s %s %s \r\n" % (x[0], x[1], x[2], x[3], x[4], x[5])
    return str_data

def do_work_on_day(year, month, day):
    urllink="http://www.hkex.com.hk/chi/csm/DailyStat/data_tab_daily_%s%s%sc.js"%(year, month, day)
    try:
        with urllib.request.urlopen(urllink) as url:
            
            raw_data = url.read().decode()
            raw_data = raw_data[10:]
            raw_data = raw_data.replace('\u3000','')
        
            china0 = get_list(0, raw_data)
            china1 = get_list(2, raw_data)
            china = china0 + "\r\n" + china1
#            print(china)
        
            with codecs.open(dirChina+'%s%s%s.txt'%(year, month, day), 'w', 'utf-8') as file:
                file.write(china)
                
            hk0 = get_list(1, raw_data)
            hk1 = get_list(3, raw_data)
            hk = hk0 + "\r\n" + hk1
#            print(hk)
        
            with codecs.open(dirHK+'%s%s%s.txt'%(year, month, day), 'w', 'utf-8') as file:
                file.write(hk)
    
            print('%s-%s-%s saved'%(year, month, day))    
    except:
        print('Skipping %s-%s-%s'%(year, month, day)) 

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

if __name__ == '__main__':
    if today_year =="":
        today = datetime.datetime.today()
        today_year = today.strftime('%Y')
        today_month = today.strftime('%m')
        today_day = today.strftime('%d')
    
#        print(today.strftime('%Y - %m - %d'))
    
    # we collect filename from both China and Hong Kong
    # we then compare which one is less updated and we will pick that one
    filenames_c=glob.glob('D:\\user\\Documents\\Python\\chinaconnect\\*.txt')
    filenames_c.sort(key=os.path.basename)
    record_year_c = path_leaf(filenames_c[-1]).replace('.txt', '')[0:4]
    record_month_c = path_leaf(filenames_c[-1]).replace('.txt', '')[4:6]
    record_day_c = path_leaf(filenames_c[-1]).replace('.txt', '')[6:8]
    
    filenames_h=glob.glob('D:\\user\\Documents\\Python\\hkconnect\\*.txt')
    filenames_h.sort(key=os.path.basename)
    record_year_h = path_leaf(filenames_h[-1]).replace('.txt', '')[0:4]
    record_month_h = path_leaf(filenames_h[-1]).replace('.txt', '')[4:6]
    record_day_h = path_leaf(filenames_h[-1]).replace('.txt', '')[6:8]
    
    
    if (int(record_year_c)< int(record_year_h)):
        record_year = record_year_c
        record_month = record_month_c
        record_day = record_day_c
    elif (int(record_year_c)> int(record_year_h)):
        record_year = record_year_h
        record_month = record_month_h
        record_day = record_day_h
    elif int(record_month_c) < int(record_month_h):
        record_year = record_year_c
        record_month = record_month_c
        record_day = record_day_c
    elif int(record_month_c) > int(record_month_h):  
        record_year = record_year_h
        record_month = record_month_h
        record_day = record_day_h
    elif int(record_day_c)< int(record_day_h):
        record_year = record_year_c
        record_month = record_month_c
        record_day = record_day_c
    else:
        record_year = record_year_h
        record_month = record_month_h
        record_day = record_day_h
        
    print ("Last record in directoy is: %s-%s-%s"% (record_year, record_month, record_day))
    
    start_date = datetime.date(int(record_year), int(record_month), int(record_day))
    end_date = datetime.date(int(today_year), int(today_month), int(today_day))
    if (start_date < end_date):
        delta = end_date - start_date
        for i in range(1, delta.days):
            eachday = start_date + datetime.timedelta(i)
            do_work_on_day(eachday.strftime('%Y'), eachday.strftime('%m'), eachday.strftime('%d'))
        print("Done")
    else:
        print("Intended finish date:", end_date)
        print("Nothing need to do")



