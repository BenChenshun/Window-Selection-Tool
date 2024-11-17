import streamlit as st
import pickle
import numpy as np
import pandas as pd
from utils import Home
import category_encoders as ce

st.title("View the Results")

# Load the trained model from a .pkl file
## List of model file names and corresponding target variables
model_files = {
    "cooling_window": "models/cooling_window.pkl",
    "heating_window": "models/heating_window.pkl",
    "cooling_load": "models/cooling_load.pkl",
    "heating_load": "models/heating_load.pkl"
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

# Load encoders
@st.cache_resource
def load_target_encoders():
    with open("models/target_encoders.pkl", "rb") as f:
        return pickle.load(f)

def load_onehot_encoder():
    with open("models/onehot_encoder.pkl", "rb") as f:
        return pickle.load(f)

onehot_encoded_conditions = ['vintage']
target_encoded_conditions = ['climatezone', 'zip_code', 'window_type']

target_encoders = load_target_encoders()
onehot_encoder = load_onehot_encoder()

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


# Check if combined_window_database and necessary predictors are available
if "combined_window_database" in st.session_state and all(
    key in st.session_state for key in ['climatezone', 'zip_code', 'vintage', 'orientation',
                                         'wwr', 'cooling_setpoint', 'heating_setpoint',
                                         'HDH', 'CDH', 'winter_avg_temp', 'summer_avg_temp',
                                         'GHI', 'conditioned_area', 'sv']
):
    combined_window_database = st.session_state["combined_window_database"]
    # st.write(combined_window_database)
    # Initialize results DataFrame
    results = combined_window_database[["window_type"]].copy()

    if st.button("Execute"):

        # Prepare predictors for each window
        for _, row in combined_window_database.iterrows():
            predictors = []
            predictors.append({
                "climatezone": st.session_state["climatezone"],
                "zip_code": st.session_state["zip_code"],
                "vintage": st.session_state["vintage"],
                "orientation": st.session_state["orientation"],
                "window_type": row["window_type"],  # Window type (matches "window_type")
                "wwr": st.session_state["wwr"],
                "window_area": st.session_state["window_area"],  # Assuming this is calculated earlier
                "U-factor": row["U-factor"],
                "SHGC": row["SHGC"],
                "cooling_setpoint": st.session_state["cooling_setpoint"],
                "heating_setpoint": st.session_state["heating_setpoint"],
                "HDH": st.session_state["HDH"],
                "CDH": st.session_state["CDH"],
                "winter_avg_temp": st.session_state["winter_avg_temp"],
                "summer_avg_temp": st.session_state["summer_avg_temp"],
                "GHI": st.session_state["GHI"],
                "conditioned_area": st.session_state["conditioned_area"],
                "sv": st.session_state["sv"]
            })

            # Convert predictors to a NumPy array for prediction
            predictors_df = pd.DataFrame(predictors)

            # Apply encoders
            onehot_encoded = onehot_encoder.transform(predictors_df[onehot_encoded_conditions])
            # Convert the NumPy array to a DataFrame with appropriate column names
            onehot_encoded_df = pd.DataFrame(
                onehot_encoded,
                columns=onehot_encoder.get_feature_names_out(onehot_encoded_conditions),
                index=predictors_df.index  # Use the same index as the original DataFrame
            )
            # Apply onehot encoding
            predictors_ready = predictors_df.drop(columns=onehot_encoded_conditions, axis=1).join(onehot_encoded_df)

            # Make predictions for each target using the respective model
            for target, model in models.items():
                # Apply target-specific encoding
                encoder = target_encoders[target]
                encoded_predictors = encoder.transform(predictors_ready[target_encoded_conditions])
                X = predictors_ready.drop(columns=target_encoded_conditions, axis=1).join(encoded_predictors)
                # Ensure compatibility with the model
                X = X[model["features"]]

                # Make predictions
                predictions = model["model"].predict(X)[0]

                # Add the prediction to the results DataFrame
                if target not in results.columns:
                    results[target] = None  # Initialize the column if it doesn't exist

                results.loc[results["window_type"] == row["window_type"], target] = predictions

    # Apply Logic to Update Results
    results.loc[results["cooling_load"] < 1, ["cooling_load"]] = 0
    results.loc[results["heating_load"] < 1, ["heating_load"]] = 0

    # Add percentage columns to the results DataFrame
    # Calculate percentages only when cooling_load and heating_load are > 0.5
    results["cooling_window_percent"] = results.apply(
        lambda row: (row["cooling_window"] / row["cooling_load"]) * 100 if row["cooling_load"] > 1 else 0, axis=1
    )
    results["heating_window_percent"] = results.apply(
        lambda row: (row["heating_window"] / row["heating_load"]) * 100 if row["heating_load"] > 1 else 0, axis=1
    )
    # Add an average percentage for sorting and recommendations
    results["average_percent"] = results.apply(
        lambda row: row["heating_window_percent"] if row["cooling_load"] == 0 else
        row["cooling_window_percent"] if row["heating_load"] == 0 else
        (row["cooling_window_percent"] + row["heating_window_percent"]) / 2,
        axis=1
    )

    # Add a button to toggle between showing all results or top 3
    show_all = st.checkbox("Show All Results", value=False)

    if show_all:
        # Show the full sorted results
        for target in models.keys():
            st.write(f"#### Predictions for {target}:")
            # Sort results by the target column in ascending order and reset the index
            sorted_results = results.sort_values(by=target, ascending=True).reset_index(drop=True)

            for i, row in sorted_results.iterrows():
                if i < 3:  # Highlight the top 3 lowest predictions
                    st.markdown(
                        f"**{row['window_type']}: {row[target]:.2f}** (Highlighted as Top 3 Lowest)"
                    )
                else:
                    st.markdown(f"{row['window_type']}: {row[target]:.2f}")
            st.write(sorted_results)
    else:
        # Sort results based on the average percentage
        sorted_results = results.sort_values(by="average_percent", ascending=True).reset_index(drop=True)
        # Show only the top 3 recommendations
        st.write("### Top 3 Recommended Windows:")

        # Get the top 3 results
        top_3_results = sorted_results.head(3)

        # Display each recommended window as text with emojis
        for i, row in top_3_results.iterrows():
            # Display custom messages for no cooling or heating need
            if (top_3_results["cooling_load"] == 0).all():
                st.markdown(
                    f"**{i + 1}. {row['window_type']}** 🪟\n"
                    f"- Your house has no cooling need! ❄️\n"
                    f"- Heating Efficiency: {row['heating_window_percent']:.2f}% 🔥\n"
                    f"- Average Efficiency: {row['average_percent']:.2f}% 🌟"
                )
            elif (top_3_results["heating_load"] == 0).all():
                st.markdown(
                    f"**{i + 1}. {row['window_type']}** 🪟\n"
                    f"- Cooling Efficiency: {row['cooling_window_percent']:.2f}% ❄️\n"
                    f"- Your house has no heating need! 🔥\n"
                    f"- Average Efficiency: {row['average_percent']:.2f}% 🌟"
                )
            else:
                st.markdown(
                    f"**{i + 1}. {row['window_type']}** 🪟\n"
                    f"- Cooling Efficiency: {row['cooling_window_percent']:.2f}% ❄️\n"
                    f"- Heating Efficiency: {row['heating_window_percent']:.2f}% 🔥\n"
                    f"- Average Efficiency: {row['average_percent']:.2f}% 🌟"
                )

else:
    st.error("Missing necessary data or predictors. Please complete previous sections.")


Home()