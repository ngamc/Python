import pandas as pd

df1 = pd.DataFrame({'id':[0,1,2,3,],
                    'name':['david', 'peter', 'mary', 'susan'],
                    'cash':[500, 10, 65000, 640]
                    })

df1.set_index('id',inplace=True)
                   
df2 = pd.DataFrame({'id':[0,1,2,3],
                    'name':['david', 'peter', 'mary', 'susan'],
                    'age':[25, 24, 30, 21]
                    })
##df2.set_index('id',inplace=True)

df3= pd.DataFrame({'id':[2,3,2,2,3,1], 
                   'Login':['yes','no','yes','yes','no','yes']
                    })

##df3.set_index('id',inplace=True)
print(df1)
##print(df3)


#print(pd.concat([df1,df2]))
#print(pd.merge(df1,df3,how='outer',left_index=True, right_index=True))

##df1['cash']=(df1['cash']-df1['cash'][0])/ df1['cash'][0]

print("[0] is",df1['cash'][0])
