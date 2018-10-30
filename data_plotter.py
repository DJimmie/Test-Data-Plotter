import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import math
from scipy.stats import skew
from scipy.stats import stats
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from pandas.plotting import scatter_matrix
from pandas.plotting import lag_plot
from pandas.plotting import autocorrelation_plot
from pandas.plotting import bootstrap_plot


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


def the_date_range(my_data):
#Establishes the range of the Datetime index    
    Y1=my_data.index.date.min().year
    Y2=my_data.index.date.max().year
    M1=my_data.index.date.min().month
    M2=my_data.index.date.max().month
    D1=my_data.index.date.min().day
    D2=my_data.index.date.max().day
    h1=my_data.index.min().hour
    h2=my_data.index.max().hour
    m1=my_data.index.min().minute
    m2=my_data.index.max().minute
    s1=my_data.index.min().second
    s2=my_data.index.max().second
     
    return Y1,Y2,M1,M2,D1,D2,h1,h2,m1,m2,s1,s2

def plot_data(my_data,temperatures,pressures):
    
    Y1=int(combo_Y1.get())
    Y2=int(combo_Y2.get())
    M1=int(combo_M1.get())
    M2=int(combo_M2.get())
    D1=int(combo_D1.get())
    D2=int(combo_D2.get())
    h1=int(combo_h1.get())
    h2=int(combo_h2.get())
    m1=int(combo_m1.get())
    m2=int(combo_m2.get())
    s1=int(combo_s1.get())
    s2=int(combo_s2.get())

    print('clicked results:',Y1,Y2,M1,M2,D1,D2,h1,h2,m1,m2,s1,s2)
    
    
    
   
##    plt.close()
    plt.figure(figsize=(10,10))
    plt.suptitle('The Graph')
    
    temps=my_data[pd.datetime(Y1, M1, D1, h1, m1, s1):pd.datetime(Y2, M2, D2, h2, m2, s2)][temperatures]
    print(temps)
    
    ax1=plt.subplot(211)
    plt.plot(temps.index.to_pydatetime(),temps)
    plt.xlabel('Time of Day')
    plt.ylabel('Temperature (°F)')
    plt.title('Temperature',loc='left')
    plt.legend(temps)
    #plt.setp(ax1.get_xticklabels(), visible=False)

    press=my_data[pd.datetime(Y1, M1, D1, h1, m1, s1):pd.datetime(Y2, M2, D2, h2, m2, s2)][pressures]
    port_B_max=press[pressures[0]].max()

#the index corresponding to the max_press
    #k=press.index[press[pressures[0]]==port_B_max].tolist()
    #print(port_B_max,k)

    ax2=plt.subplot(212)
    plt.plot(press.index.to_pydatetime(),press)
    #plt.plot(k[0],port_B_max,'o',color='black')
    plt.xlabel('Time of Day')
    plt.ylabel('Pressure (PSIG)')
    plt.ylim(0,10000)
    plt.title('Pressure',loc='left')
    plt.legend(press)
    #plt.setp(ax2.get_xticklabels(), visible=False)

    plt.show()
    
    #data_scatter_matrix(my_data['2017-12-27 15'][pressures])
    #temperature_noise(my_data['2017-10-25 08']['Ambient'])
    

def go_to_plot():
    plot_data(my_data,temperatures,pressures)

def go_to_analysis():
    zoom_analysis(my_data, pressures)

def go_to_noise():
    noise_check(my_data)    



def zoom_analysis(my_data, pressures):

    Y1=int(combo_Y1.get())
    Y2=int(combo_Y2.get())
    M1=int(combo_M1.get())
    M2=int(combo_M2.get())
    D1=int(combo_D1.get())
    D2=int(combo_D2.get())
    h1=int(combo_h1.get())
    h2=int(combo_h2.get())
    m1=int(combo_m1.get())
    m2=int(combo_m2.get())
    s1=int(combo_s1.get())
    s2=int(combo_s2.get())

    start=pd.datetime(Y1, M1, D1, h1, m1, s1)
    stop=pd.datetime(Y2, M2, D2, h2, m2, s2)

    the_data=my_data[start:stop]
    print(the_data)

    
    the_data.hist(bins=50, figsize=(8,8))
    the_data.plot(kind='density', subplots=True, sharex=False, figsize=(8,8))
    the_data.plot(kind='box', subplots=True, sharex=False, sharey=False, figsize=(8,8))
    
    
    plt.figure(figsize=(8,8))
    plt.hist2d(the_data['pump_pr'], the_data['back_be'], bins=100)

    scatter_matrix(the_data, alpha=0.2, figsize=(6, 6), diagonal='kde')
    plt.title('SCATTER MATRIX')

    bootstrap_plot(the_data['pump_pr'], size=50, samples=500, color='grey')
      
    pump_press_mav=the_data.pump_pr.rolling(window=30)
    pump_press_mav_mean=pump_press_mav.mean()
    
    print(pump_press_mav)
    print(pump_press_mav_mean)

    press=my_data[pd.datetime(Y1, M1, D1, h1, m1, s1):pd.datetime(Y2, M2, D2, h2, m2, s2)][pressures]
    max_press=press.max()
    min_press=press.min()
    
    print(press.head())
    print(press.max())
    

    plt.figure(figsize=(8,8))
    plt.plot(press.index.to_pydatetime(),press, label='pump pressure')
    plt.plot(pump_press_mav_mean.index.to_pydatetime(),pump_press_mav_mean, label='smoothed')
    plt.xlabel('Time of Day')
    plt.ylabel('Pressure (PSIG)')
    y_max=round((max_press+1000),-3)
    y_min=round((min_press-1000),-3)
    
    print('ymax:',y_max[0])
    plt.ylim(y_min[0], y_max[0])
    plt.title('Pressure',loc='left')
##    plt.legend(press)
    plt.legend()
##    pump_press_mav_mean.plot(color='r')
    
    plt.show()



def noise_check(my_data):

    Y1=int(combo_Y1.get())
    Y2=int(combo_Y2.get())
    M1=int(combo_M1.get())
    M2=int(combo_M2.get())
    D1=int(combo_D1.get())
    D2=int(combo_D2.get())
    h1=int(combo_h1.get())
    h2=int(combo_h2.get())
    m1=int(combo_m1.get())
    m2=int(combo_m2.get())
    s1=int(combo_s1.get())
    s2=int(combo_s2.get())

    start=pd.datetime(Y1, M1, D1, h1, m1, s1)
    stop=pd.datetime(Y2, M2, D2, h2, m2, s2)

    the_data=my_data[start:stop]

    plt.figure(figsize=(10,10))
    plt.suptitle('LAG PLOTS')

    ax1=plt.subplot(211)
    lag_plot(the_data['back_be'], c='r')

    ax2=plt.subplot(212)
    lag_plot(the_data['pump_pr'])

    plt.figure(figsize=(8,8))
    autocorrelation_plot(the_data.pump_pr)
     
     
    
##    fig, axes=plt.subplots(nrows=1, ncols=2,figsize=(8,8))
##    axes[0]=lag_plot(the_data['pump_pr'])
##    axes[0].set_title('Lag Plot')
##    axes[0]=autocorrelation_plot(the_data.pump_pr)

    plt.show()


  
def bye_bye():
    plt.close()
    root.destroy()

# In[12]:

#-------------------------------------------------------------------------------------------



if __name__ == '__main__':
    Location=r'C:\Users\96015\Desktop\Jim_Python_Code\Datasets\dynex_900rpm.csv'
    my_data=get_data(Location)
    my_data=clean_data(my_data)
    Y1,Y2,M1,M2,D1,D2,h1,h2,m1,m2,s1,s2=the_date_range(my_data)

    all_data=list(my_data)
    print (all_data)
    temperatures=all_data[1:4]
    pressures=all_data[0:1]
    print('the pressures:', pressures)

    root = Tk()
    root.title("Plot Parameters")
    #window.geometry('400x400')

    topframe=Frame(root)
    topframe.pack()
    window=Frame(root)
    window.pack()
        
    months=[i1 for i1 in range(M1,M2+1)]
    days=[i2 for i2 in range(D1,D2+1)]
    hours=[i3 for i3 in range(0,23)]
    mins_secs=[i4 for i4 in range(0,59)]
        
    #print('before selection:',Y1,Y2,M1,M2,D1,D2,h1,h2,m1,m2,s1,s2)
        
        
    v1=StringVar(window)
    v2=StringVar(window)
    v3=StringVar(window)
    v4=StringVar(window)
    v5=StringVar(window)
    v6=StringVar(window)
    v7=StringVar(window)
    v8=StringVar(window)
    v9=StringVar(window)
    v10=StringVar(window)
    v11=StringVar(window)
    v12=StringVar(window)
        
        
    combo_Y1 = Combobox(window,textvariable=v1,values=[Y1,2018,2017])
    combo_Y2 = Combobox(window,textvariable=v2,values=[Y2,2018,2017])
    combo_M1 = Combobox(window,textvariable=v3,values=[M1]+months)
    combo_M2 = Combobox(window,textvariable=v4,values=[M2]+months)
    combo_D1 = Combobox(window,textvariable=v5,values=[D1]+days)
    combo_D2 = Combobox(window,textvariable=v6,values=[D2]+days)
    combo_h1 = Combobox(window,textvariable=v7,values=[h1]+hours)
    combo_h2 = Combobox(window,textvariable=v8,values=[h2]+hours)
    combo_m1 = Combobox(window,textvariable=v9,values=[m1]+mins_secs)
    combo_m2 = Combobox(window,textvariable=v10,values=[m2]+mins_secs)
    combo_s1 = Combobox(window,textvariable=v11,values=[s1]+mins_secs)
    combo_s2 = Combobox(window,textvariable=v12,values=[s2]+mins_secs)        
        
    #d=combo_h2.bind('<<ComboboxSelected>>',lambda x:2)
        
    combo_Y1.current(0) #set the selected item
    combo_Y2.current(0) #set the selected item
    combo_M1.current(0) #set the selected item
    combo_M2.current(0) #set the selected item
    combo_D1.current(0) #set the selected item
    combo_D2.current(0) #set the selected item
    combo_h1.current(0) #set the selected item
    combo_h2.current(0) #set the selected item
    combo_m1.current(0) #set the selected item
    combo_m2.current(0) #set the selected item
    combo_s1.current(0) #set the selected item
    combo_s2.current(0) #set the selected item
         
    combo_Y1.grid(column=0, row=3)
    combo_Y2.grid(column=0, row=4)
    combo_M1.grid(column=0, row=5)
    combo_M2.grid(column=0, row=6)
    combo_D1.grid(column=0, row=7)
    combo_D2.grid(column=0, row=8)
    combo_h1.grid(column=0, row=9)
    combo_h2.grid(column=0, row=10)
    combo_m1.grid(column=0, row=11)
    combo_m2.grid(column=0, row=12)
    combo_s1.grid(column=0, row=13)
    combo_s2.grid(column=0, row=14)

    hist_btn=tk.Button(window, text="Analysis",bg='blue',fg='yellow', command=go_to_analysis)
    hist_btn.grid(column=1,row=2)

    hist_btn=tk.Button(window, text="Noise",bg='blue',fg='yellow', command=go_to_noise)
    hist_btn.grid(column=1,row=3)
            
        
    btn1 = tk.Button(topframe, text="Plot Data",bg='blue',fg='yellow', command=go_to_plot)
    btn2=tk.Button(topframe,text='Get Out',bg='red',fg='yellow',command=bye_bye)
    btn1.pack(side=tk.LEFT)
    btn2.pack(side=tk.LEFT)
      
    root.mainloop()
        
    """tkinter code ends here-----------------------------------------------------------------------"""
        




