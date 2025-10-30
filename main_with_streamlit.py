# --- streamlit_app.py ---
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# === Class Definition ===
class TestData:
    def __init__(self, datafile):
        self.datafile = datafile
        self.data = pd.read_csv(datafile)
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


# === Streamlit App Logic ===
st.title("📊 CSV Data Plotter (Auto DateTime Detection)")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], key="csv_uploader")

if uploaded_file:
    data_instance = TestData(uploaded_file)
    st.success(f"✅ File '{uploaded_file.name}' loaded successfully!")

    # Display data preview
    with st.expander("Preview Data"):
        st.dataframe(data_instance.data.head())

    # Select columns to plot
    st.write("### Select Columns to Plot")
    columns = data_instance.available_columns
    selected_columns = st.multiselect("Select up to 2 columns to plot", columns)

    # Checkbox for datetime x-axis
    use_datetime = st.checkbox(
        "Use datetime column for X-axis (if available)",
        value=data_instance.x_is_datetime,
    )

    # Plot button
    if st.button("Generate Plot"):
        if not selected_columns:
            st.warning("Please select at least one column to plot.")
        elif len(selected_columns) > 2:
            st.warning("Please select up to 2 columns only.")
        else:
            plt.style.use("ggplot")

            # Choose X-axis
            if use_datetime and data_instance.x_is_datetime and data_instance.x_value in data_instance.data.columns:
                x_data = data_instance.data[data_instance.x_value]
                x_label = data_instance.x_value
            else:
                st.info("⚙️ Using index for X-axis (no valid datetime found).")
                x_data = data_instance.data["data_index"]
                x_label = "Index"

            fig, ax1 = plt.subplots(figsize=(10, 6))

            # Convert Y columns to numeric safely
            for col in selected_columns:
                data_instance.data[col] = pd.to_numeric(data_instance.data[col], errors="coerce")

            if len(selected_columns) == 2:
                ax2 = ax1.twinx()
                ax1.plot(x_data, data_instance.data[selected_columns[0]], "b-", label=selected_columns[0])
                ax2.plot(x_data, data_instance.data[selected_columns[1]], "r--", label=selected_columns[1])
                ax1.set_ylabel(selected_columns[0], color="b")
                ax2.set_ylabel(selected_columns[1], color="r")
                ax1.legend(loc="upper left")
                ax2.legend(loc="upper right")
            else:
                ax1.plot(x_data, data_instance.data[selected_columns[0]], "b-", label=selected_columns[0])
                ax1.set_ylabel(selected_columns[0], color="b")
                ax1.legend(loc="upper left")

            ax1.set_xlabel(x_label)
            plt.title(f"Plot of {', '.join(selected_columns)}")

            st.pyplot(fig)

            # Show min/max values
            st.write("### Value Summary")
            for col in selected_columns:
                min_val, max_val = data_instance.get_min_max(col)
                st.write(f"**{col}** — Min: `{min_val}`, Max: `{max_val}`")
