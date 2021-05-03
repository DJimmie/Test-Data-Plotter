import pandas as pd
import numpy as np

import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors

import math

try:
    import tkinter.ttk
    from tkinter import *
except:
    from tkinter import *
    
from tkinter import messagebox
from tkinter import filedialog

from pandas.plotting import scatter_matrix
from pandas.plotting import lag_plot
from pandas.plotting import autocorrelation_plot
from pandas.plotting import bootstrap_plot

import os
import sys
import subprocess

#----------------------------------------------------

class TestData():
    
    data_columns_list=list()
    x_value=None
    y_value=None

    skiprows=None
    
    def __init__(self,datafile):
        self.datafile=datafile
        
    def get_data(self):
        self.data=pd.read_csv(self.datafile, skiprows=TestData.skiprows)
        
        
        print(f'THE HEADERS:{TestData.data_columns_list}')
        self.drop_unused_columns()
        TestData.data_columns_list=self.data.columns.tolist()
        
        
    def drop_unused_columns(self):
        # All of the columns named UNUSED
        p=self.data.loc[:, self.data.columns.str.contains('Unnamed')].head()
        self.data.drop(p,axis=1,inplace=True)
        
        self.clean_data()
        
    def clean_data(self):
        #replacing header spaces with underscores 
        self.data.columns=self.data.columns.str.replace(' ','_')

        #replacing header dashes with underscores
        self.data.columns=self.data.columns.str.replace('-','_')
        self.data.columns=self.data.columns.str.replace(':','')
        self.data.columns=self.data.columns.str.replace('@','')
        
        
        
    def plot_data(self):
    
        pd.set_option('precision',1)
        plt.style.use('ggplot')

        fig, ax = plt.subplots(2,1,figsize=(15,10))

        plt.suptitle(UI.filename)

        the_labels=self.data.columns.tolist()
#         print(the_labels)
        
        xlow=self.data[TestData.x_value].min()
        xhigh=self.data[TestData.x_value].max()
        pressure_max=round(self.data[TestData.y_value].max(),ndigits=1)

        ax[0]=plt.subplot(111)
        ax[0].plot(self.data[TestData.x_value],self.data[TestData.y_value])
        ax[0].axhline(y=pressure_max,linewidth=2, color='black',linestyle="--")
        ax[0].set_xlabel(TestData.x_value)
        ax[0].set_ylabel(TestData.y_value)
        ax[0].set_xlim(xlow,xhigh)
        ax[0].set_title(f'Max {TestData.y_value}:{pressure_max}',loc='left')
        ax[0].legend()
        

        plt.show()
        
      

class UserInterface():
    """Parent class for the UI. Instantiates the composit Window"""

    def __init__(self):
        UI(None)
        mainloop()


class UI(Tk):
    """User Interface."""
    
    now=dt.date.today().strftime('%B %d, %Y')
    time_of_day=dt.datetime.today().strftime('%I:%M:%S %p')
    
    l=list()
    
    filename=None

    fix_X=0
    
    initialdir=os.getcwd()

    
    
    def __init__(self,parent,*args,**kargs):
        """Create the UI Window"""
        Tk.__init__(self,parent,*args,**kargs)
        
        self.parent=parent
        self.initialize()
        self.banner=Label(self,text=f'DRILLING CONTROLS DATA PLOTS & ANALYSIS\n{UI.now}',fg='white',bg='blue',font='Ariel 30 bold')
        self.banner.grid(row=0,column=0, columnspan=2)

    def initialize(self):
            """Set-up and configure the UI window"""
            self.title('UML Project')
            the_window_width=self.winfo_screenwidth()
            the_window_height=self.winfo_screenheight()
    #         self.configure(width=the_window_width,height=the_window_height)
            the_window_width=1000
            the_window_height=700
            self.geometry(f'{the_window_width}x{the_window_height}+0+0')
    #         self.attributes('-fullscreen', True)
            self['borderwidth']=4
            self['bg']='blue'
            self.menubar=Menu(self)
            self.menubar.add_command(label="Exit",font='ariel',command=self.bye_bye)
            self.config(menu=self.menubar)
            self.makeFields()
    
    def bye_bye(self):
        """Close the UI Window on menu Exit"""
        self.destroy()
        
    def makeFields(self):
        """Generate the fields and buttons"""
        # make the frame
        self.frame1=Frame(self.parent)
        self.frame1['background']='green'
        self.frame1['relief']='raised'
        self.frame1['borderwidth']=10
        self.frame1.grid(row=1,column=0,columnspan=2)
        banner_text='Drilling Controls-Data Plotting & Analysis'
        frame_banner=Label(self.frame1,text=banner_text,fg='white',bg='green',font='Ariel 15 bold')
        frame_banner.grid(row=0,column=0,columnspan=5,pady=15)

        self.file_label=Label(self.frame1,bg='green',fg='yellow', text='Data File Name',font='Ariel 12 bold')
        self.file_label.grid(row=2,column=0)
        self.v1=StringVar()
        self.txt_file=Entry(self.frame1,bg='yellow',font='Ariel 15 bold',width=30,textvariable=self.v1)
        self.txt_file.grid(row=3,column=0,sticky=E)
        
        # Buttons
        
        self.access_dir=Button(self.frame1, text="Open Directory",bg='blue',fg='yellow',relief='raised',state='normal',command=self.open_directory)
        self.access_dir.grid(row=5,column=0,sticky=W,pady=5)

        self.view_file=Button(self.frame1, text="View File",bg='blue',fg='yellow',relief='raised',state='normal',command=view_the_file)
        self.view_file.grid(row=5,column=1,sticky=E,pady=5)

        self.set_x_value=Button(self.frame1, text="Fix X",bg='blue',fg='yellow',relief='raised',state='normal',command=self.fix_x_state)
        self.set_x_value.grid(row=6,column=1,sticky=N,pady=5)

        # Header list box
        self.header_list=Listbox(self.frame1,bg='cyan',fg='blue',font='Ariel 12 bold')
        self.header_list['selectmode']=SINGLE
        self.header_list.grid(row=6,column=0,sticky=W,pady=5)

        # skiprow entry field

        self.skip_row_label=Label(self.frame1,bg='green',fg='yellow', text='Skip Rows',font='Ariel 12 bold')
        self.skip_row_label.grid(row=4,column=2,sticky=E)
        self.v2=IntVar()
        self.skip_rows=Entry(self.frame1,bg='blue',fg='yellow', font='Ariel 15 bold',width=5,textvariable=self.v2)
        self.skip_rows.grid(row=5,column=2,sticky=E)


    def fix_x_state(self):
        
        if (UI.fix_X!=1):
            UI.fix_X=1
            self.set_x_value['bg']='red'
            clear_plot_variables()
        else:
            UI.fix_X=0
            self.set_x_value['bg']='blue'
            clear_plot_variables()

        print(UI.fix_X)

        
    def open_directory(self):
        """Opens the directory folder for user to access"""

        if (UI.fix_X!=0):
            self.fix_x_state()
        
        x=filedialog.askopenfilename(initialdir = UI.initialdir,title = "Directory",
                                     filetypes = (("csv files","*.csv"),("all files","*.*")))
        
        print(x)
        
        path=self.set_directory(x)

        the_file_name=x.split(sep='/')[-1].split('.')[0]
        self.v1.set(the_file_name)
##        dataFile=f'{the_file_name}.csv'
        dataFile=path
        print(f'datafile:{dataFile}')
        
        
        
        self.the_data=TestData(dataFile)

        TestData.skiprows=int(self.skip_rows.get())
        print(f'sr:{TestData.skiprows}\ntype:{type(TestData.skiprows)}')
        self.the_data.get_data()
        
        self.header_list.delete(0,END)
        header_list=TestData.data_columns_list
        print(f'HEADERS:{header_list}')
        for i in header_list:
            self.header_list.insert(END,i)
        
        self.header_list.bind("<<ListboxSelect>>",lambda x: self.selected_columns())
            
    def selected_columns(self):

        if (UI.fix_X==0):
            
            selection=self.header_list.curselection()
            c=self.header_list.get(ANCHOR)
            UI.l.append(c)
            print(f'{c}\nlength of list:{len(UI.l)}')
            if (len(UI.l)==2):
                print(UI.l)
                TestData.x_value=UI.l[0]
                TestData.y_value=UI.l[1]
                clear_plot_variables()
                self.the_data.plot_data()
                print(f'after plot list:{UI.l}')
        else:
            selection=self.header_list.curselection()
            print(f'selection={selection}')
##            c=self.header_list.get(ANCHOR)
            c=self.header_list.get(selection[0])
            print(f'c={c}')
            UI.l.append(c)
            if (len(UI.l)>1):
                TestData.x_value=UI.l[0]
                TestData.y_value=c
                print(f'fixed UI List:{UI.l}')
                print(f'selection={selection[0]}')
                
                UI.l.pop()
                print(f'popped list={UI.l}')
                self.the_data.plot_data()
                
        print(f'c={c}')
            
           
            
    def set_directory(self,selectedFile):
        """Changes the initialdir for the filedialog window and uses the same directory for files saved."""
        
        filename=selectedFile.split(sep='/')[-1]
        print(f'filename:{filename}')
        
        self.the_dir=selectedFile.split(sep=filename)
        print(f'the_dir:{self.the_dir}')
        
        UI.initialdir=self.the_dir[0]
        UI.filename=filename

        return UI.initialdir+UI.filename



#------FUNCTIONS-------FUNCTIONS-------FUNCTIONS--------FUNCTIONS----------------------

def view_the_file():

    path=UI.initialdir+UI.filename
    print(f'complete path:{path}')
    os.startfile(path)
##    subprocess.Popen('C:\Windows\System32\notepad.exe',path)
    
        
def clear_plot_variables():
    """Clears the plot variable list"""
    UI.l.clear()




#------MAIN-------MAIN-------MAIN------------------------------

if __name__ == '__main__':
    UserInterface()


    

