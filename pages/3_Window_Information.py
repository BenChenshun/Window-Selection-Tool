import streamlit as st
from preprocessing import *
import pandas as pd
from utils import Back_to_House, Go_to_Result

# Path to the default window database file
DEFAULT_WINDOW_DATABASE_PATH = 'data/window_data.csv'

# Display default window database
# st.write("### Default Window Database:")
default_window_database = pd.read_csv(DEFAULT_WINDOW_DATABASE_PATH)
default_window_database["window_name"] = default_window_database["window_type"]
# st.write(default_window_database)

st.title("Specify Window Details")

# Window-Wall Ratio
st.write(f"**Select the most applicable window configuration of your house (see example image below):**")
col1, col2, col3 = st.columns(3)
with col1:
    wwr_10_path = "utils/SF_WWR_10.png"
    st.image(wwr_10_path, caption="Window-to-Wall Ratios = 9%")
with col2:
    wwr_15_path = "utils/SF_WWR_15.png"
    st.image(wwr_15_path, caption="Window-to-Wall Ratios = 15%")
with col3:
    wwr_15_path = "utils/SF_WWR_30.png"
    st.image(wwr_15_path, caption="Window-to-Wall Ratios = 30%")

wwr = st.selectbox(
    "Window-to-Wall Ratio",
    options=[9, 15, 30],
    format_func=lambda x: f"{x}%"
)

# Baseline window for home users
st.write(f"**Select the most applicable window type your home currently use (Single-pane window by default)**")
baseline = st.selectbox(
    "Baseline Window Type",
    options=default_window_database["window_type"].unique(),
    index=6
)
st.link_button("Learn about window products💡", "https://efficientwindows.org/types_parts/")

conditioned_area = st.session_state["conditioned_area"]
house_type = st.session_state["house_type"]
stories = st.session_state["stories"]
foundation = st.session_state["foundation"]

# Calculate the predicted window area using user inputs
window_area = calculate_predicted_window_area(conditioned_area, house_type, stories, wwr,
                                              foundation='Heated Basement')  # Defaulting foundation to 'Heated Basement' for demonstration

# Initialize session state for custom windows if not already present
if "custom_windows" not in st.session_state:
    st.session_state.custom_windows = pd.DataFrame(columns=["window_type", "window_name", "U-factor", "SHGC"])

# Add custom window
add = st.toggle("Add Custom Windows")
if add:
    # Form for adding custom windows
    with st.form("add_window_form"):
        # Dropdown for predefined window types
        window_type = st.selectbox("Window Type", options=default_window_database["window_type"].unique())
        # Input for custom window name
        window_name = st.text_input("Window Name",
                                    placeholder="Enter a name for the custom window (e.g., My Custom Window)")
        U_factor = st.number_input("U-factor", min_value=0.0, step=0.01)
        SHGC = st.number_input("SHGC (Solar Heat Gain Coefficient)", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Add Window")

    # Append custom window to session state if form is submitted
    if submitted:
        if window_type and window_name and U_factor and SHGC:
            new_window = pd.DataFrame(
                [[window_type, window_name, U_factor, SHGC]],
                columns=["window_type", "window_name", "U-factor", "SHGC"]
            )
            st.session_state.custom_windows = pd.concat([st.session_state.custom_windows, new_window], ignore_index=True)
            st.success(f"Window '{window_type}' added successfully!")
        else:
            st.error("Please fill out all fields before submitting.")

# Combine default and custom windows
combined_window_database = pd.concat([default_window_database,
                                      st.session_state.custom_windows], ignore_index=True)

# Create a sorting key based on the pane type
def get_sort_key(window_type):
    if window_type.startswith("Single-pane"):
        return 1  # Single-pane has the highest priority
    elif window_type.startswith("Double-pane"):
        return 2  # Double-pane next
    elif window_type.startswith("Triple-pane"):
        return 3  # Triple-pane last
    else:
        return 4  # Any other type (if exists)

# Add a sort key column to the DataFrame
combined_window_database["sort_key"] = combined_window_database["window_type"].apply(get_sort_key)

# Sort the DataFrame by sort_key and then alphabetically within each group
sorted_window_database = combined_window_database.sort_values(by=["sort_key", "window_type"]).drop(columns="sort_key")

# # Display the combined database
st.write("### Current Window Database (Default + Custom):")
st.write(sorted_window_database)

st.session_state["combined_window_database"] = combined_window_database
st.session_state["window_area"] = window_area
st.session_state["wwr"] = wwr
st.session_state["baseline"] = baseline

# Navigation buttons
col1, col2 = st.columns([1, 1.5])
with col1:
    Back_to_House()
with col2:
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(
            '<p style="font-size:12px;">Please notice that three recommendations will made based on your choice of window!</p>',
            unsafe_allow_html=True
        )
    with col2:
        Go_to_Result()
