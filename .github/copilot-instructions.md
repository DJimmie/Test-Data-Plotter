# Copilot Instructions for Test-Data-Plotter

## Project Overview
A CSV data visualization tool with matplotlib backends and multiple interfaces (Tkinter GUI, Streamlit web app). Focuses on time series plotting with automatic datetime detection and dual y-axis support.

## Architecture

**Core Design**: Single `TestData` class wraps pandas DataFrame and provides data operations + plotting methods.

**Key Data Flow**:
1. CSV loaded → Datetime detection (tries: Date+Time columns, unix timestamps, datetime columns)
2. Columns auto-parsed to numeric where possible
3. User selects 1-2 columns via UI → `TestData` renders matplotlib plots
4. Optional dual y-axis support for 2-column selections

**Entry Points**:
- [main.py](main.py) — Tkinter GUI (desktop app)
- [main_with_streamlit.py](main_with_streamlit.py) — Streamlit web interface

## Critical Patterns

### Datetime Handling
The project implements sophisticated datetime detection across multiple formats:
- **Unix timestamps**: `timestamp` column (ms) → converted via `pd.to_datetime(unit='ms')`
- **Separate Date+Time**: Combines columns, tries 8 format variations before fallback
- **Direct datetime columns**: Auto-detected via `pd.api.types.is_datetime64_any_dtype()`

Keep datetime fallback logic: if parsing fails, gracefully use index instead of crashing.

### Plotting Pattern
All plots use `matplotlib` with `'ggplot'` style. Standard workflow in `TestData.plot_data()`:
1. Resolve x-axis: use `x_value` (datetime) or `data_index` (fallback)
2. Create figure + optionally twin y-axis for 2nd series
3. Apply labels, legend, title
4. Pass to `plt.show()` (Tkinter) or `st.pyplot(fig)` (Streamlit)

### UI Selection Pattern
Both interfaces follow identical logic:
- Multi-select listbox/dropdown for column selection
- Validate: 1-2 columns only (show warning if violated)
- Display min/max stats after plotting
- Provide datetime checkbox to toggle x-axis mode

## Adding New Plot Types
To add histogram/box-plot support:

1. **Add method to `TestData`**: e.g., `def plot_histogram(self, column):`
2. **Keep signature consistent**: Accept column names + optional parameters (bins, orientation)
3. **Return figure objects** rather than calling `plt.show()` directly (allows Streamlit integration)
4. **Use same color/style scheme**: `'ggplot'` style, blues for first series
5. **Update UI**: Add buttons/options in both `main.py` and `main_with_streamlit.py`

## Dependencies
- `pandas`: Data loading + numeric conversions
- `matplotlib`: Rendering (uses `'ggplot'` style)
- `tkinter`: Desktop GUI
- `streamlit`: Web interface

## Testing Workflow
Quick verify after changes:
- Test with CSV containing datetime (should auto-detect)
- Test with unix timestamp column
- Test multi-column selections
- Verify both Tkinter and Streamlit interfaces
