import streamlit as st
from preprocessing import *
from utils import Home, Go_to_House

st.title("Input Your Zip Code")

# Input for zip code
zip_code = st.text_input(f"**Enter your zip code**")
if zip_code:
    st.session_state["zip_code"] = zip_code
    st.write(f"Zip code saved: {zip_code}")
    weather_df = get_weather_info(zip_code)
    st.session_state["summer_avg_temp"] = weather_df["summer_avg_temp"].iloc[0]
    st.session_state["winter_avg_temp"] = weather_df["winter_avg_temp"].iloc[0]
    st.session_state["HDH"] = weather_df["HDH"].iloc[0]
    st.session_state["CDH"] = weather_df["CDH"].iloc[0]
    st.session_state["GHI"] = weather_df["GHI"].iloc[0]
    st.session_state["climatezone"] = weather_df["Climate Zone"].iloc[0]
else:
    st.write("Please enter a zip code.")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    Home()
with col2:
    Go_to_House()