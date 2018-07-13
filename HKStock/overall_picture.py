# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 17:13:39 2018

This will give you a whole picture of each day, so as to compare each day's charactistics
@author: user
"""

import pandas as pd
from read_sp import Read_SP_Ticker_Period, Read_SP_Min_File
import matplotlib.pyplot as plt
from datetime import date
import datetime
import sys
import os

path = "P:\\HSI\\"
start_date = date(2018,1,1)
end_date   = date(2018,6,14)
name_amfl = "all_min_file_list.txt"             # name of the all SP minute file list

def maybe_update_allminfilelist():
    if os.path.isfile(name_amfl):
        try:
            lines =[]
            with open(name_amfl, 'r') as f:
                lines = f.read().splitlines()
                last_line_num = -1
                last_line = lines[last_line_num]
                while True:
                    if last_line.strip() == "":
                        last_line_num = last_line_num -1
                        last_line = lines[last_line_num]
                    else:
                        break
   
            yy = last_line.split("\\")[-1].split("-")[0]
            mm = last_line.split("\\")[-1].split("-")[1]
            dd = last_line.split("\\")[-1].split("-")[2]
            
            y_today = datetime.datetime.now().year
            m_today = datetime.datetime.now().month
            d_today = datetime.datetime.now().day
            
            if int(yy)==y_today and int(mm)==m_today and int(dd)==d_today:
                print('All Min file list is up-to-date')
                new_lines = []
                for item in lines:
                    if item.strip() != "":
                        new_lines.append(item)

                return new_lines
        except:                 # if the file has strange format, we update it anyway
            print('File format error.')
            pass
        
    # if the file is missing or not-up-to-date, we will write a new one
    print("The Min file list is not up to date. Updating...")
    years = [2016, 2017, 2018]
    months = [ 1,2,3,4,5,6,7,8,9,10,11,12]
    days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
    allfilelist = []

    for y in years:
        for m in months:
            for d in days:
                filename=path+ str(y)+'\\'+str(m)+ '\\'+str(y)+'-'+str(m)+'-'+str(d)+'-one_min.txt'
                if os.path.isfile(filename):
                    allfilelist.append(filename)
                      
                  
    with open(name_amfl, 'w') as f:
        for item in allfilelist:
            f.write(item+"\r\n")   

    return allfilelist
 
# this will return the index of the file in the allfilelist
def getindex(afilelist, dd ):
    i = 0
    eachday=""
    idx = 0
    while True:
        try:
            eachday = dd + datetime.timedelta(i)
            if eachday > datetime.date.today():
                idx = len(afilelist)
                break;
            y1 = eachday.strftime('%Y')
            m1 = eachday.strftime('%m')
            d1 = eachday.strftime('%d')
#            print(y1,m1,d1.lstrip("0"))
            idx = afilelist.index(path+y1+"\\"+m1.lstrip('0')+"\\"+y1+"-"+m1.lstrip('0')+"-"+d1.lstrip("0")+"-one_min.txt")
#            print (idx)
            break;
        except:
            i +=1
    return idx

# retrieve a list of file that exists from start_date to end_date
def retrieve_file_list(afilelist, start_date, end_date):
    
    start_idx = getindex(afilelist, start_date)
    end_idx   = getindex(afilelist, end_date)
#    end_idx +=1
    
    if start_idx > end_idx:
        print ('Error: Start date is later than end date')
        sys.exit()
        
#    print (start_idx)
#    print(end_idx)
#    filefmt = eachday.strftime("%Y\\%m\\%Y-%m-%d-one_min.txt")
#    print(filefmt, idx_start)           
    
   
    list = []
    for i in range(start_idx, end_idx):
#        print(afilelist[i])
        list.append(afilelist[i])
    return list

def collect_stat(flist):
    df = pd.DataFrame(columns = ['DateTime', 'HLDiff', 'gainpct', 'Volume', 'Step', 'Wave', 'vow' , 'vowd'])
    
    close_list = []
    
    for file in flist:
        print(file)
        day_o = 0
        day_h = 0
        day_l = 888888
        day_c = 0
        day_v = 0
        step  = 0
        prev_min_close = 0
        with open(file, 'r') as f:
            lines = f.read().splitlines()
            if len(lines) < 300:
                continue
            # we choose line 5 to get the date because line 0 sometimes are wrong
            y = lines[5].split(';')[0].split('/')[0]
            m = lines[5].split(';')[0].split('/')[1]
            d = lines[5].split(';')[0].split('/')[2]

            for l in lines:
                day  = l.split(';')[0].split('/')[2]
                if day != d:            # skip, if not correct, the first line which is usually wrong
                    print (day, d)
                    continue
                hour = int(l.split(';')[0].split('/')[3])
                if hour < 8:            # for simplicity, we skip all records from 00:00-08:00
                    continue
                o   = int(l.split(';')[1])
                h   = int(l.split(';')[2])
                lo  = int(l.split(';')[3])
                c   = int(l.split(';')[4])
                v   = int(l.split(';')[5])
                
                if prev_min_close != 0:
                    step += abs(c - prev_min_close)
                prev_min_close = c
                
                if day_o == 0:
                    day_o = int(o)
                if int(h) > day_h:
                    day_h = int(h)
                if int(lo) < day_l:
                    day_l = int(lo)
                day_c = int(c)
                day_v += int(v)

#            opendiff=0
            gainpct=0
            if len(close_list) != 0:
#                opendiff = day_o - close_list[len(close_list)-1]           
                gainpct = (day_c - close_list[len(close_list)-1]) / close_list[len(close_list)-1] *100
                gainpct = "%.2f"% gainpct
                
            close_list.append(day_c)
            print(day_o, day_h, day_l, day_c, day_v)
            dt = datetime.date(int(y),int(m),int(d))

            hldiff = day_h - day_l
            volume = day_v
            wave = num_of_wave(y, m, d)
            
            df.loc[len(df)] = [dt, hldiff, gainpct, volume, step, len(wave), volume/len(wave), volume/len(wave)*hldiff/100000]
            

    sortdf = df.sort_values(df.columns[-1], ascending = False)
    print(sortdf)
    
def num_of_wave(y, m, d):
    df = Read_SP_Min_File(y,m.lstrip('0'),d.lstrip('0'))

    s_df = Sdf.retype(df)
    print(df)
    df['sma'] = s_df['close_30_sma']    

    df.dropna(inplace=True)
      
    period = 5
    direction1 = None
    count_direction1 = 0
    wave = []


    for i in range(period, len(df)):         
        if df.iloc[i,-1] > df.iloc[i-period,-1]:
            if direction1 == "Up":
                count_direction1 +=1
            else:
                wave.append(count_direction1)
                count_direction1 = 1
                direction1 = "Up"

        elif df.iloc[i,-1] < df.iloc[i-period,-1]:
            if direction1 == "Down":
                count_direction1 +=1
            else:
                wave.append(count_direction1)
                count_direction1 = 1
                direction1 = "Down"
        
                    
    print(wave)
    print("trend1: %d"%(len(wave)))
    return wave
    
    
              

if __name__ == '__main__':
    today = datetime.date.today()
    
    # generate all min file list:
    afilelist = maybe_update_allminfilelist()
    
    # get only those file in the period
    flist = retrieve_file_list(afilelist, start_date, end_date)
    
    collect_stat(flist)
    
    