# --- streamlit_app.py ---
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# === Class Definition ===
class TestData:
    def __init__(self, datafile, header=0):
        self.datafile = datafile
        self.data = pd.read_csv(datafile, header=header)
        self.data['data_index'] = range(len(self.data))
        self.x_value = None
        self.y_value = None
        self.x_is_datetime = False
        self.combine_date_time_columns()
        self.parse_datetime_column()
        self.create_datetime_column_if_needed()
        self.update_available_columns()

    def combine_date_time_columns(self):
        """Combine 'Date' and 'Time' columns if both exist and auto-detect datetime format."""
        if "Date" in self.data.columns and "Time" in self.data.columns:
            datetime_series = self.data["Date"].astype(str) + " " + self.data["Time"].astype(str)

            # Common datetime formats to try
            possible_formats = [
                "%Y-%m-%d %H:%M:%S",
                "%m/%d/%Y %H:%M:%S",
                "%d/%m/%Y %H:%M:%S",
                "%y-%m-%d %H:%M:%S",
                "%m/%d/%y %H:%M:%S",
                "%d/%m/%y %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%m/%d/%Y %H:%M",
            ]

            for fmt in possible_formats:
                try:
                    self.data["datetime_stamp"] = pd.to_datetime(datetime_series, format=fmt, errors="raise")
                    self.x_is_datetime = True
                    self.x_value = "datetime_stamp"
                    return  # stop at the first successful parse
                except Exception:
                    continue

            # Fallback if none of the formats worked
            try:
                self.data["datetime_stamp"] = pd.to_datetime(datetime_series, errors="coerce")
                if self.data["datetime_stamp"].notna().any():
                    self.x_is_datetime = True
                    self.x_value = "datetime_stamp"
                else:
                    raise ValueError("Datetime parsing failed for all formats.")
            except Exception as e:
                st.warning(f"⚠️ Failed to format Date and Time columns automatically: {e}")
                self.x_is_datetime = False
                self.x_value = "data_index"

    def parse_datetime_column(self):
        """Detect any pre-existing datetime-like column."""
        for col in self.data.columns:
            try:
                self.data[col] = pd.to_datetime(self.data[col], errors="ignore")
                if pd.api.types.is_datetime64_any_dtype(self.data[col]):
                    self.x_is_datetime = True
                    self.x_value = col
                    break
            except Exception:
                continue

    def create_datetime_column_if_needed(self):
        """Create a 'Datetime' column if Unix timestamp detected."""
        if "timestamp" in self.data.columns and pd.api.types.is_integer_dtype(self.data["timestamp"]):
            self.data["Datetime"] = pd.to_datetime(self.data["timestamp"], unit="ms")
            self.x_value = "Datetime"
            self.x_is_datetime = True

    def update_available_columns(self):
        """Update list of available columns."""
        self.available_columns = self.data.columns.tolist()
        if "datetime_stamp" in self.available_columns:
            self.x_is_datetime = True
            self.x_value = "datetime_stamp"

    def get_min_max(self, column):
        """Get min and max values for any numeric column."""
        return self.data[column].min(), self.data[column].max()
    
    def get_stats(self, column):
        """Get statistical values (min, max, mean, std) for a specified column."""
        data_numeric = pd.to_numeric(self.data[column], errors="coerce").dropna()
        return {
            'min': data_numeric.min(),
            'max': data_numeric.max(),
            'mean': data_numeric.mean(),
            'std': data_numeric.std()
        }

    def plot_histogram(self, column, bins=30):
        """Plot histogram for a specified column."""
        plt.style.use("ggplot")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Convert to numeric, handling non-numeric values
        data_numeric = pd.to_numeric(self.data[column], errors="coerce").dropna()
        
        ax.hist(data_numeric, bins=bins, color="steelblue", edgecolor="black", alpha=0.7)
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        ax.set_title(f"Histogram of {column}")
        
        return fig

    def plot_box_plot(self, *columns):
        """Plot box and whisker plot for one or more columns and annotate stats."""
        plt.style.use("ggplot")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Prepare data for box plot
        box_data = []
        labels = []
        stats_list = []
        for col in columns:
            # Convert to numeric, handling non-numeric values
            data_numeric = pd.to_numeric(self.data[col], errors="coerce").dropna()
            box_data.append(data_numeric)
            labels.append(col)
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
        ax.set_ylabel("Values")
        ax.set_title(f"Box Plot of {', '.join(columns)}")
        
        # Color the boxes
        colors = ["lightblue", "lightcoral", "lightgreen", "lightyellow"]
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        
        # annotate stats
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
        
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        return fig

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


# === Streamlit App Logic ===
st.title("📊 CSV Data Plotter (Auto DateTime Detection)")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], key="csv_uploader")

if uploaded_file:
    header_row = st.number_input("Header Row (0-based)", min_value=0, value=0, step=1, key="header_row")
    data_instance = TestData(uploaded_file, header=header_row)
    st.success(f"✅ File '{uploaded_file.name}' loaded successfully!")

    # Display data preview
    with st.expander("Preview Data"):
        st.dataframe(data_instance.data.head())

    # Select plot type
    st.write("### Select Plot Type")
    plot_type = st.radio("Choose a plot type:", ["Line Plot", "Scatter Plot", "Histogram", "Box Plot"])

    # Select columns to plot
    st.write("### Select Columns to Plot")
    columns = data_instance.available_columns
    
    if plot_type == "Histogram":
        selected_columns = st.multiselect("Select 1 column for histogram", columns, max_selections=1)
    elif plot_type == "Box Plot":
        selected_columns = st.multiselect("Select up to 4 columns for box plot", columns, max_selections=4)
    elif plot_type == "Scatter Plot":
        selected_columns = st.multiselect("Select up to 4 columns for scatter plot", columns, max_selections=4)
    else:  # Line Plot
        selected_columns = st.multiselect("Select up to 4 columns for line plot", columns, max_selections=4)

    # Checkbox for datetime x-axis (only for line plot)
    use_datetime = False
    if plot_type == "Line Plot":
        use_datetime = st.checkbox(
            "Use datetime column for X-axis (if available)",
            value=data_instance.x_is_datetime,
        )

    # Plot button
    if st.button("Generate Plot"):
        if not selected_columns:
            st.warning(f"Please select at least one column for {plot_type.lower()}.")
        elif plot_type == "Histogram" and len(selected_columns) != 1:
            st.warning("Please select exactly 1 column for histogram.")
        elif plot_type in ["Line Plot", "Box Plot", "Scatter Plot"] and len(selected_columns) > 4:
            st.warning(f"Please select no more than 4 columns for {plot_type.lower()}.")
        else:
            # determine share flag
            share_y = False
            if len(selected_columns) == 2:
                share_y = st.checkbox("Share Y-axis for two columns", value=False, key="share_axis")
            elif len(selected_columns) > 2:
                share_y = True

            if plot_type == "Histogram":
                fig = data_instance.plot_histogram(selected_columns[0])
                st.pyplot(fig)
                
                # Show statistics
                st.write("### Value Summary")
                stats = data_instance.get_stats(selected_columns[0])
                st.write(f"**{selected_columns[0]}** — Min: `{stats['min']:.2f}`, Max: `{stats['max']:.2f}`, Avg: `{stats['mean']:.2f}`, Std: `{stats['std']:.2f}`")
            
            elif plot_type == "Box Plot":
                fig = data_instance.plot_box_plot(*selected_columns)
                st.pyplot(fig)
                
                # Show statistics
                st.write("### Value Summary")
                for col in selected_columns:
                    stats = data_instance.get_stats(col)
                    st.write(f"**{col}** — Min: `{stats['min']:.2f}`, Max: `{stats['max']:.2f}`, Avg: `{stats['mean']:.2f}`, Std: `{stats['std']:.2f}`")
            
            elif plot_type == "Scatter Plot":
                # if user chose to override x-axis we still modify the instance
                if use_datetime and data_instance.x_is_datetime and data_instance.x_value in data_instance.data.columns:
                    pass  # instance already configured
                else:
                    st.info("⚙️ Using index for X-axis (no valid datetime found).")
                    data_instance.x_is_datetime = False

                fig = data_instance.plot_scatter(selected_columns, share_y=share_y)
                st.pyplot(fig)

                # Show statistics
                st.write("### Value Summary")
                for col in selected_columns:
                    stats = data_instance.get_stats(col)
                    st.write(f"**{col}** — Min: `{stats['min']:.2f}`, Max: `{stats['max']:.2f}`, Avg: `{stats['mean']:.2f}`, Std: `{stats['std']:.2f}")
            
            else:  # Line Plot
                if use_datetime and data_instance.x_is_datetime and data_instance.x_value in data_instance.data.columns:
                    pass
                else:
                    st.info("⚙️ Using index for X-axis (no valid datetime found).")
                    data_instance.x_is_datetime = False

                fig = data_instance.plot_data(selected_columns, share_y=share_y)
                st.pyplot(fig)

                # Show statistics
                st.write("### Value Summary")
                for col in selected_columns:
                    stats = data_instance.get_stats(col)
                    st.write(f"**{col}** — Min: `{stats['min']:.2f}`, Max: `{stats['max']:.2f}`, Avg: `{stats['mean']:.2f}`, Std: `{stats['std']:.2f}")
