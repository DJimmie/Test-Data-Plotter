
import os
import sys
import subprocess
import logging
import datetime as dt

import threading
import time

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import math

try:
    import tkinter.ttk
    from tkinter import *
#     from tkinter.ttk import *
except:
    from tkinter import *
    
    
from tkinter import messagebox
from tkinter import filedialog

from pandas.plotting import scatter_matrix
from pandas.plotting import lag_plot
from pandas.plotting import autocorrelation_plot
from pandas.plotting import bootstrap_plot

import program_work_dir as pwd


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# logging file handler
f_handler = logging.FileHandler('workflow_logger.log',mode='w')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
f_handler.setLevel(logging.DEBUG)

ch=logging.StreamHandler()
ch.setFormatter(f_format)
ch.setLevel(logging.DEBUG)
logger.addHandler(f_handler)
logger.addHandler(ch)

#------------FUNCTIONS---------------------------FUNCTIONS---------------------

def get_data(rawdata):
    logger.debug('def get_data(rawdata)')
    test_data=pd.read_csv(rawdata,skiprows=18,usecols=[0,1,2,3,4,5,6,7])

    test_data.drop([0],inplace=True)

    logger.info(f'data columns: {test_data.columns}')


    ## remove all spaces in the header names
    test_data.columns=[x.lstrip() for x in list(test_data.columns)] 

    test_data.rename(columns={"CommStat": "Hours","Seconds":"seconds"},inplace=True)

    
    logger.info(f'test_data.head: {test_data.head()}')
  

    # test_data['Hours']=0
    test_data['Hours']=test_data['seconds']/3600
    
    # using apply method to convert to numeric data types
    test_data[['seconds','Hours','room temp','box temp','dut temp','supply at box']] = test_data[['seconds','Hours','room temp','box temp','dut temp','supply at box']].apply(pd.to_numeric) 
    # test_data['Hours']=test_data['seconds']/3600
    
    test_data.info()

    return test_data



def plot_data(a):

    logger.debug('def plot_data(a)')

    global xlow,xhigh,xA,yA,zA,dA,pA

    print(f'what is a={xA}')
    
    y_col=yA
    
    x=a[xA]
    y=a[yA]
    z=a[zA]
    d=a[dA]
    p=a[pA]


    y_median=round(y.median())
    z_median=round(z.median())
    d_median=round(d.median())
    p_median=round(p.median())

    y_max=round(y.max())
    z_max=round(z.max())
    d_max=round(d.max())
    p_max=round(p.max())

    y_min=round(y.min())
    z_min=round(z.min())
    d_min=round(d.min())
    p_min=round(p.min())


##    y_max=a[y_col].max()
##    y_min=a[y_col].min()


    
    pd.set_option('precision',2)
    plt.style.use('seaborn')
    

    fig, ax = plt.subplots(3,1,figsize=(15,10),tight_layout=True)

    xlow=x.min()
    xhigh=x.max()

    plt.suptitle(title_from_filename,fontsize=24, y=1)
    
    ax[0].plot(x,y,color='k',label=yA)
    ax[0].plot(x,z,color='g',label=zA)
    ax[0].plot(x,d,color='b',label=dA)
    ax[0].plot(x,p,color='r',label=pA)
    
    ax[0].legend()
    
    ax[0].axhline(y=z_max,linewidth=1, color='black',linestyle="--")
    ax[0].axhline(y=z_min,linewidth=1, color='black',linestyle="--")
    
    ax[0].set_xlabel(xA)
    ax[0].set_ylabel('Temperature')
    
    ax[0].set_xlim(xlow,xhigh)
    
##    ax[1].hist(y, 100, density=True,facecolor='k', label=yA, alpha=0.35) ## remove room temp hist
    ax[1].hist(z, 100, density=True,facecolor='g', label=zA, alpha=0.35)
    ax[1].hist(d, 100, density=True,facecolor='b', label=dA, alpha=0.35)
    ax[1].hist(p, 100, density=True,facecolor='r', label=pA, alpha=0.35)
    
    ax[1].set_xlabel('Temperature')
    ax[1].legend()
#     ax[1].plot(bins, y, '--')
    
    
    
##    data_for_box=[y,z,d,p]
    data_for_box=[z,d,p]
    ax[2].boxplot(data_for_box,showfliers=True)
##    ax[2].set_xticklabels([yA,zA,dA,pA])
    ax[2].set_xticklabels([zA,dA,pA])

##    ax[2].annotate(y_median,xy=(1.1,y_median))
    ax[2].annotate(z_median,xy=(1.1,z_median))
    ax[2].annotate(d_median,xy=(2.1,d_median))
    ax[2].annotate(p_median,xy=(3.1,p_median))

##    ax[2].annotate(y_max,xy=(1.1,y_max))
    ax[2].annotate(z_max,xy=(1.1,z_max))
    ax[2].annotate(d_max,xy=(2.1,d_max))
    ax[2].annotate(p_max,xy=(3.1,p_max))

##    ax[2].annotate(y_min,xy=(1.1,y_min))
    ax[2].annotate(z_min,xy=(1.1,z_min))
    ax[2].annotate(d_min,xy=(2.1,d_min))
    ax[2].annotate(p_min,xy=(3.1,p_min))

    #3D Plot
    plot3D=False
    if plot3D==True:
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111, projection='3d')
        surf =ax.plot3D(x,d,p)

        ax.set_xlabel('hours')
        ax.set_ylabel('dut')
        ax.set_zlabel('supply')

 
##    ax[3].plot(y,z,'ok',markersize=1, alpha=0.5)
##    ax[3].set_xlabel(yA)
##    ax[3].set_ylabel(zA)
    
##    ax[4].hist2d(y,z,bins=50)
##    ax[4].hist2d(d,y,bins=50)
##    ax[4].set_xlabel(yA)
##    ax[4].set_ylabel(dA)
    
    fig.tight_layout()
    plt.close()

    return fig
    # plt.show()

def get_the_value():
    logger.debug('def get_the_value()')
    logger.debug(var.get())
    print('jim')
    logger.debug(var2.get())
    
    subset=a[(a[xA]>var.get()) & (a[xA]<var2.get())]

    logger.info(f'subset head:\n{subset.head()}')

    plot_data(subset)




def bye_bye():
        """Close the UI Window on menu Exit"""
        logger.info('Exiting Program')
        top.destroy()
        root.destroy()



def get_plot():

    fig=plot_data(a)
    canvas = FigureCanvasTkAgg(fig, master=top)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

    
def refresh_plot():


    fig=plot_data(get_data(datafile))
    canvas = FigureCanvasTkAgg(fig, master=top)  # A tk.DrawingArea.
    # canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)
    
    plt.figure().close()

    logger.debug('delay')
    # Tk.update()
    NUM_MINUTES=.001
    delay=int(60000*NUM_MINUTES)
    top.after(delay, refresh_plot)

    


    



#------------------------------------------------------------MAIN--------

if __name__ == "__main__":

    logger.info('PROGRAM START')
    # Create program working folder and its subfolders
    config_parameters={'TCU Bench Test Data':{'Purpose':'Plot and analysis the results of TCU benchmark test'}}
    client=pwd.ClientFolder(os.path.basename(__file__),config_parameters)
    ini_file=f'c:/my_python_programs/{client}/{client}.ini'

    # working folder for the storage of data plots
    plot_folder=pwd.WorkDirectory('benchmark_plots',client_folder=client)
    plot_folder_path=f'C:\\my_python_programs\\{plot_folder.client_folder}\\{plot_folder.client_sub_folder}'

    mpl.rcParams["savefig.directory"] = os.chdir(plot_folder_path)

    # working folder for the storage of raw data files
    raw_folder=pwd.WorkDirectory('raw_data',client_folder=client)
    raw_folder_path=f'C:\\my_python_programs\\{raw_folder.client_folder}\\{raw_folder.client_sub_folder}'

    global xlow, xhigh,a,xA,yA,zA,dA,pA,title_from_filename,datafile


    xA='Hours'
    yA='room temp'
    dA='box temp'
    zA='dut temp'
    pA='supply at box'

    my_path=raw_folder_path
        
    # x=filedialog.askopenfilename(initialdir = my_path,title = "Data Repository",filetypes = (("all files","*.*"),("*.csv","*.txt")))
    # filename, file_extension = os.path.splitext(x)
    # datafile=f'{filename}{file_extension}'
    # title_from_filename=os.path.basename(filename)

    # logger.debug(f'datafile: {datafile}')

    # a=get_data(datafile)
    

    root = Tk()

    logger.info('Start tkinter loop')
    root['bg']='blue'
    root.withdraw()

    x=filedialog.askopenfilename(initialdir = my_path,title = "Data Repository",filetypes = (("all files","*.*"),("*.csv","*.txt")))
    filename, file_extension = os.path.splitext(x)
    datafile=f'{filename}{file_extension}'
    title_from_filename=os.path.basename(filename)

    logger.debug(f'datafile: {datafile}')
    a=get_data(datafile)

    top = Toplevel(
            root,
            bg='#00008B',
            bd=5)
        
    # self.top.geometry('1200x600')
    # self.top.attributes('-fullscreen', True)

    menubar=Menu(top)
    menubar.add_command(label="Exit",font='ariel',command=root.destroy)
    menubar.add_command(label="Instructions",font='ariel',command=None)
    top.config(menu=menubar)

    
    top.protocol("WM_DELETE_WINDOW", root.destroy)

    
    # fig=plot_data(a)
    # canvas = FigureCanvasTkAgg(fig, master=top)  # A tk.DrawingArea.
    # canvas.draw()
    # canvas.get_tk_widget().grid(row=0, column=0)

    get_plot()

    x = threading.Thread(target=refresh_plot, args=(1,),daemon=True)
    x.start()

    root.mainloop()





    
    




