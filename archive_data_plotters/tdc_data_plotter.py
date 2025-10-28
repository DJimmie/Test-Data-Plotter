import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.process_data()

    def process_data(self):
        """Process the data as specified."""
        # Open the file and skip the first 9 rows
        with open(self.file_path, 'r') as file:
            # Read the data, skipping the first 9 rows
            lines = file.readlines()[9:]

        # Load the remaining data into a DataFrame
        from io import StringIO
        data_str = ''.join(lines)
        self.data = pd.read_csv(StringIO(data_str))

        # Print to check the DataFrame
        print("DataFrame after removing the first 9 rows:")
        print(self.data.head())

        # Remove columns named 'UNUSED'
        self.data = self.data.loc[:, self.data.columns != 'UNUSED']
        
        # Convert 'Date' column to 'YYYY-MM-DD' format
        if 'Date' in self.data.columns:
            self.data['Date'] = pd.to_datetime(self.data['Date'], format='%m/%d/%y').dt.strftime('%Y-%m-%d') 

        # Create 'datetime' column combining 'Date' and 'Time'
        if 'Date' in self.data.columns and 'Time' in self.data.columns:
            self.data['datetime'] = pd.to_datetime(self.data['Date'] + ' ' + self.data['Time'], format='%Y-%m-%d %H:%M:%S.%f')

        # Create 'unix_timestamp' column
        if 'datetime' in self.data.columns:
            self.data['unix_timestamp'] = self.data['datetime'].apply(lambda dt: int(dt.timestamp() * 1000))

        # Set available_columns attribute
        self.available_columns = self.data.columns.tolist()

class UserInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Plotter")
        self.geometry("600x500")
        self.data_processor = None
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the UI."""
        self.file_label = tk.Label(self, text="Select Data File:")
        self.file_label.pack(pady=10)
        
        self.open_button = tk.Button(self, text="Open File", command=self.open_file)
        self.open_button.pack(pady=10)
        
        self.column_list = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.column_list.pack(pady=10, fill=tk.BOTH, expand=True)

        self.plot_button = tk.Button(self, text="Plot Data", command=self.plot_data)
        self.plot_button.pack(pady=10)
        
        self.info_label = tk.Label(self, text="")
        self.info_label.pack(pady=10)

    def open_file(self):
        """Open the file dialog and load the selected file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            self.data_processor = DataProcessor(file_path)
            self.update_column_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {e}")
            print(e)

    def update_column_list(self):
        """Update the listbox with column names from the loaded data."""
        if self.data_processor and self.data_processor.available_columns:
            self.column_list.delete(0, tk.END)
            for col in self.data_processor.available_columns:
                self.column_list.insert(tk.END, col)

    def plot_data(self):
        """Plot the data based on user selections."""
        if not self.data_processor:
            messagebox.showwarning("Selection Error", "No data loaded.")
            return

        selected_indices = self.column_list.curselection()
        selected_columns = [self.column_list.get(i) for i in selected_indices]

        if not selected_columns:
            messagebox.showwarning("Selection Error", "Please select at least one column.")
            return

        if len(selected_columns) > 2:
            messagebox.showwarning("Selection Error", "Please select up to 2 columns.")
            return

        # Extract data from the DataProcessor
        data = self.data_processor.data

        # Determine x and y columns
        x_col = 'datetime'  # Use 'datetime' column for x-axis if available
        y_col1 = selected_columns[0]
        y_col2 = selected_columns[1] if len(selected_columns) == 2 else None

        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Plot the first y-axis column
        ax1.plot(data[x_col], data[y_col1], 'b-', label=y_col1)
        ax1.set_xlabel('Datetime')
        ax1.set_ylabel(y_col1, color='b')
        ax1.tick_params(axis='y', labelcolor='b')

        # Plot the second y-axis column if provided
        if y_col2:
            ax2 = ax1.twinx()
            ax2.plot(data[x_col], data[y_col2], 'r--', label=y_col2)
            ax2.set_ylabel(y_col2, color='r')
            ax2.tick_params(axis='y', labelcolor='r')

        # Format the x-axis with date formatting
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45)
        
        # Add legends
        if y_col2:
            ax1.legend(loc='upper left')
            ax2.legend(loc='upper right')
        else:
            ax1.legend(loc='upper left')

        plt.title(f'Plot of {y_col1}' + (f' and {y_col2}' if y_col2 else ''))
        plt.grid()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    ui = UserInterface()
    ui.mainloop()
