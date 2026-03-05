# --- main.py ---

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, messagebox
import datetime as dt




class TestData:
    def __init__(self, datafile, header=0):
        self.datafile = datafile
        self.data = pd.read_csv(datafile, header=header)
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

    def plot_data(self, y_values=None, share_y=False):
        """Plot data for one to four columns.

        y_values may be a list of column names or a single name.  If two
        values are provided the caller can request a shared y-axis by
        setting ``share_y``; otherwise a twin y-axis will be used.  When
        three or four columns are plotted they always share the same axis.
        """
        plt.style.use('ggplot')

        # normalize input
        if y_values is None:
            y_values = [self.y_value] if self.y_value else []
        elif isinstance(y_values, str):
            y_values = [y_values]
        else:
            y_values = list(y_values)

        if self.x_is_datetime and self.x_value:
            x_data = self.data[self.x_value]
            x_label = self.x_value
        else:
            x_data = self.data['data_index']
            x_label = 'Index'

        fig, ax1 = plt.subplots(figsize=(15, 10))
        x_series = self.data[x_data.name] if hasattr(x_data, 'name') else x_data

        # plotting logic depending on number of series
        n = len(y_values)
        if n == 0:
            return fig
        elif n == 1:
            ax1.plot(x_series, self.data[y_values[0]], 'b-', label=y_values[0])
            ax1.set_ylabel(y_values[0], color='b')
            ax1.legend(loc='upper left')
        elif n == 2:
            if share_y:
                colors = ['b', 'r']
                for col, color in zip(y_values, colors):
                    ax1.plot(x_series, self.data[col], color + '-', label=col)
                ax1.set_ylabel(', '.join(y_values), color='b')
                ax1.legend(loc='upper left')
            else:
                ax2 = ax1.twinx()
                ax1.plot(x_series, self.data[y_values[0]], 'b-', label=y_values[0])
                ax2.plot(x_series, self.data[y_values[1]], 'r--', label=y_values[1])
                ax1.set_ylabel(y_values[0], color='b')
                ax2.set_ylabel(y_values[1], color='r')
                ax1.legend(loc='upper left')
                ax2.legend(loc='upper right')
        else:  # 3 or 4 series
            colors = ['b', 'r', 'g', 'm']
            for col, color in zip(y_values, colors):
                ax1.plot(x_series, self.data[col], color + '-', label=col)
            ax1.set_ylabel('Values', color='b')
            ax1.legend(loc='upper left')

        ax1.set_xlabel(x_label)
        plt.title(f"Plot of {', '.join(y_values)}")
        return fig

    def plot_scatter(self, y_values=None, share_y=False):
        """Scatter plot for up to four columns.

        y_values normalized similarly to :meth:`plot_data` above.  Sharing of the
        y-axis follows the same rules as the line plot.
        """
        plt.style.use('ggplot')
        if self.x_is_datetime and self.x_value:
            x_data = self.data[self.x_value]
            x_label = self.x_value
        else:
            x_data = self.data['data_index']
            x_label = 'Index'
        
        fig, ax1 = plt.subplots(figsize=(15, 10))
        x_series = self.data[x_data.name] if hasattr(x_data, 'name') else x_data

        # normalize y_values
        if y_values is None:
            y_values = [self.y_value] if self.y_value else []
        elif isinstance(y_values, str):
            y_values = [y_values]
        else:
            y_values = list(y_values)

        n = len(y_values)
        if n == 0:
            return fig
        elif n == 1:
            ax1.scatter(x_series, self.data[y_values[0]], c='b', label=y_values[0])
            ax1.set_ylabel(y_values[0], color='b')
            ax1.legend(loc='upper left')
        elif n == 2:
            if share_y:
                colors = ['b', 'r']
                for col, color in zip(y_values, colors):
                    ax1.scatter(x_series, self.data[col], c=color, label=col)
                ax1.set_ylabel(', '.join(y_values), color='b')
                ax1.legend(loc='upper left')
            else:
                ax2 = ax1.twinx()
                ax1.scatter(x_series, self.data[y_values[0]], c='b', label=y_values[0])
                ax2.scatter(x_series, self.data[y_values[1]], c='r', label=y_values[1])
                ax1.set_ylabel(y_values[0], color='b')
                ax2.set_ylabel(y_values[1], color='r')
                ax1.legend(loc='upper left')
                ax2.legend(loc='upper right')
        else:
            colors = ['b', 'r', 'g', 'm']
            for col, color in zip(y_values, colors):
                ax1.scatter(x_series, self.data[col], c=color, label=col)
            ax1.set_ylabel('Values', color='b')
            ax1.legend(loc='upper left')

        ax1.set_xlabel(x_label)
        plt.title(f"Scatter of {', '.join(y_values)}")
        return fig

    def plot_histogram(self, column, bins=30):
        """Plot histogram for a specified column."""
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Convert to numeric, handling non-numeric values
        data_numeric = pd.to_numeric(self.data[column], errors='coerce').dropna()
        
        ax.hist(data_numeric, bins=bins, color='steelblue', edgecolor='black', alpha=0.7)
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        ax.set_title(f'Histogram of {column}')
        return fig

    def plot_box_plot(self, *columns):
        """Plot box and whisker plot for one or more columns and annotate stats."""
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Prepare data for box plot
        box_data = []
        labels = []
        stats_list = []  # list of dicts for annotation
        for col in columns:
            # Convert to numeric, handling non-numeric values
            data_numeric = pd.to_numeric(self.data[col], errors='coerce').dropna()
            box_data.append(data_numeric)
            labels.append(col)
            # compute stats
            desc = data_numeric.describe()
            stats_list.append({
                'min': desc['min'],
                'q1': data_numeric.quantile(0.25),
                'median': desc['50%'],
                'q3': data_numeric.quantile(0.75),
                'max': desc['max'],
                'mean': desc['mean'],
                'std': data_numeric.std(),
            })
        
        bp = ax.boxplot(box_data, labels=labels, patch_artist=True)
        ax.set_ylabel('Values')
        ax.set_title(f'Box Plot of {", ".join(columns)}')
        
        # Color the boxes
        colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightyellow']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        
        # annotate each box with stats
        for i, stats in enumerate(stats_list, start=1):
            text_x = i + 0.1
            lines = [
                f"Min: {stats['min']:.2f}",
                f"Q1: {stats['q1']:.2f}",
                f"Median: {stats['median']:.2f}",
                f"Q3: {stats['q3']:.2f}",
                f"Max: {stats['max']:.2f}",
                f"Avg: {stats['mean']:.2f}",
                f"Std: {stats['std']:.2f}",
            ]
            ax.text(text_x, stats['max'], "\n".join(lines), fontsize=8, va='top')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def get_min_max(self, column):
        """Get min and max values for a specified column."""
        return self.data[column].min(), self.data[column].max()
    
    def get_stats(self, column):
        """Get statistical values (min, max, mean, std) for a specified column."""
        data_numeric = pd.to_numeric(self.data[column], errors='coerce').dropna()
        return {
            'min': data_numeric.min(),
            'max': data_numeric.max(),
            'mean': data_numeric.mean(),
            'std': data_numeric.std()
        }

class UserInterface(Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Plotter")
        self.geometry("700x600")
        self.data = None
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the UI."""
        self.file_label = Label(self, text="Select Data File:")
        self.file_label.pack(pady=10)
        
        self.open_button = Button(self, text="Open File", command=self.open_file)
        self.open_button.pack(pady=10)
        
        self.header_label = Label(self, text="Header Row (0-based):")
        self.header_label.pack(pady=5)
        
        self.header_entry = Entry(self)
        self.header_entry.insert(0, "0")
        self.header_entry.pack(pady=5)
        
        self.column_list = Listbox(self, selectmode=MULTIPLE)
        self.column_list.pack(pady=10, fill=BOTH, expand=True)

        self.use_datetime_var = IntVar()
        self.use_datetime_checkbox = Checkbutton(self, text="Use 'Datetime' for X-Axis", variable=self.use_datetime_var)
        self.use_datetime_checkbox.pack(pady=10)

        self.share_axis_var = IntVar()
        self.share_axis_checkbox = Checkbutton(self, text="Share Y-axis for two columns", variable=self.share_axis_var)
        self.share_axis_checkbox.pack(pady=5)

        # Plot type selection frame
        button_frame = Frame(self)
        button_frame.pack(pady=10)

        self.plot_button = Button(button_frame, text="Line Plot", command=self.plot_line)
        self.plot_button.grid(row=0, column=0, padx=5)
        
        self.scatter_button = Button(button_frame, text="Scatter Plot", command=self.plot_scatter_ui)
        self.scatter_button.grid(row=0, column=1, padx=5)
        
        self.histogram_button = Button(button_frame, text="Histogram", command=self.plot_histogram_ui)
        self.histogram_button.grid(row=0, column=2, padx=5)
        
        self.boxplot_button = Button(button_frame, text="Box Plot", command=self.plot_boxplot_ui)
        self.boxplot_button.grid(row=0, column=3, padx=5)
        
        self.info_label = Label(self, text="")
        self.info_label.pack(pady=10)

    def open_file(self):
        """Open the file dialog and load the selected file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            header_row = int(self.header_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Header row must be an integer.")
            return

        self.data = TestData(file_path, header=header_row)
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

    def plot_line(self):
        """Plot line chart for selected columns."""
        selected_indices = self.column_list.curselection()
        selected_columns = [self.column_list.get(i) for i in selected_indices]
        
        if not selected_columns:
            messagebox.showwarning("Selection Error", "Please select at least one column.")
            return
        
        if len(selected_columns) > 4:
            messagebox.showwarning("Selection Error", "Please select no more than 4 columns for line plot.")
            return

        # determine share flag; only relevant when exactly two
        share_flag = bool(self.share_axis_var.get()) if len(selected_columns) == 2 else True if len(selected_columns) > 2 else False

        if len(selected_columns) == 1:
            self.data.y_value = selected_columns[0]
            fig = self.data.plot_data()
            plt.show()
            stats = self.data.get_stats(self.data.y_value)
            self.info_label.config(text=f"{self.data.y_value}: Min={stats['min']:.2f}, Max={stats['max']:.2f}, Avg={stats['mean']:.2f}, Std={stats['std']:.2f}")
        else:
            self.data.y_value = selected_columns[0]
            fig = self.data.plot_data(selected_columns, share_y=share_flag)
            plt.show()
            # gather stats for all columns
            stats_text = ""
            for col in selected_columns:
                s = self.data.get_stats(col)
                stats_text += f"{col}: Min={s['min']:.2f}, Max={s['max']:.2f}, Avg={s['mean']:.2f}, Std={s['std']:.2f}\n"
            self.info_label.config(text=stats_text.strip())

    def plot_scatter_ui(self):
        """Plot scatter chart for selected columns."""
        selected_indices = self.column_list.curselection()
        selected_columns = [self.column_list.get(i) for i in selected_indices]
        
        if not selected_columns:
            messagebox.showwarning("Selection Error", "Please select at least one column.")
            return
        
        if len(selected_columns) > 4:
            messagebox.showwarning("Selection Error", "Please select no more than 4 columns for scatter plot.")
            return

        share_flag = bool(self.share_axis_var.get()) if len(selected_columns) == 2 else True if len(selected_columns) > 2 else False

        if len(selected_columns) == 1:
            self.data.y_value = selected_columns[0]
            fig = self.data.plot_scatter()
            plt.show()
            stats = self.data.get_stats(self.data.y_value)
            self.info_label.config(text=f"{self.data.y_value}: Min={stats['min']:.2f}, Max={stats['max']:.2f}, Avg={stats['mean']:.2f}, Std={stats['std']:.2f}")
        else:
            self.data.y_value = selected_columns[0]
            fig = self.data.plot_scatter(selected_columns, share_y=share_flag)
            plt.show()
            stats_text = ""
            for col in selected_columns:
                s = self.data.get_stats(col)
                stats_text += f"{col}: Min={s['min']:.2f}, Max={s['max']:.2f}, Avg={s['mean']:.2f}, Std={s['std']:.2f}\n"
            self.info_label.config(text=stats_text.strip())
    def plot_histogram_ui(self):
        """Plot histogram for selected column."""
        selected_indices = self.column_list.curselection()
        selected_columns = [self.column_list.get(i) for i in selected_indices]
        
        if not selected_columns:
            messagebox.showwarning("Selection Error", "Please select a column.")
            return
        
        if len(selected_columns) > 1:
            messagebox.showwarning("Selection Error", "Please select only 1 column for histogram.")
            return

        column = selected_columns[0]
        fig = self.data.plot_histogram(column)
        plt.show()
        stats = self.data.get_stats(column)
        self.info_label.config(text=f"{column}: Min={stats['min']:.2f}, Max={stats['max']:.2f}, Avg={stats['mean']:.2f}, Std={stats['std']:.2f}")

    def plot_boxplot_ui(self):
        """Plot box and whisker plot for selected columns."""
        selected_indices = self.column_list.curselection()
        selected_columns = [self.column_list.get(i) for i in selected_indices]
        
        if not selected_columns:
            messagebox.showwarning("Selection Error", "Please select at least one column.")
            return
        
        if len(selected_columns) > 4:
            messagebox.showwarning("Selection Error", "Please select no more than 4 columns for box plot.")
            return

        fig = self.data.plot_box_plot(*selected_columns)
        plt.show()
        
        # Display stats for all selected columns
        stats_text = ""
        for col in selected_columns:
            stats = self.data.get_stats(col)
            stats_text += f"{col}: Min={stats['min']:.2f}, Max={stats['max']:.2f}, Avg={stats['mean']:.2f}, Std={stats['std']:.2f}\n"
        
        self.info_label.config(text=stats_text.strip())

if __name__ == "__main__":
    ui = UserInterface()
    ui.mainloop()

