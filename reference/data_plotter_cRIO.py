
# coding: utf-8

# In[ ]:


import pandas as pd
pd.set_option('precision', 2)
from pandas.plotting import scatter_matrix
from pandas.plotting import autocorrelation_plot
from pandas.plotting import lag_plot
from io import StringIO
import numpy as np
import datetime
import matplotlib
import matplotlib.pyplot as plt
#% matplotlib inline
plt.style.use('ggplot')
from scipy.stats import skew
from scipy.stats import stats
import tkinter as tk
from tkinter import *
from tkinter.ttk import *





##my_data=pd.DataFrame()
##temperatures=['TOP_SKIN','MID_SKIN','BOT_SKIN','ROOM','BOX','8.125','7.875']
##pressures=['A___8.125','BETWEEN_(MON)','C___7.875']
##AO_channels=['Z3_AIR_PPC1','Z3_LQD_PPC1']
##DO_channels=['Z1A3_PIV','Z1B3_PIV','Z1C3_PIV',''Z1D3_PIV']
##SV_channels=['Z1A2_PPC','Z1B2_PPC','Z1C2_PPC','Z1D2_PPC']

##---------------------------------------------------------------------

def get_data():
    """ this function retreives the raw test data from the designated location."""
    Location=r'C:\Users\96015\Desktop\Jim_Python_Code\Datasets\104-18\104-18_COLD HOLD.dat'
    num_rows=4000
    raw_data=pd.read_csv(Location,header=9,na_values='NotImplemented',skip_blank_lines=False)
    return raw_data
#na_values='NotImplemented.
#The test data's NotImplemented changed to NaN so that specific column can be dropna when ready.""" 

##-------------------------------------------------------------------------------------------------

def data_clean(raw_data):
#Combining the Date and Time columns into the Time column. It will then be converted to a Datetime object.
    raw_data['Time']=raw_data[['Date','Time']].apply(lambda x: ' '.join(x), axis=1)
#Converting the Time column to a Datetime object
    raw_data['Time']=pd.to_datetime(arg=raw_data['Time'])
#removing the Date column since the date and time have been joined under the time column.
    raw_data.drop('Date',axis=1,inplace=True)
#Removed the NaN columns
    raw_data=raw_data.dropna(axis=1)
#All of the columns named UNUSED
    p=raw_data.loc[:, raw_data.columns.str.contains('UNUSED')].head()
#Removing the UNUSED columns
    raw_data.drop(p,axis=1,inplace=True)
#replacing header spaces with underscores 
    raw_data.columns=raw_data.columns.str.replace(' ','_')
#replacing header dashes with underscores
    raw_data.columns=raw_data.columns.str.replace('-','_')
#make the Time column the Datetime index
    raw_data.set_index('Time', inplace=True)
    
    return raw_data


##--------------------------------------------------------------------------------------------------
def plot_data(my_data,temperatures,pressures,AO_channels,DO_channels,SV_channels):
    
    #Y1,Y2,M1,M2,D1,D2,h1,h2,m1,m2,s1,s2=the_date_range(my_data)
    
    
    #global h2
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
    
    
    
   
    plt.close()
    plt.figure(figsize=(15,15))
    plt.suptitle('The Graph')
    
    temps=my_data[pd.datetime(Y1, M1, D1, h1, m1, s1):pd.datetime(Y2, M2, D2, h2, m2, s2)][temperatures]
    print(temps)
    ax1=plt.subplot(511)
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

    ax2=plt.subplot(512)
    plt.plot(press.index.to_pydatetime(),press)
    #plt.plot(k[0],port_B_max,'o',color='black')
    plt.xlabel('Time of Day')
    plt.ylabel('Pressure (PSIG)')
    plt.ylim(10400,10600)
    plt.title('Pressure',loc='left')
    plt.legend(press)
    #plt.setp(ax2.get_xticklabels(), visible=False)

    ax3=plt.subplot(513)
    AO=my_data[pd.datetime(Y1, M1, D1, h1, m1, s1):pd.datetime(Y2, M2, D2, h2, m2, s2)][AO_channels]
    plt.plot(AO.index.to_pydatetime(),AO)
    plt.xlabel('Time of Day')
    plt.ylabel('Analog Output (4mA-20mA)')
    plt.title('LQD & AIR PPC Output',loc='left')
    plt.legend(AO)
    #plt.setp(ax3.get_xticklabels(), visible=False)

    
    ax4=plt.subplot(514)
    DO=my_data[pd.datetime(Y1, M1, D1, h1, m1, s1):pd.datetime(Y2, M2, D2, h2, m2, s2)][DO_channels]
    plt.plot(DO.index.to_pydatetime(),DO)
    plt.xlabel('Time of Day')
    plt.ylabel('Digital Output')
    plt.title('PIV State',loc='left')
    plt.legend(DO)
    #plt.setp(ax4.get_xticklabels(), visible=False)

    
    ax5=plt.subplot(515)
    SV=my_data[pd.datetime(Y1, M1, D1, h1, m1, s1):pd.datetime(Y2, M2, D2, h2, m2, s2)][SV_channels]
    plt.plot(SV.index.to_pydatetime(),SV)
    plt.xlabel('Time of Day')
    plt.ylabel('Analog Output')
    plt.title('Supply/Vent PPC Analog Output State',loc='left')
    plt.legend(SV)
    
    #plt.subplots_adjust(left=None, bottom=None, right=None, top=None,wspace=2, hspace=1)
   
    plt.show()
    
    #data_scatter_matrix(my_data['2017-12-27 15'][pressures])
    
    
    #temperature_noise(my_data['2017-10-25 08']['Ambient'])
    

##------------------------------------------------------------------------------------------------------------

def data_scatter_matrix(x):
    plt.figure()
    scatter_data=x
    scatter_matrix(scatter_data,alpha=.5,diagonal='hist',figsize=(15,10),color='black')
    plt.show()

##---------------------------------------------------------------------

def temperature_noise(temps):
    fig=plt.figure(figsize=(15,10))
    fig.suptitle('Autocorrelation of Temperature During Hold')
    plt.figure()
    plt.acorr(temps,usevlines=False,maxlags=10,color='blue')
    #ax3.autocorrelation_plot(temps['2017-10-25 08']['Ambient'],color='green')
    #ax4.autocorrelation_plot(temps['2017-10-25 08']['T2'],color='black')
    print('Autocorrelation Plot')
    plt.show()

##---------------------------------------------------------------------

def describe_stats(x):
    test_data=x.columns[0:len(x.columns)]
    for i in test_data:
        my_stats=stats.describe(x[i])
        print(i,'\n',my_stats,'\n')
##---------------------------------------------------------------------

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

##---------------------------------------------------------------------    

def my_data_info():
    print(my_data.head())
    print(my_data.info())
    print(my_data.iloc[:,:].agg(['max','min','mean']))

##---------------------------------------------------------------------

def go_to_plot():
    plot_data(my_data,temperatures,pressures,AO_channels,DO_channels,SV_channels)

##---------------------------------------------------------------------

def bye_bye():
    plt.close()
    root.destroy()


##----------MAIN-------------------------MAIN------------------------MAIN------------------------
my_data=get_data()
my_data=data_clean(my_data)

print(my_data.head())

all_data=list(my_data)
temperatures=all_data[0:4]
pressures=all_data[4:7]

AO_channels=['Z3_AIR_PPC1','Z3_LQD_PPC1']
DO_channels=['Z1A3_PIV','Z1B3_PIV','Z1C3_PIV','Z1D3_PIV']
SV_channels=['Z1A2_PPC','Z1B2_PPC','Z1C2_PPC','Z1D2_PPC']


#plot_data(my_data,temperatures,pressures,AO_channels,DO_channels,SV_channels)
#describe_stats(my_data)

Y1,Y2,M1,M2,D1,D2,h1,h2,m1,m2,s1,s2=the_date_range(my_data)

##----------MAIN-------------------------MAIN------------------------MAIN------------------------



"""tkinter code starts here---------------------------------------------------------------------"""
        
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
        
    
btn1 = tk.Button(topframe, text="Plot Data",bg='blue',fg='yellow', command=go_to_plot)
btn2=tk.Button(topframe,text='Get Out',bg='red',fg='yellow',command=bye_bye)
btn1.pack(side=tk.LEFT)
btn2.pack(side=tk.LEFT)
  
root.mainloop()
    
"""tkinter code ends here-----------------------------------------------------------------------"""
    




    

