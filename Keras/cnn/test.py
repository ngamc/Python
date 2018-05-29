# -*- coding: utf-8 -*-
"""
Created on Mon May 28 13:05:38 2018

@author: user
"""

import numpy as np
#y = [0,2]
#y = np.asarray(y)
#
#x = [[0,0],
#     [1,1],
#     [2,2],
#     [3,3],
#     [4,4]]
#x = np.asarray(x)
#
#print(x.shape)
#
#z = x[[1,2],:]
#print(z)

a = np.array(((1,2),(2,3)))
print(a.shape)
print(a)
a=a.reshape(-1, len(a))
print(a.shape)
print(a)