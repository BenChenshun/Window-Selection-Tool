import streamlit as st
from preprocessing import *
from utils import Home, Go_to_House

st.title("Input Your Zip Code")

# Input for zip code
zip_code = st.text_input(f"**Enter your zip code**")
if zip_code:
    # Get weather info based on zip code
    st.session_state["zip_code"] = zip_code
    st.write(f"Zip code saved: {zip_code}")
    weather_df = get_weather_info(zip_code)
    st.session_state["summer_avg_temp"] = weather_df["summer_avg_temp"].iloc[0]
    st.session_state["winter_avg_temp"] = weather_df["winter_avg_temp"].iloc[0]
    st.session_state["HDH"] = weather_df["HDH"].iloc[0]
    st.session_state["CDH"] = weather_df["CDH"].iloc[0]
    HDD = weather_df["HDD"].iloc[0]
    CDD = weather_df["CDD"].iloc[0]
    st.session_state["heating_period"], st.session_state["cooling_period"] = calculate_period(HDD, CDD)
    st.session_state["GHI"] = weather_df["GHI"].iloc[0]
    st.session_state["climatezone"] = weather_df["Climate Zone"].iloc[0]

    # Get EnergyStar climatezone
    energystar_zone = get_energystar_zone(zip_code)
    st.session_state["energystar_zone"] = energystar_zone

    # Get heating and cooling period
    heating_period = calculate_period(HDD, CDD)[0]
    st.session_state["heating_period"] = heating_period
    cooling_period = calculate_period(HDD, CDD)[1]
    st.session_state["cooling_period"] = cooling_period

else:
    st.write("Please enter a zip code.")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    Home()
with col2:
    Go_to_House()