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
    test_data=pd.read_csv(rawdata)
    test_data.head()
    return test_data



def plot_data(a):

    
    global xlow,xhigh,xA,yA,zA,dA,pA

    print(f'what is a={xA}')
    
    y_col=yA
    
    x=a[xA]
    y=a[yA]
    z=a[zA]
    d=a[dA]
    p=a[pA]


    y_median=round(y.median(),2)
    z_median=round(z.median(),2)
    d_median=round(d.median(),2)
    p_median=round(p.median(),2)

    y_max=round(y.max(),2)
    z_max=round(z.max(),2)
    d_max=round(d.max(),2)
    p_max=round(p.max(),2)

    y_min=round(y.min(),2)
    z_min=round(z.min(),2)
    d_min=round(d.min(),2)
    p_min=round(p.min(),2)


    y_max=a[y_col].max()
    y_min=a[y_col].min()

    pd.set_option('precision',1)
    plt.style.use('seaborn')

    fig, ax = plt.subplots(3,1,figsize=(15,10),tight_layout=True)

    xlow=x.min()
    xhigh=x.max()

    ax[0].plot(x,y,color='k',label=yA)
    ax[0].plot(x,z,color='g',label=zA)
    ax[0].plot(x,d,color='b',label=dA)
    ax[0].plot(x,p,color='r',label=pA)
    
    ax[0].legend()
    
    ax[0].axhline(y=y_max,linewidth=1, color='black',linestyle="--")
    ax[0].axhline(y=y_min,linewidth=1, color='black',linestyle="--")
    
    ax[0].set_xlabel(xA)
    ax[0].set_ylabel('Temperature')
    
    ax[0].set_xlim(xlow,xhigh)
    
    ax[1].hist(y, 100, density=True,facecolor='k', label=yA, alpha=0.35)
    ax[1].hist(z, 100, density=True,facecolor='g', label=zA, alpha=0.35)
    ax[1].hist(d, 100, density=True,facecolor='b', label=dA, alpha=0.35)
    ax[1].hist(p, 100, density=True,facecolor='r', label=pA, alpha=0.35)
    
    ax[1].set_xlabel('Temperature')
    ax[1].legend()
#     ax[1].plot(bins, y, '--')
    
    
    
    data_for_box=[y,z,d,p]
    ax[2].boxplot(data_for_box,showfliers=False)
    ax[2].set_xticklabels([yA,zA,dA,pA])

    ax[2].annotate(y_median,xy=(1,y_median))
    ax[2].annotate(z_median,xy=(2,z_median))
    ax[2].annotate(d_median,xy=(3,d_median))
    ax[2].annotate(p_median,xy=(4,p_median))

    ax[2].annotate(y_max,xy=(1,y_max))
    ax[2].annotate(z_max,xy=(2,z_max))
    ax[2].annotate(d_max,xy=(3,d_max))
    ax[2].annotate(p_max,xy=(4,p_max))

    ax[2].annotate(y_min,xy=(1,y_min))
    ax[2].annotate(z_min,xy=(2,z_min))
    ax[2].annotate(d_min,xy=(3,d_min))
    ax[2].annotate(p_min,xy=(4,p_min))
    
    
    
##    ax[3].plot(y,z,'ok',markersize=1, alpha=0.5)
##    ax[3].set_xlabel(yA)
##    ax[3].set_ylabel(zA)

    
##    ax[4].hist2d(y,z,bins=50)
##    ax[4].hist2d(d,y,bins=50)
##    ax[4].set_xlabel(yA)
##    ax[4].set_ylabel(dA)
    
    plt.show()

def get_the_value():
    print(var.get())
    print('jim')
    print(var2.get())
    
    
    subset=a[(a[xA]>var.get()) & (a[xA]<var2.get())]
    
    
    plot_data(subset)



#------------------------------------------------------------MAIN--------

global xlow, xhigh,a,xA,yA,zA,dA,pA

##datafile='080-20_6-4-V_SWING.csv'
##datafile='russel_unit_1.csv'
##datafile='07172020_ru1.csv'
datafile='STCU-3_benchmark.csv'


xA='Hours'
yA='box temp'
dA='Top skin'
zA='Bottom skin'
pA='supply'




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




    
    




