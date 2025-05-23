import streamlit as st
from preprocessing import *
from utils import Back_to_Location, Go_to_Window
import re

st.title("Enter House Information")

vintage = st.selectbox(
        f"**Select the year your house was built (Vintage)**",
        options=["<1940", "1940s", "1950s", "1960s", "1970s",
                 "1980s", "1990s", "2000s", ">2010"]
    )

if vintage == ">2010":
    vintage = "2010s"

house_type = st.selectbox(
    f"**Select your house type**",
    options=["Single-Family Detached", "Single-Family Attached", "Apartment Unit",
            "Mobile Home"]
)

orientation = st.selectbox(
    f"**Orientation of the front of the dwelling unit as it faces the street**",
    options=["East", "West", "Northeast", "Southwest", "North", "South", "Northwest",
            "Southeast"]
)

floor_area = st.number_input(f"**Enter the floor area (sq ft) above grade (Exclude basement)**", min_value=100, max_value=10000)
stories = st.number_input(f"**Number of Stories**", min_value=1, max_value=3, step=1)

is_cooling = st.checkbox("Air conditioner")
if is_cooling:
    cooling_setpoint = st.number_input(f"**Cooling setpoint (°F)**", min_value=60, max_value=80, value=75)
else:
    cooling_setpoint = 0
is_heating = st.checkbox("Heater")
if is_heating:
    # heating_fuel = st.selectbox(
    #     f"**Select the type of heating fuel this house utilize**",
    #     options=["Electricity", "Natural Gas", "Propane", "Fuel Oil", "Wood"]
    # )
    heating_setpoint = st.number_input(f"**Heating setpoint (°F)**", min_value=50, max_value=80, value=68)
else:
    heating_setpoint = 0


st.write(f"**Basement Information**")
is_heated_basement = st.checkbox("Do you have a heated basement?")
foundation = "Heated Basement" if is_heated_basement else "Others"
if is_heated_basement:
    basement_area = st.number_input(f"**Enter the basement area (sq ft)**", min_value=100, max_value=10000)
else:
    basement_area = 0

conditioned_area = floor_area + basement_area

# Utility input section
st.write(f"**Utility Costs**")
summer_bill = st.number_input(
    "Summer season Monthly utility bill ($)", min_value=0.0, step=0.01, format="%.2f"
)
winter_bill = st.number_input(
    "Winter season Monthly utility bill ($)", min_value=0.0, step=0.01, format="%.2f"
)

# Calculate the surface volume ratio using user inputs
sv = calculate_surface_volume_ratio(conditioned_area, house_type, stories,
                                    foundation='Heated Basement')  # Defaulting foundation to 'Heated Basement' for demonstration

# Convert the orientation from str to number
orient = convert_orientation(orientation)

# Determine house infiltration level
zip_code = st.session_state["zip_code"]
infiltration = get_infiltration(zip_code, floor_area, vintage)
match = re.match(r'Option=(\d+)', infiltration)
if match:
    infiltration = int(match.group(1))

# Calculate annual total utility bills
heating_period = st.session_state["heating_period"]
cooling_period = st.session_state["cooling_period"]
total_bills = summer_bill * cooling_period + winter_bill * heating_period

# Save house details in session state
st.session_state["vintage"] = vintage
st.session_state["house_type"] = house_type
st.session_state["stories"] = stories
st.session_state["orientation"] = orient
# **HVAC**
st.session_state["is_cooling"] = is_cooling
st.session_state["cooling_setpoint"] = cooling_setpoint
st.session_state["is_heating"] = is_heating
# st.session_state["heating_fuel"] = heating_fuel
st.session_state["heating_setpoint"] = heating_setpoint
# **Foundation**
st.session_state["conditioned_area"] = conditioned_area
st.session_state["foundation"] = foundation
# **Utility**
st.session_state["summer_bill"] = summer_bill
st.session_state["winter_bill"] = winter_bill
# **Derived**
st.session_state["infiltration"] = infiltration
st.session_state["sv"] = sv
st.session_state['total_bills'] = total_bills

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    Back_to_Location()
with col2:
    Go_to_Window()