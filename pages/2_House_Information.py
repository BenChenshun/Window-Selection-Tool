import streamlit as st
from preprocessing import *
from utils import Back_to_Location, Go_to_Window

st.title("Enter House Information")

vintage = st.selectbox(
        "Select the year your house was built (Vintage)",
        options=["<1940", "1940s", "1950s", "1960s", "1970s",
                 "1980s", "1990s", "2000s", "2010s"]
    )
house_type = st.selectbox(
    "Select your house type",
    options=["Single-Family Detached", "Single-Family Attached", "Apartment Unit",
            "Mobile Home"]
)

orientation = st.selectbox(
    "Orientation of the front of the dwelling unit as it faces the street",
    options=["East", "West", "Northeast", "Southwest", "North", "South", "Northwest",
            "Southeast"]
)

conditioned_area = st.number_input("Enter the floor area (sq ft)", min_value=100, max_value=10000)
stories = st.number_input("Number of Stories", min_value=1, max_value=3, step=1)
heating_setpoint = st.number_input("Heating setpoint (°F)", min_value=50, max_value=80, value=68)
cooling_setpoint = st.number_input("Cooling setpoint (°F)", min_value=60, max_value=80, value=75)

st.write("Basement Information")
is_heated_basement = st.checkbox("Do you have a heated basement?")
foundation = "Heated Basement" if is_heated_basement else "Others"

# Calculate the surface volume ratio using user inputs
sv = calculate_surface_volume_ratio(conditioned_area, house_type, stories,
                                    foundation='Heated Basement')  # Defaulting foundation to 'Heated Basement' for demonstration

# Convert the orientation from str to number
orient = convert_orientation(orientation)

# Save house details in session state
st.session_state["vintage"] = vintage
st.session_state["house_type"] = house_type
st.session_state["stories"] = stories
st.session_state["orientation"] = orient
st.session_state["heating_setpoint"] = heating_setpoint
st.session_state["cooling_setpoint"] = cooling_setpoint
st.session_state["conditioned_area"] = conditioned_area
st.session_state["foundation"] = foundation
st.session_state["sv"] = sv

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    Back_to_Location()
with col2:
    Go_to_Window()