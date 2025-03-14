# File: utils.py

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stoggle import stoggle
import matplotlib.pyplot as plt
import numpy as np

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
    fig, ax = plt.subplots(figsize=(18, len(window_names) * 1.5))  # Adjust height dynamically

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
        fontsize=12
    )

    # Add percentage labels to bars
    for i, (y, total, percent) in enumerate(zip(y_positions, total_heating, heating_percent)):
        ax.text(total, y - bar_width / 2, f"{percent:.2f}%", va="center", ha="left", fontsize=15)
    for i, (y, total, percent) in enumerate(zip(y_positions, total_cooling, cooling_percent)):
        ax.text(total, y + bar_width / 2, f"{percent:.2f}%", va="center", ha="left", fontsize=15)

    # Adjust layout and display the plot in Streamlit
    # plt.tight_layout()
    st.pyplot(fig)

def plot_energy_contributions_pie(df):
    """
    Creates a single figure with pie charts for cooling and/or heating contributions,
    using all rows in the DataFrame.

    For each pie chart:
      - Each window’s contribution (absolute value) is a slice with its window_name as the label.
      - An "Other" slice is added representing the remainder to reach the total load.
      - The percentage shown on each slice is computed relative to the total load.

    Cooling and heating charts use different color schemes.

    If cooling_load or heating_load is less than 5, the corresponding pie chart is not plotted.
    """
    # Obtain total loads (assumed constant across rows)
    window_name = df["window_name"]
    cooling_total = df["cooling_load"]
    heating_total = df["heating_load"]

    valid_cooling = cooling_total >= 5
    valid_heating = heating_total >= 5

    # If neither qualifies, exit.
    if not (valid_cooling or valid_heating):
        st.write("Both cooling and heating loads are below threshold (5). No plots to display.")
        return

    # Determine number of subplots to create.
    plot_count = (1 if valid_cooling else 0) + (1 if valid_heating else 0)

    # Create the figure and axes.
    if plot_count == 1:
        fig, ax = plt.subplots(figsize=(6, 6))
        axes = [ax]
    else:
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    ax_index = 0

    # --- Cooling Pie Chart ---
    if valid_cooling:
        # Compute slices: use absolute contributions for wedge sizes.
        cooling_contrib = abs(df["cooling_window"])  # non-negative values
        # sum_cooling = cooling_contrib.sum()
        other_cooling = max(0, abs(cooling_total))
        slices_cooling = np.append(cooling_contrib, other_cooling)
        # Use each window_name as label, plus "Other"
        labels_cooling = ["Window", "Other"]

        # Define a blue color scheme for cooling.
        cmap_cooling = plt.get_cmap("Blues")
        colors_cooling = cmap_cooling(np.linspace(0.4, 0.8, len(slices_cooling)))

        ax = axes[ax_index]
        ax.pie(
            slices_cooling,
            labels=labels_cooling,
            colors=colors_cooling,
            startangle=140,
            autopct="%1.1f%%",
            textprops={"fontsize": 14}
        )
        ax.set_title(f"{window_name} - Cooling Contribution")
        ax_index += 1

    # --- Heating Pie Chart ---
    if valid_heating:
        heating_contrib = abs(df["heating_window"])
        # sum_heating = heating_contrib.sum()
        other_heating = max(0, abs(heating_total))
        slices_heating = np.append(heating_contrib, other_heating)
        labels_heating = ["Window", "Other"]

        # Define an orange color scheme for heating.
        cmap_heating = plt.get_cmap("Oranges")
        colors_heating = cmap_heating(np.linspace(0.4, 0.8, len(slices_heating)))

        ax = axes[ax_index]
        ax.pie(
            slices_heating,
            labels=labels_heating,
            colors=colors_heating,
            startangle=140,
            autopct="%1.1f%%",
            textprops={"fontsize": 14}
        )
        ax.set_title(f"{window_name} - Heating Contribution")
        ax_index += 1

    plt.tight_layout()
    st.pyplot(fig)