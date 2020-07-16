import pandas as pd
import numpy as np

import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors

import math

try:
##    import tkinter.ttk
    from tkinter import *
except:
    from tkinter import *

# import tkinter as tk   
    
    
from tkinter import messagebox
from tkinter import filedialog

from pandas.plotting import scatter_matrix
from pandas.plotting import lag_plot
from pandas.plotting import autocorrelation_plot
from pandas.plotting import bootstrap_plot

import os
import sys
import subprocess



#------------FUNCTIONS---------------------------FUNCTIONS---------------------

def get_data(rawdata):
    test_data=pd.read_csv(rawdata, skiprows=None)
    test_data.head()
    return test_data



def plot_data(a):
    
    
    
    global xlow, xhigh,xA,yA,zA
    
    y_col=yA
    x=a[xA]
    y=a[yA]
    z=a[zA]
    
    y_max=a[y_col].max()
    y_min=a[y_col].min()

    pd.set_option('precision',1)
    plt.style.use('seaborn')

    fig, ax = plt.subplots(5,1,figsize=(15,10),tight_layout=True)

    xlow=x.min()
    xhigh=x.max()

    ax[0].plot(x,y,label=yA)
    ax[0].plot(x,z,color='r',label=zA)
    ax[0].legend()
    
    ax[0].axhline(y=y_max,linewidth=1, color='black',linestyle="--")
    ax[0].axhline(y=y_min,linewidth=1, color='black',linestyle="--")
    
    ax[0].set_xlabel(xA)
    ax[0].set_ylabel('Temperature')
    
    ax[0].set_xlim(xlow,xhigh)
    
    n, bins, patches=ax[1].hist(y, 100, density=True,facecolor='g', label=yA, alpha=0.75)
    ax[1].hist(z, 100, density=True,facecolor='r', label=zA, alpha=0.75)
    ax[1].set_xlabel('Temperature')
    ax[1].legend()
#     ax[1].plot(bins, y, '--')
    
    
    
    data_for_box=[y,z]
    ax[2].boxplot(data_for_box,showfliers=False)
##    ax[2].boxplot(z,showfliers=False)
    
    ax[2].set_xticklabels([yA,zA])
    
    
    
    ax[3].plot(y,z,'ok',markersize=1, alpha=0.5)
    ax[3].set_xlabel(yA)
    ax[3].set_ylabel(zA)

    
    ax[4].hist2d(y,z,bins=50)

    plt.show()

def get_the_value():
    print(var.get())
    print('jim')
    print(var2.get())
    
    
    subset=a[(a[xA]>var.get()) & (a[xA]<var2.get())]
    
    
    plot_data(subset)



#------------------------------------------------------------MAIN--------

global xlow, xhigh,a,xA,yA,zA

##datafile='080-20_6-4-V_SWING.csv'
datafile='russel_unit_1.csv'


xA='S'
yA='box temp'
##zA='box temp'
zA='supply at box'




a=get_data(datafile)

print(a.head())


plot_data(a)

root = Tk()
root.geometry('500x300')
root['bg']='blue'

scale_tick_interval=sti=(xhigh-xlow)/4

var = DoubleVar()
scale = Scale( root, variable = var, from_=xlow, to=xhigh,
             orient="horizontal",command=None)

scale.config(label='low x', tickinterval=sti,
             sliderlength=20, width=30, length=400)

scale.pack(anchor=CENTER)

var2=DoubleVar()
high_scale=Scale( root, variable = var2, from_=xlow, to=xhigh,
             orient="horizontal",command=var2.set(xhigh))

high_scale.config(label='low x', tickinterval=sti,
                  sliderlength=20, width=30, length=400)

high_scale.pack(anchor=CENTER)

selected_low=Button(root,text='press',command=get_the_value)
selected_low.pack()



mainloop()




    
    




