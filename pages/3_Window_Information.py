import streamlit as st
from preprocessing import *
import pandas as pd
from utils import Back_to_House, Go_to_Result

st.title("Specify Window Details")

# st.write("Select your window-to-wall ratio (see example image below):")
# window_wall_ratio_image_path = "data/window_wall_ratio_example.png"
# st.image(window_wall_ratio_image_path, caption="Example Window-to-Wall Ratios")
wwr = st.selectbox(
    "Window-to-Wall Ratio",
    options=[9, 15, 30],
    format_func=lambda x: f"{x}%"
)

conditioned_area = st.session_state["conditioned_area"]
house_type = st.session_state["house_type"]
stories = st.session_state["stories"]
foundation = st.session_state["foundation"]

# Calculate the predicted window area using user inputs
window_area = calculate_predicted_window_area(conditioned_area, house_type, stories, wwr,
                                              foundation='Heated Basement')  # Defaulting foundation to 'Heated Basement' for demonstration

# Path to the default window database file
DEFAULT_WINDOW_DATABASE_PATH = 'data/window_data.csv'

# Display default window database
# st.write("### Default Window Database:")
default_window_database = pd.read_csv(DEFAULT_WINDOW_DATABASE_PATH)
# st.write(default_window_database)

# Initialize session state for custom windows if not already present
if "custom_windows" not in st.session_state:
    st.session_state.custom_windows = pd.DataFrame(columns=["window_type", "U-factor", "SHGC"])

# Form for adding custom windows
st.header("Add Custom Windows")
with st.form("add_window_form"):
    window_type = st.text_input("Window Type", placeholder="Enter window type (e.g., Custom Window 1)")
    U_factor = st.number_input("U-factor", min_value=0.0, step=0.01)
    SHGC = st.number_input("SHGC (Solar Heat Gain Coefficient)", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add Window")

# Append custom window to session state if form is submitted
if submitted:
    if window_type and U_factor and SHGC:
        new_window = pd.DataFrame(
            [[window_type, U_factor, SHGC]],
            columns=["window_type", "U-factor", "SHGC"]
        )
        st.session_state.custom_windows = pd.concat([st.session_state.custom_windows, new_window], ignore_index=True)
        st.success(f"Window '{window_type}' added successfully!")
    else:
        st.error("Please fill out all fields before submitting.")

# Combine default and custom windows
combined_window_database = pd.concat([default_window_database, st.session_state.custom_windows], ignore_index=True)

# Display the combined database
st.write("### Current Window Database (Default + Custom):")
st.write(combined_window_database)

st.session_state["combined_window_database"] = combined_window_database
st.session_state["window_area"] = window_area
st.session_state["wwr"] = wwr

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    Back_to_House()
with col2:
    Go_to_Result()