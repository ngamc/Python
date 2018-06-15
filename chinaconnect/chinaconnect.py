"""
Created on Fri Sep  8 11:18:57 2017

@author: user
"""

import pandas as pd
import glob
from tabulate import tabulate
from cash_flow import cashflow
from io import StringIO
import sys
#sys.path.insert(0, '/path/to/application/app/folder')
sys.path.append('D:\\user\\Documents\\Python\\')
from Others.email import sendm

# skipDay and numDay
# skipDay is number of days you want to skip. e.g. 1 if you only want to skip one day
# numDay is number of days you want to process including skipDay
# skipDay=1, numDay=2 will give a result of 1 day trading which is the previous day before yesterday

skipDay=0   # number of day skipped, 0 for nothing
numDay=3


    # Total number of day, including skipDay
dirChina='D:\\user\\Documents\\Python\\chinaconnect\\*.txt'
dirHK='D:\\user\\Documents\\Python\\hkconnect\\*.txt'
focus_list_hk = [5, 27, 66, 388, 700, 772, 799, 1211, 1299, 2318, 2628, 6030]
focus_list_china = [333, 651, 2008, 2230, 2236, 2241, 2415, 2673, 300033, 600036, 600660, 600837, 600887, 601318]

sendemail = False
debug = False

def add_focus_hk(row):
    for id in focus_list_hk:
        if row['id'] == id:
#            print(row['id'])
            return "*"
    return ""

def add_focus_china(row):
    for id in focus_list_china:
        if row['id'] == id:
#            print(row['id'])
            return "*"
    return ""
        
def sorting(wdir, f=None):

    filenames=glob.glob(wdir)
    
    if debug:
        print('Total number of files: ', len(filenames))
    
    main_df=pd.DataFrame()
    countid=1
    for eachfile in reversed(filenames[-numDay:]):
        if skipDay<countid:
            if debug:
                print(eachfile)
            df=pd.read_csv(eachfile,delim_whitespace=True, header=None, encoding='utf-8', thousands=',')
            
#            print(df)
            df.columns=['dummy','id','name','buy','sell','volume']
            df[countid]=1           # add a new column


            #print(df)
            if main_df.empty:
                main_df=df
            else:
                main_df=main_df.append(df)
        countid=countid+1

    if wdir == dirHK:
        main_df['focus'] = main_df.apply(add_focus_hk, axis=1)
    if wdir == dirChina:
        main_df['focus'] = main_df.apply(add_focus_china, axis=1)
    
#    print(main_df)
#    main_df=main_df.iloc[:,1:]
#    print(main_df)
    main_df.reset_index(drop=True, inplace=True)
#    main_df.columns=['id','name','buy','sell','volume','countid']
#    print(main_df)
    
    # create buySum, sellSum, volSum
    main_df.sort_values('id', inplace=True)
#    pd.options.display.float_format = '{:,.2f}'.format
    main_df['buySum']=(main_df.groupby('id')['buy'].transform('sum'))   /1000000
    main_df['sellSum']=(main_df.groupby('id')['sell'].transform('sum')) /1000000
    main_df['volSum']=(main_df.groupby('id')['volume'].transform('sum'))/1000000
    main_df.drop('dummy', 1, inplace=True)
    
    # for each 1,2,3,..n columns, add them up if they are same stock
    for num in range(skipDay+1,numDay+1):
        main_df[num]=main_df.groupby('id')[num].transform('sum')


    
    
    # delete buy, sell, volume and remove duplicate lines
    main_df.drop('buy', 1, inplace=True)
    main_df.drop('sell', 1, inplace=True)
    main_df.drop('volume', 1, inplace=True)
    main_df.drop_duplicates(subset='id', inplace=True)
    
    # create net and buyPert
    main_df['net'] = main_df.buySum - main_df.sellSum
    main_df['buyPert'] = main_df.buySum / main_df.volSum * 100
    
    main_df.sort_values('net', inplace=True, ascending=False)
    
    main_df.fillna(value='-', inplace=True)  # all NaA will become '-'
    main_df['buySum']  = main_df['buySum'].map('{:,.2f}M'.format)
    main_df['sellSum'] = main_df['sellSum'].map('{:,.2f}M'.format)
    main_df['net']     = main_df['net'].map('{:,.2f}M'.format)
    main_df['buyPert']     = main_df['buyPert'].map('{:,.2f}%'.format)

    
    printList=['id','focus', 'name','buySum','sellSum','net','buyPert']
    for num in range (skipDay+1, numDay+1):
        printList.append(num)
        main_df[num] = main_df[num].map('{:,.0f}'.format)
#    print(printList)
#    print(main_df.loc[:,printList])
    print(tabulate(main_df.loc[:,printList], headers='keys', tablefmt='psql'))

    if sendemail:
        print(tabulate(main_df.loc[:,printList], headers='keys', tablefmt='psql'), file =f)
       
    
if __name__ == '__main__':
    if sendemail:
        f = StringIO()
        
    print('==== China ====')
    sorting(dirChina, f)
    print('\n\n==== Hong Kong ====')
    sorting(dirHK, f )
    
    if sendemail:
        sendm("China Connect", f.getvalue())
    else:
        path="D:\\user\\Documents\\Python\\"
        southbound_1 = path + 'hkconnect\\stat\\shanghai_southbound.txt'
        southbound_2 = path + 'hkconnect\\stat\\shenzhen_southbound.txt'
        northbound_1 = path + 'chinaconnect\\stat\\shanghai_northbound.txt'
        northbound_2 = path + 'chinaconnect\\stat\\shenzhen_northbound.txt'
        cashflow(southbound_1, southbound_2, 'South Bound')
        cashflow(northbound_1, northbound_2, 'North Bound')

