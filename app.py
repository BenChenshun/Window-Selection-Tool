import streamlit as st
import pandas as pd
import pickle
from preprocessing import *
import lightgbm as lgb
import numpy as np

#%%
# Load the trained model from a .pkl file
## List of model file names and corresponding target variables
model_files = {
    "cooling_window": "models/cooling_window_lightgbm.pkl",
    "heating_window": "models/heating_window_lightgbm.pkl",
    "cooling_load": "models/cooling_load_lightgbm.pkl",
    "heating_load": "models/heating_load_lightgbm.pkl"
}

# Load the models into a dictionary
models = {}
for target, model_file in model_files.items():
    try:
        with open(model_file, "rb") as file:
            models[target] = pickle.load(file)
    except FileNotFoundError:
        st.error(f"Model file for {target} not found. Please upload or specify the correct path.")
        st.stop()

#%%
def add_logo_and_title():
    """
    Add the logo and header title to each page.
    """
    # logo_path = "assets/logo.png"  # Adjust the path to your logo image
    # st.image(logo_path, width=150)  # Adjust width as needed
    st.title("Window Selection Tool")
    st.markdown("---")  # Optional: Adds a horizontal divider

# Initialize session state to keep track of the page
if "page" not in st.session_state:
    st.session_state.page = 1

# Navigation handlers
def go_to_next_page():
    st.session_state.page += 1

def go_to_previous_page():
    st.session_state.page -= 1

# Page 1: Zip Code Input
if st.session_state.page == 1:
    st.title("Welcome to Window Selection Tool")
    st.write(
        "This app provides predictions for a default set of window products. You can also add your own custom windows.")

    add_logo_and_title()
    st.header("Location")
    zip_code = st.text_input("Enter your zip code")

    if zip_code:
        st.session_state["zip_code"] = zip_code
        st.write(f"Zip code saved: {zip_code}")
    else:
        st.write("Please enter a zip code.")

    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Next"):
            go_to_next_page()

# Page 2: House Information
elif st.session_state.page == 2:
    add_logo_and_title()  # Add the logo and header
    st.header("House Information")

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
    orientation = convert_orientation(orientation)

    # Save house details in session state
    st.session_state["vintage"] = vintage
    st.session_state["house_type"] = house_type
    st.session_state["stories"] = stories
    st.session_state["orientation"] = orientation
    st.session_state["heating_setpoint"] = heating_setpoint
    st.session_state["cooling_setpoint"] = cooling_setpoint
    st.session_state["conditioned_area"] = conditioned_area
    st.session_state["foundation"] = foundation
    st.session_state["sv"] = sv

    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Previous"):
            go_to_previous_page()
    with col2:
        if st.button("Next"):
            go_to_next_page()

# Page 3: Window Information
elif st.session_state.page == 3:
    add_logo_and_title()  # Add the logo and header
    st.header("Window Information")
    # st.write("Select your window-to-wall ratio (see example image below):")
    # window_wall_ratio_image_path = "data/window_wall_ratio_example.png"
    # st.image(window_wall_ratio_image_path, caption="Example Window-to-Wall Ratios")
    wwr = st.selectbox(
        "Window-to-Wall Ratio",
        options=[9, 15, 30],
        format_func=lambda x: f"{x}%"
    )
    window_type_baseline = st.selectbox(
        "Window Type Baseline",
        options=["Single-pane window", "Double-pane window", "Double-pane low-E window", "Triple-pane window"]
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
        st.session_state.custom_windows = pd.DataFrame(columns=["Window Name", "U-Factor", "SHGC"])

    # Form for adding custom windows
    st.header("Add Custom Windows")
    with st.form("add_window_form"):
        window_name = st.text_input("Window Name", placeholder="Enter window name (e.g., Custom Window 1)")
        U_factor = st.number_input("U-Factor", min_value=0.0, step=0.01)
        SHGC = st.number_input("SHGC (Solar Heat Gain Coefficient)", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Add Window")

    # Append custom window to session state if form is submitted
    if submitted:
        if window_name and U_factor and SHGC:
            new_window = pd.DataFrame(
                [[window_name, U_factor, SHGC]],
                columns=["Window Name", "U-Factor", "SHGC"]
            )
            st.session_state.custom_windows = pd.concat([st.session_state.custom_windows, new_window], ignore_index=True)
            st.success(f"Window '{window_name}' added successfully!")
        else:
            st.error("Please fill out all fields before submitting.")

    # Combine default and custom windows
    combined_window_database = pd.concat([default_window_database, st.session_state.custom_windows], ignore_index=True)

    # Display the combined database
    st.write("### Current Window Database (Default + Custom):")
    st.write(combined_window_database)

    st.session_state["combined_window_database"] = combined_window_database
    st.session_state["wwr"] = wwr
    st.session_state["window_type_baseline"] = window_type_baseline

    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Previous"):
            go_to_previous_page()
    with col2:
        if st.button("Finish and run"):
            go_to_next_page()

# Page 4: Results Page
elif st.session_state.page == 4:
    add_logo_and_title()  # Add the logo and header
    st.header("Results")

    st.write("Summary of your house properties:")
    # Display summary
    if "zip_code" in st.session_state:
        st.write(f"Zip Code: {st.session_state['zip_code']}")
    if "vintage" in st.session_state:
        st.write(f"Vintage: {st.session_state['vintage']}")
    if "house_type" in st.session_state:
        st.write(f"House Type: {st.session_state['house_type']}")
    if "heating_setpoint" in st.session_state:
        st.write(f"Heating Setpoint: {st.session_state['heating_setpoint']} °F")
    if "cooling_setpoint" in st.session_state:
        st.write(f"Cooling Setpoint: {st.session_state['cooling_setpoint']} °F")
    if "floor_area" in st.session_state:
        st.write(f"Floor Area: {st.session_state['floor_area']} sq ft")
    if "window_wall_ratio" in st.session_state:
        st.write(f"Window-to-Wall Ratio: {st.session_state['window_wall_ratio']}%")
    if "window_area" in st.session_state:
        st.write(f"Window Area: {st.session_state['window_area']}")
    if "window_type_baseline" in st.session_state:
        st.write(f"Window Type Baseline: {st.session_state['window_type_baseline']}")


    # Check if combined_window_database and necessary predictors are available
    if "combined_window_database" in st.session_state and all(
        key in st.session_state for key in ['climatezone', 'zip_code', 'vintage', 'orientation',
                                             'wwr', 'cooling_setpoint', 'heating_setpoint',
                                             'HDH', 'CDH', 'winter_avg_temp', 'summer_avg_temp',
                                             'GHI', 'conditioned_area', 'sv']
    ):
        combined_window_database = st.session_state["combined_window_database"]

        # Prepare predictors for each window
        predictors = []
        for _, row in combined_window_database.iterrows():
            predictors.append([
                st.session_state["climatezone"],
                st.session_state["zip_code"],
                st.session_state["vintage"],
                st.session_state["orientation"],
                row["Window Name"],  # Window type (matches "window_type")
                st.session_state["wwr"],
                st.session_state["window_area"],  # Assuming this is calculated earlier
                row["U-factor"],
                row["SHGC"],
                st.session_state["cooling_setpoint"],
                st.session_state["heating_setpoint"],
                st.session_state["HDH"],
                st.session_state["CDH"],
                st.session_state["winter_avg_temp"],
                st.session_state["summer_avg_temp"],
                st.session_state["GHI"],
                st.session_state["conditioned_area"],
                st.session_state["sv"]
            ])

        # Convert predictors to a NumPy array for prediction
        X = np.array(predictors)

        # Make predictions for each target using the respective model
        results = combined_window_database[["Window Name"]].copy()
        for target, model in models.items():
            results[target] = model.predict(X)

        # Display results with top 3 lowest predictions for each target highlighted
        st.write("### Final Results (Descending Order of Primary Target):")
        for target in models.keys():
            st.write(f"#### Predictions for {target}:")
            for i, row in results.iterrows():
                if i < 3:  # Highlight the top 3 lowest predictions
                    st.markdown(
                        f"**{row['Window Name']}: {row[target]:.2f}** (Highlighted as Top 3 Lowest)"
                    )
                else:
                    st.markdown(f"{row['Window Name']}: {row[target]:.2f}")

        # Optionally, display the entire results table
        st.write(results)

    else:
        st.error("Missing necessary data or predictors. Please complete previous sections.")

    # Navigation buttons
    if st.button("Previous"):
        go_to_previous_page()



 




