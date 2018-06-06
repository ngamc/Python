# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:46:01 2018

@author: user
"""

import urllib.request, json 
import codecs
import datetime
import glob
import sys
import ntpath
import os

fileChina1 = 'D:\\user\\Documents\\Python\\chinaconnect\\stat\\shanghai_northbound.txt'
fileChina2 = 'D:\\user\\Documents\\Python\\chinaconnect\\stat\\shenzhen_northbound.txt'
fileHK1 = 'D:\\user\\Documents\\Python\\hkconnect\\stat\\shanghai_southbound.txt'
fileHK2 = 'D:\\user\\Documents\\Python\\hkconnect\\stat\\shenzhen_southbound.txt'

filelist = [fileChina1, fileHK1, fileChina2, fileHK2]

today_year = ""
today_month = "05"
today_day = "29"

#def get_list(num, raw_data):
#    str_data = ''
#    for i in range(10):
#        x = json.loads(raw_data)[num]['content'][1]['table']['tr'][i]['td'][0]
#        str_data = str_data + "%s %s %s %s %s %s \r\n" % (x[0], x[1], x[2], x[3], x[4], x[5])
#    return str_data

def get_stat_on_day(year, month, day, filename, num):
    urllink="http://www.hkex.com.hk/eng/csm/DailyStat/data_tab_daily_%s%s%se.js"%(year, month, day)
#    print(urllink)
    try:
        with urllib.request.urlopen(urllink) as url:
            
            raw_data = url.read().decode()
            raw_data = raw_data[10:]            # remove the trailing keyword from HKEx. It is useless to us
            raw_data = raw_data.replace('\u3000','')
            
            result = []
            if num == 0 or num == 2:
                for i in range(8):
                    item = json.loads(raw_data)[num]['content'][0]['table']['tr'][i]['td'][0][0]       
                    result.append(item)

                with codecs.open(filename, 'a', 'utf-8') as file:
                    file.write("%s-%s-%s %s %s %s %s %s %s %s %s\r\n"%(year, month, day, result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7]))
            else:
                for i in range(6):
                    item = json.loads(raw_data)[num]['content'][0]['table']['tr'][i]['td'][0][0]       
                    result.append(item)
                with codecs.open(filename, 'a', 'utf-8') as file:
                    file.write("%s-%s-%s %s %s %s %s %s %s\r\n"%(year, month, day, result[0], result[1], result[2], result[3], result[4], result[5]))
    
            print('%s-%s-%s saved'%(year, month, day))    
    except:
        print('Skipping %s-%s-%s'%(year, month, day)) 
        
        
def process_one_file(file, num, date, today_year):
    print(file, "last record was", date.strftime('%Y-%m-%d'))
    
    if today_year =="":
        today = datetime.datetime.today()
        today_year = today.strftime('%Y')
        today_month = today.strftime('%m')
        today_day = today.strftime('%d')
    
    start_date = date
    end_date = datetime.date(int(today_year), int(today_month), int(today_day))

    if (start_date < end_date):
        delta = end_date - start_date
        for i in range(1, delta.days):
            eachday = start_date + datetime.timedelta(i)
            print(eachday.strftime('%Y-%m-%d'))
            get_stat_on_day(eachday.strftime('%Y'), eachday.strftime('%m'), eachday.strftime('%d'), file, num)
        print("Done")
    else:
        print("Intended finish date:", end_date)
        print("Nothing need to do")
    


if __name__ == '__main__':  
    # We check four files and read the last line
    for num, file in enumerate(filelist):
        with open(file, 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            if last_line =="":
                last_line = lines[-2]
            date = datetime.datetime.strptime((last_line.split(" ")[0]), '%Y-%m-%d').date()
            process_one_file(file, num, date, today_year)


