"""
Created on Fri Sep  8 11:18:57 2017

@author: user
"""

import pandas as pd
import glob

# skipDay and numDay
# skipDay is number of days you want to skip. e.g. 1 if you only want to skip one day
# numDay is number of days you want to process including skipDay
# skipDay=1, numDay=2 will give a result of 1 day trading which is the previous day before yesterday

skipDay=0   # number of day skipped, 0 for nothing
numDay=1


    # Total number of day, including skipDay
dirChina='D:\\user\\Documents\\Python\\chinaconnect\\*.txt'
dirHK='D:\\user\\Documents\\Python\\hkconnect\\*.txt'

debug=True

def sorting(wdir):
    filenames=glob.glob(wdir)
    
    if debug:
        print('Total number of files: ', len(filenames))
    
    main_df=pd.DataFrame()
    countid=1
    for eachfile in reversed(filenames[-numDay:]):
        if skipDay<countid:
            if debug:
                print(eachfile)
            df=pd.read_csv(eachfile,delim_whitespace=True, header=None, encoding='utf_8', thousands=',')
           # print(df)
            df.columns=['dummy','id','name','buy','sell','volume']
            df[countid]=1           # add a new column


            #print(df)
            if main_df.empty:
                main_df=df
            else:
                main_df=main_df.append(df)
        countid=countid+1
#    print(main_df)
#    main_df=main_df.iloc[:,1:]
#    print(main_df)
    main_df.reset_index(drop=True, inplace=True)
#    main_df.columns=['id','name','buy','sell','volume','countid']
#    print(main_df)
    
    # create buySum, sellSum, volSum
    main_df.sort_values('id', inplace=True)
    main_df['buySum']=main_df.groupby('id')['buy'].transform('sum')
    main_df['sellSum']=main_df.groupby('id')['sell'].transform('sum')
    main_df['volSum']=main_df.groupby('id')['volume'].transform('sum')
    main_df.drop('dummy', 1, inplace=True)
    
    # for each 1,2,3,..n columns, add them up if they are same stock
    for num in range(skipDay+1,numDay+1):
        main_df[num]=main_df.groupby('id')[num].transform('sum')

#    print(main_df)
    
    
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
    
    printList=['id','name','buySum','sellSum','net','buyPert']
    for num in range (skipDay+1, numDay+1):
        printList.append(num)
    print(main_df.ix[:,printList])
  
print('==== China ====')
sorting(dirChina)
print('\n\n==== Hong Kong ====')
sorting(dirHK)

