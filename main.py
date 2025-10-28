# --- main.py ---

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, messagebox
import datetime as dt




class TestData:
    def __init__(self, datafile):
        self.datafile = datafile
        self.data = pd.read_csv(datafile)
        self.data['data_index'] = range(len(self.data))
        self.x_value = None
        self.y_value = None
        self.x_is_datetime = False
        self.parse_datetime_column()
        self.create_datetime_column_if_needed()
        self.update_available_columns()

    def parse_datetime_column(self):
        """Check if there is a column that can be parsed as datetime."""
        for col in self.data.columns:
            try:
                self.data[col] = pd.to_datetime(self.data[col], errors='ignore')
                if pd.api.types.is_datetime64_any_dtype(self.data[col]):
                    self.x_is_datetime = True
                    self.x_value = col
                    break
            except:
                continue

    def create_datetime_column_if_needed(self):
        """Create a 'Datetime' column if 'timestamp' column is detected as Unix timestamp."""
        if 'timestamp' in self.data.columns and pd.api.types.is_integer_dtype(self.data['timestamp']):
            self.data['Datetime'] = pd.to_datetime(self.data['timestamp'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
            self.x_value = 'Datetime'
            self.x_is_datetime = True

    def update_available_columns(self):
        """Update available columns for plotting."""
        self.available_columns = self.data.columns.tolist()
        if 'Datetime' in self.available_columns:
            self.x_is_datetime = True
            self.x_value = 'Datetime'

    def plot_data(self, y_value_2=None):
        """Plot data with options for single or dual y-axes."""
        plt.style.use('ggplot')
        
        if self.x_is_datetime and self.x_value:
            x_data = self.data[self.x_value]
            x_label = self.x_value
        else:
            x_data = self.data['data_index']
            x_label = 'Index'
        
        fig, ax1 = plt.subplots(figsize=(15, 10))

        if y_value_2:
            ax2 = ax1.twinx()
            ax1.plot(self.data[x_data.name], self.data[self.y_value], 'b-', label=self.y_value)
            ax2.plot(self.data[x_data.name], self.data[y_value_2], 'r--', label=y_value_2)
            ax1.set_ylabel(self.y_value, color='b')
            ax2.set_ylabel(y_value_2, color='r')
            ax1.legend(loc='upper left')
            ax2.legend(loc='upper right')
        else:
            ax1.plot(self.data[x_data.name], self.data[self.y_value], 'b-', label=self.y_value)
            ax1.set_ylabel(self.y_value, color='b')
            ax1.legend(loc='upper left')

        ax1.set_xlabel(x_label)
        plt.title(f'Plot of {self.y_value}{" and " + y_value_2 if y_value_2 else ""}')
        plt.show()

    def get_min_max(self, column):
        """Get min and max values for a specified column."""
        return self.data[column].min(), self.data[column].max()

class UserInterface(Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Plotter")
        self.geometry("600x500")
        self.data = None
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the UI."""
        self.file_label = Label(self, text="Select Data File:")
        self.file_label.pack(pady=10)
        
        self.open_button = Button(self, text="Open File", command=self.open_file)
        self.open_button.pack(pady=10)
        
        self.column_list = Listbox(self, selectmode=MULTIPLE)
        self.column_list.pack(pady=10, fill=BOTH, expand=True)

        self.use_datetime_var = IntVar()
        self.use_datetime_checkbox = Checkbutton(self, text="Use 'Datetime' for X-Axis", variable=self.use_datetime_var)
        self.use_datetime_checkbox.pack(pady=10)

        self.plot_button = Button(self, text="Plot Data", command=self.plot_data)
        self.plot_button.pack(pady=10)
        
        self.info_label = Label(self, text="")
        self.info_label.pack(pady=10)

    def open_file(self):
        """Open the file dialog and load the selected file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        self.data = TestData(file_path)
        self.update_column_list()
        self.update_datetime_option()

    def update_column_list(self):
        """Update the listbox with column names from the loaded data."""
        self.column_list.delete(0, END)
        for col in self.data.available_columns:
            self.column_list.insert(END, col)
    
    def update_datetime_option(self):
        """Show or hide the 'Datetime' option based on available columns."""
        if 'Datetime' in self.data.available_columns:
            self.use_datetime_checkbox.config(state=NORMAL)
            self.use_datetime_var.set(1 if self.data.x_is_datetime else 0)
        else:
            self.use_datetime_checkbox.config(state=DISABLED)
            self.use_datetime_var.set(0)

    def plot_data(self):
        """Plot the data based on user selections."""
        selected_indices = self.column_list.curselection()
        selected_columns = [self.column_list.get(i) for i in selected_indices]
        
        if not selected_columns:
            messagebox.showwarning("Selection Error", "Please select at least one column.")
            return
        
        if len(selected_columns) > 2:
            messagebox.showwarning("Selection Error", "Please select up to 2 columns.")
            return

        if len(selected_columns) == 1:
            self.data.y_value = selected_columns[0]
            self.data.plot_data()
            min_val, max_val = self.data.get_min_max(self.data.y_value)
            self.info_label.config(text=f"{self.data.y_value}: Min={min_val}, Max={max_val}")
        elif len(selected_columns) == 2:
            self.data.y_value = selected_columns[0]
            self.data.plot_data(selected_columns[1])
            min_val1, max_val1 = self.data.get_min_max(self.data.y_value)
            min_val2, max_val2 = self.data.get_min_max(selected_columns[1])
            self.info_label.config(text=f"{self.data.y_value}: Min={min_val1}, Max={max_val1}\n{selected_columns[1]}: Min={min_val2}, Max={max_val2}")

if __name__ == "__main__":
    ui = UserInterface()
    ui.mainloop()

