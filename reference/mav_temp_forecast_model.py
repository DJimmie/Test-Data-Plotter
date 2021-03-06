import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import math
from scipy.stats import skew
from scipy.stats import stats
from scipy import fftpack
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from pandas.plotting import scatter_matrix
from pandas.plotting import lag_plot
from pandas.plotting import autocorrelation_plot
from pandas.plotting import bootstrap_plot
from math import sqrt
from numpy import mean
from sklearn.metrics import mean_squared_error
from random import seed
from random import randrange
from random import random
from statsmodels.tsa.stattools import adfuller


pd.set_option('precision',1)


plt.style.use('ggplot')


# In[2]:

def get_data(location):
    
##    num_rows=7223
    
    usecols=[1,2,5,19,20,21]
    my_data=pd.read_csv(location, skiprows=None, header=0, usecols=usecols)

    #na_values='NotImplemented'. 
    #The test data's NotImplemented changed to NaN so that specific column can be dropna when ready.

    print(my_data.head(10),'\n')
    print(my_data.info())

    print(my_data.shape)
    return my_data 
    



def clean_data(my_data):
    
    print(my_data.head(),'\n')

##    Removes unwanted spaces in the header name.
    my_data.columns = my_data.columns.to_series().apply(lambda x: x.strip())
    
    # Combining the Date and Time columns into the Time column. It will then be converted to a Datetime object.
    my_data['Time']=my_data[['DATE','TIME']].apply(lambda x: ' '.join(x), axis=1)


    #Converting the Time column to a Datetime object
    my_data['Time']=pd.to_datetime(arg=my_data['Time'])

    #removing the separate DATE  and TIME columns since the date and time have been joined under the Time column.
    my_data.drop('DATE',axis=1,inplace=True)
    my_data.drop('TIME',axis=1,inplace=True)

    #Removed the NaN columns
    my_data=my_data.dropna(axis=1)


    # All of the columns named UNUSED
    p=my_data.loc[:, my_data.columns.str.contains('UNUSED')].head()

    #Removing the UNUSED columns
##    my_data.drop(p,axis=1,inplace=True)

    #replacing header spaces with underscores 
    my_data.columns=my_data.columns.str.replace(' ','_')

    #replacing header dashes with underscores
    my_data.columns=my_data.columns.str.replace('-','_')


    #looking at the extremes of the test data
    my_data.iloc[:,:].agg(['max','min'])

    # make the Time column the Datetime index
    my_data.set_index('Time', inplace=True)
    print(my_data.head(),'\n')
    print(my_data.info())
    
    return my_data



def data_analysis(the_data):

    plt.figure(figsize=(8,8))
    plt.title('Autocorrelation')
    autocorrelation_plot(the_data)

##    plt.figure(figsize=(8,8))
##    lag_plot(the_data)



def the_random_walk():
    
    seed(1)
    random_walk=list()
    random_walk.append(-1 if random() <0.5 else 1)

    for i in range (1,1000):
        movement =(-1 if random() <0.5 else 1)
        value=random_walk[i-1] +movement
        random_walk.append(value)
    
##    series=[randrange(10) for i in range(1000)]
##    print(series)

    plt.figure(figsize=(8,8))
    plt.title('Random Walk')
    plt.plot (random_walk, color='black')

    data_analysis(np.asarray(random_walk))

##    mav_forcast(np.asarray(random_walk))

    dicky_fuller_test(np.asarray(random_walk))



def mav_forcast(my_data):

    X=my_data
    data_analysis(X)

    

    window=3
    history=[X[i] for i in range (window)]
    test=[X[i] for i in range (window, len(X))]
    predictions=list()


    for t in range(len(test)):
        length=len(history)
        yhat=mean([history[i] for i in range(length-window,length)])
        obs=test[t]
        predictions.append(yhat)
        history.append(obs)
##        print('predicted=%f, expected=%f' %(yhat,obs))

    rmse=sqrt(mean_squared_error(test, predictions))
    print ('Test RMSE:', rmse)

    plt.figure(figsize=(10,8))
    plt.title('Actual and Predictions (all data)')
    plt.plot (test, color='black')
    plt.plot(predictions, color='r')

    plt.figure(figsize=(10,8))
    plt.title('Actual and Predictions (zoomed in)')
    plt.plot (test[500:700], color='black')
    plt.plot(predictions[500:700], color='r')
    

def test_dataset(location):

    my_data=get_data(location)
    my_data=clean_data(my_data[1000:2000])
    my_data=my_data['pump_pr'].values

    mav_forcast(my_data)
    
def dicky_fuller_test(the_data):
    result=adfuller(the_data)
    print(f'ADF Statistic:{result[0]}')
    print(f'p-value: {result[1]}')
    print('Critical Values:')
    for key,value in result[4].items():
        print(f'\{key}: {value}')
        

if __name__ == '__main__':

    Location=r'C:\Users\96015\Desktop\Jim_Python_Code\Datasets\dynex_900rpm.csv'
    
##    test_dataset(Location)
    the_random_walk()


    plt.show()


                  
                  
        

    
    





