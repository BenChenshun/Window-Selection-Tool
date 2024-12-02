# File: utils.py

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stoggle import stoggle
import matplotlib.pyplot as plt

# Navigation button functions
def Home():
    home = st.button("Return")
    if home:
        switch_page("Home")

def Go_to_Location():
    loc = st.button("Next")
    if loc:
        switch_page("house location")

def Back_to_Location():
    loc = st.button("Return")
    if loc:
        switch_page("house location")

def Go_to_House():
    house = st.button("Next")
    if house:
        switch_page("House Information")

def Back_to_House():
    house = st.button("Return")
    if house:
        switch_page("House Information")

def Go_to_Window():
    window = st.button("Next")
    if window:
        switch_page("Window Information")

def Back_to_Window():
    window = st.button("Return")
    if window:
        switch_page("Window Information")

def Go_to_Result():
    window = st.button("Finish and Run!")
    if window:
        switch_page("Results")

def plot_energy_contributions(df):
    # Prepare data for the plot
    window_names = df["window_name"]
    # Truncate window names for display
    window_names = [name[:20] + "..." if len(name) > 20 else name for name in window_names]
    cooling_window = df["cooling_window"]
    cooling_percent = df["cooling_window_percent"]
    heating_window = df["heating_window"]
    heating_percent = df["heating_window_percent"]
    total_cooling = df["cooling_load"]
    total_heating = df["heating_load"]

    # Create subplots for cooling and heating
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Bar plot for heating contribution
    axes[0].bar(window_names, total_heating, label="Total Heating Energy", color="lightcoral", alpha=0.8)
    axes[0].bar(window_names, heating_window, label="Window Heating Contribution", color="red", alpha=0.8)
    axes[0].set_title("Heating Contribution by Windows")
    axes[0].set_ylabel("Energy Contribution (kWh)")
    axes[0].set_xticks(range(len(window_names)))
    axes[0].set_xticklabels(window_names, rotation=45, ha="right")
    axes[0].legend(loc="upper right")

    # Add percentage labels to bars (upper-right corner)
    for i, (total, percent) in enumerate(zip(total_heating, heating_percent)):
        axes[0].text(i, total, f"{percent:.2f}%", ha="center", va="bottom", fontsize=10)

    # Bar plot for cooling contribution
    axes[1].bar(window_names, total_cooling, label="Total Cooling Energy", color="lightblue", alpha=0.8)
    axes[1].bar(window_names, cooling_window, label="Window Cooling Contribution", color="dodgerblue", alpha=0.8)
    axes[1].set_title("Cooling Contribution by Windows")
    axes[1].set_ylabel("Energy Contribution (kWh)")
    axes[1].set_xticks(range(len(window_names)))
    axes[1].set_xticklabels(window_names, rotation=45, ha="right")
    axes[1].legend(loc="upper right")

    # Add percentage labels to bars (upper-right corner)
    for i, (total, percent) in enumerate(zip(total_cooling, cooling_percent)):
        axes[1].text(i, total, f"{percent:.2f}%", ha="center", va="bottom", fontsize=10)

    # Adjust layout and display the plot in Streamlit
    plt.tight_layout()
    st.pyplot(fig)