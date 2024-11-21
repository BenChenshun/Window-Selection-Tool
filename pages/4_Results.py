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

summer_bill = st.session_state["summer_bill"]
winter_bill = st.session_state["winter_bill"]
baseline = st.session_state["baseline"]

def show_results(df):
    for i, row in df.iterrows():
        if (df["cooling_load"] == 0).all() and "cost_difference" in df.columns:
            stars = "⭐" * max(3 - i, 0)
            st.markdown(
                f"**{stars}{row['window_type']}🪟** \n"
                f"- Your house has no cooling need! ❄️\n"
                f"- Window Heating Contribution (%): {row['heating_window_percent']:.2f}% 🔥\n"
                f"- Heating Cost Related to Window ($): {row['heating_cost']:.2f}% 💲\n"
                f"- Total Cost Related to Window ($): {row['total_cost']:.2f} 💰\n"
                f"- Total Money Saved By Using This Window ($): {row['cost_difference'] if pd.notnull(row['cost_difference']) else 0.00:.2f} 💰"
            )
        elif (df["heating_load"] == 0).all() and "cost_difference" in df.columns:
            stars = "⭐" * max(3 - i, 0)
            st.markdown(
                f"**{stars}{row['window_type']}🪟** \n"
                f"- Window Cooling Contribution (%): {row['cooling_window_percent']:.2f}% ❄️\n"
                f"- Cooling Cost Related to Window ($): {row['cooling_cost']:.2f} 💲\n"
                f"- Your house has no heating need! 🔥\n"
                f"- Total Cost Related to Window ($): {row['total_cost']:.2f} 💰\n"
                f"- Total Money Saved By Using This Window ($): {row['cost_difference'] if pd.notnull(row['cost_difference']) else 0.00:.2f} 💰"
            )
        elif "cost_difference" in df.columns:
            stars = "⭐" * max(3 - i, 0)
            st.markdown(
                f"**{stars}{row['window_type']}🪟** \n"
                f"- Window Cooling Contribution (%): {row['cooling_window_percent']:.2f}% ❄️\n"
                f"- Window Heating Contribution (%): {row['heating_window_percent']:.2f}% 🔥\n"
                f"- Cooling Cost Related to Window ($): {row['cooling_cost']:.2f} 💲\n"
                f"- Heating Cost Related to Window ($): {row['heating_cost']:.2f} 💲\n"
                f"- Total Cost Related to Window ($): {row['total_cost']:.2f} 💰"
                f"- Total Money Saved By Using This Window ($): {row['cost_difference'] if pd.notnull(row['cost_difference']) else 0.00:.2f} 💰"
            )
        else:
            st.markdown(
                f"**{row['window_type']}🪟** \n"
                f"- Window Cooling Contribution (%): {row['cooling_window_percent']:.2f}% ❄️\n"
                f"- Window Heating Contribution (%): {row['heating_window_percent']:.2f}% 🔥\n"
                f"- Cooling Cost Related to Window ($): {row['cooling_cost']:.2f} 💲\n"
                f"- Heating Cost Related to Window ($): {row['heating_cost']:.2f} 💲\n"
                f"- Total Cost Related to Window ($): {row['total_cost']:.2f} 💰"
            )

st.write("** Summary of your house properties: **")
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


# Check if combined_window_database and necessary predictors are available
if "combined_window_database" in st.session_state and all(
    key in st.session_state for key in ['climatezone', 'zip_code', 'vintage', 'orientation',
                                         'wwr', 'window_area', 'cooling_setpoint', 'heating_setpoint',
                                         'HDH', 'CDH', 'winter_avg_temp', 'summer_avg_temp',
                                         'GHI', 'conditioned_area', 'sv']
):
    combined_window_database = st.session_state["combined_window_database"]
    # st.write(combined_window_database)
    # Initialize results DataFrame
    results = combined_window_database[["window_type"]].copy()

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
    # Add an average percentage for sorting
    results["average_percent"] = results.apply(
        lambda row: row["heating_window_percent"] if row["cooling_load"] == 0 else
        row["cooling_window_percent"] if row["heating_load"] == 0 else
        (row["cooling_window_percent"] + row["heating_window_percent"]) / 2,
        axis=1
    )

    # Add a $ value for corresponding window type based on user's utility bills
    results["cooling_cost"] = results.apply(
        lambda row: (row["cooling_window_percent"]/100 * summer_bill) if row["cooling_load"] > 1 else 0, axis = 1
    )
    results["heating_cost"] = results.apply(
        lambda row: (row["heating_window_percent"]/100 * winter_bill) if row["heating_load"] > 1 else 0, axis=1
    )

    # Total bills for window cooling + heating
    results["total_cost"] = results.apply(
        lambda row: (row["cooling_cost"] + row["heating_cost"]), axis=1
    )

    # Baseline result
    baseline_result = results.loc[results["window_type"] == baseline]

    # Money saved compared to the baseline model
    results["cost_difference"] = baseline_result["total_cost"].values[0] - results["total_cost"]
    sorted_results = results.sort_values(by="total_cost", ascending=True).reset_index(drop=True)
    top_3_results = sorted_results.head(3)

    st.write("### Baseline window performance:")
    show_results(baseline_result)

    top3 = st.button("🏆Make recommendations!")
    if top3:
        st.write("### Top 3 Recommended Windows:")
        show_results(top_3_results)

    # Add a button to toggle showing all results
    show_all = st.toggle("Show All Results")
    if show_all:
        st.write(sorted_results)

else:
    st.error("Missing necessary data or predictors. Please complete previous sections.")


Home()