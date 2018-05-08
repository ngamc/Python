
import pandas as pd


def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 2
    for col in cols:
        print('Doing ',col)
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0

def abc(a,b,c):
     return a*10000+b*100+c

list1=[11,22,33]
list2=[44,55,66]
list3=[77,88,99]
a=pd.DataFrame()

print(tuple(map(abc,list1,list2,list3)))
print(dir (list1))
print(dir (abc))
print(dir(a))
#print(buy_sell_hold(0,-10,2,3,4,5))
