# -*- coding: utf-8 -*-
"""
Created on Mon May 21 15:30:26 2018
use Keras to try to predict if the next candle stick is go up/ go down / stay still
x is the hlcv number of n candlestick (defined by num_candle_stick)
y is simply buy / sell / no action

We later add sklearn support for learning
@author: user
"""

from Lib_SP_Min import get_file_list, read_df
import os.path
import numpy
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from plotlosses import PlotLosses
from matplotlib import pyplot as plt
import sys
import pickle
import time

starttime = time.time()

data_file_path = "Z:\\2018\\5"
#data_file_path = "/HSI/2018/5"
num_candlestick = 15       # number of candle stick submitted as x's features
cut_loss_pt = 5     # if next low < current close - cut_loss_pt we will not buy
target_pt   = 5     # if next high - target_pt > current close we will buy
day_start = '09/18/00'      # this is consider as the first candlestick

save_file_x = 'hlcv_sp_min_x'
save_file_y = 'hlcv_sp_min_y'
save_sklearn_model = 'hlcv_sp_min_sklearn.pickle'
    
# Neural Network Parameters:
batch_size = 1024 
epoch_number = 100

def normalized1to0(value, list):
    return ((value - min(list)) / (max(list) - min(list)))

def normalized1toMinus1(value, list):
    return (2*(value - min(list))/(max(list) - min(list)) -1)
    

def maybe_process_and_save():
    np_data_x = numpy.empty([0,0])       # create empty np array. Will be saved to disk later
    np_data_y = numpy.empty([0,0]) 
    total_files_processed = 0
    filelist = get_file_list(data_file_path)   # use \\ in subfolder
    
    for file in filelist:
        df = read_df(file)
        if (df.empty == False):         # df is empty if it is not valid
            print(file, df.shape)
            df.columns=['datetime','open','high','low','close','volume']
            
            # remove all entries before 09:18
            num=df.loc[df['datetime'].str.contains(day_start)].index.values
            
            if(num.shape[0]==0):            # sometimes our day_start time entry is missing. We will skip that file
                continue     
            
            df=df[num[0]:]
    #        print(df.iloc[0:5])
            
            x_raw=df.values[:,1:6]      # convert to numpy array
    #        print(x_raw.shape)
    
    
            x = []
            y = []
            idx=0
            x_list=x_raw.tolist()
            
            for open, high, low, close, volume in x_list:
                x_instance = []
                
                # Find out the max and min price, volume for candlestick group
                # we use it to normalize price & volume data afterward
                priceset=[] 
                volumeset=[]

                for j in range(num_candlestick):
                    x_list_next = x_list[idx+j]
                    priceset.append(x_list_next[1] - open)
                    priceset.append(x_list_next[2] - open)
                    priceset.append(x_list_next[3] - open)
                    volumeset.append(x_list_next[4])   
                
                if ((max(priceset) == min(priceset)) or (max(volumeset) == min(volumeset))):
#                    print(max(priceset), min(priceset), max(volumeset), min(volumeset), file, volumeset)
                    continue        # pass or otherwise divided by zero exception later

                # we each n candlestick's hlcv
                for i in range(num_candlestick):
                    x_list_next = x_list[idx+i]
                    
                    # Below 3 lines are no normalizations
#                    x_instance.append(x_list_next[1] - open)
#                    x_instance.append(x_list_next[2] - open)
#                    x_instance.append(x_list_next[3] - open)
                    
                    # Below 3 lines are for normalization
                    x_instance.append(normalized1toMinus1((x_list_next[1] - open), priceset))
                    x_instance.append(normalized1toMinus1((x_list_next[2] - open), priceset))
                    x_instance.append(normalized1toMinus1((x_list_next[3] - open), priceset))
                    
                    # volume will be normalized anyway
                    x_instance.append(normalized1to0(x_list_next[4], volumeset))
                
                x.append(x_instance)
                    
                    
                # obtain y value
                # action value: 0 - no action 1 - buy 2-sell
                x_list_target = x_list[idx+num_candlestick]
                p_close = x_list[idx + num_candlestick - 1][3]  # previous candlestick close
                action = 0          
                
#                y_open   = x_list_target[0]
                y_high   = x_list_target[1]
                y_low    = x_list_target[2]
#                y_close  = x_list_target[3]
#                y_volume = x_list_target[4]
                
                if y_low + cut_loss_pt >= p_close and y_high > p_close + target_pt:
                    action = 1
                elif (y_high - cut_loss_pt <= p_close) and (y_low < p_close - target_pt):
                    action = -1
                    
                y.append(action)
                        
                if (idx==len(x_list) - num_candlestick - 2):
                    break
                else:
                    idx=idx+1
           
    #        print(x)
            x_numpy = numpy.asarray(x)
            y_numpy = numpy.asarray(y)
            
    #        print(x_numpy.shape)
            total_files_processed += 1
    #        print(x_numpy)
    #        print(y_numpy)
    #        print(x_numpy.shape)
            if (np_data_x.shape[0] == 0):
                np_data_x = x_numpy
                np_data_y = y_numpy
            else:
                print(np_data_x.shape, x_numpy.shape)
                np_data_x = numpy.concatenate((np_data_x, x_numpy))
                np_data_y = numpy.concatenate((np_data_y, y_numpy))
    
    
    numpy.save(save_file_x, np_data_x)
    numpy.save(save_file_y, np_data_y)
    
    print("\r\n")
    print('='*40)
    print('np_data shape: x = %s y = %s'%(np_data_x.shape, np_data_y.shape))  
    print('Total files processed:', total_files_processed)
    print('Saved files to %s.npy and %s.npy '% (save_file_x,  save_file_y))
    print('='*40)

def run_nn(x, y):
    
    y = np_utils.to_categorical(y, 3)       # we have 3 class
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
   
    
    model = Sequential()
    model.add(Dense(16, input_dim=(x.shape[1]) ))
    model.add(Dropout(0.2))
    model.add(Dense(128, ))
    model.add(Dense(128, ))
    model.add(Dropout(0.2))
    model.add(Dense(128, ))
    model.add(Dropout(0.2))

#    model.add(Dense(64, activation='sigmoid' ))
#    model.add(Dropout(0.2))
#    model.add(Dense(32, activation='relu' ))
    model.add(Dense(8,  ))
    model.add(Dropout(0.2))
    model.add(Dense(3, activation='softmax'))
    model.summary()
    
    plot_losses = PlotLosses()  
    
    model.compile(optimizer='SGD', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=epoch_number, validation_split=0.2, batch_size=batch_size, callbacks=[plot_losses], verbose=1)

    score=model.evaluate(x_test, y_test, verbose=0)
    print('Test loss: %.3f' % score[0])
    print('Test accuracy: %.3f' % (score[1]*100))
    plot_losses.plot();
  
def run_sklearn(x, y, new_model = True):
  
    x_list = x.tolist()
    y_list = y.tolist()
    x_train, x_test, y_train, y_test = train_test_split(x_list, y_list, test_size=0.33)
    
    clf = svm.SVC(verbose=False)
    model = None
    
    if new_model:        
        model = clf.fit(x_train, y_train) 
        with open(save_sklearn_model, 'wb') as f:
            pickle.dump(model, f)
        print("Saved model to", save_sklearn_model)
    else:
        print("Loading model from", save_sklearn_model)
        with open(save_sklearn_model, 'rb') as f:
            model=pickle.load(f)
            
    y_predict = model.predict(x_test)
#    print('MSE:  %.2f' % mean_squared_error(y_test, y_predict) )
    accuracy = accuracy_score(y_test, y_predict)
    error_rate = 1 - accuracy
    
    print("Error rate: %.2f%%" % (error_rate*100))


if __name__ == '__main__':
    if os.path.isfile(save_file_x + '.npy') and os.path.isfile(save_file_y + '.npy'):
        print('Found data file')
        
    else:
        maybe_process_and_save()

    np_load_x = numpy.load(save_file_x + '.npy')
    np_load_y = numpy.load(save_file_y + '.npy')
    
#    print("\r\n")
    print('='*40)
    print('Loaded data file from: %s.npy and %s.npy' % (save_file_x,  save_file_y))
    print('np_data shape: x = %s y = %s' % (np_load_x.shape, np_load_y.shape))  
    print('='*40)
    
    run_nn(np_load_x, np_load_y)
#    run_sklearn(np_load_x, np_load_y, True)
    
    print("Learning used %.2f seconds or %.2f minutes" % ((time.time()-starttime), (time.time()-starttime)/60))
