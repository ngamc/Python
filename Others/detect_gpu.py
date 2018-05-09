# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

#from keras import backend as K
#K.tensorflow_backend._get_available_gpus()