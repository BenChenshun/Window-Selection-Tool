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
    window_names = [name[:25] + "..." if len(name) > 25 else name for name in window_names]
    cooling_window = df["cooling_window"]
    cooling_percent = df["cooling_window_percent"]
    heating_window = df["heating_window"]
    heating_percent = df["heating_window_percent"]
    total_cooling = df["cooling_load"]
    total_heating = df["heating_load"]

    # Define positions for grouped bars
    bar_width = 0.5
    y_positions = [i * 2 for i in range(len(window_names))]

    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(10, len(window_names) * 1.5))  # Adjust height dynamically

    # Plot heating bars
    ax.barh(
        [y - bar_width / 2 for y in y_positions], total_heating, bar_width,
        label="Total Heating Energy", color="lightcoral", alpha=0.7
    )
    ax.barh(
        [y - bar_width / 2 for y in y_positions], heating_window, bar_width,
        label="Window Heating Contribution", color="red", alpha=0.9
    )

    # Plot cooling bars
    ax.barh(
        [y + bar_width / 2 for y in y_positions], total_cooling, bar_width,
        label="Total Cooling Energy", color="lightblue", alpha=0.7
    )
    ax.barh(
        [y + bar_width / 2 for y in y_positions], cooling_window, bar_width,
        label="Window Cooling Contribution", color="dodgerblue", alpha=0.9
    )

    # Add labels and title
    ax.set_yticks(y_positions)
    ax.set_yticklabels(window_names)
    ax.set_xlabel("Energy Contribution (Btu)")
    # ax.set_title("Heating/Cooling Energy Contributions by Windows")
    # Adjust legend placement: Move outside the plot area
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1),  # Place legend above the plot
        ncol=2,  # Spread legend horizontally
        fontsize=8
    )

    # Add percentage labels to bars
    for i, (y, total, percent) in enumerate(zip(y_positions, total_heating, heating_percent)):
        ax.text(total, y - bar_width / 2, f"{percent:.2f}%", va="center", ha="left", fontsize=10)
    for i, (y, total, percent) in enumerate(zip(y_positions, total_cooling, cooling_percent)):
        ax.text(total, y + bar_width / 2, f"{percent:.2f}%", va="center", ha="left", fontsize=10)

    # Adjust layout and display the plot in Streamlit
    plt.tight_layout()
    st.pyplot(fig)