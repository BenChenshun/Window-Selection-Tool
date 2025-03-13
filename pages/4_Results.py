import streamlit as st
import pickle
import numpy as np
import pandas as pd
from utils import Home, plot_energy_contributions
import category_encoders as ce
from IPython import embed

st.title("View the Results")

# Load the trained model from a .pkl file
## List of model file names and corresponding target variables
model_files = {
    "cooling_window": "models/cooling_window_lightgbm_lineartree.pkl",
    "heating_window": "models/heating_window_lightgbm_lineartree.pkl",
    "cooling_load": "models/cooling_load_lightgbm_lineartree.pkl",
    "heating_load": "models/heating_load_lightgbm_lineartree.pkl"
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

def load_label_encoder():
    with open("models/label_encoder.pkl", "rb") as f:
        return pickle.load(f)

# onehot_encoded_conditions = ['vintage']
target_encoded_conditions = ['climatezone', 'zip_code']
label_encoded_conditions = ['vintage']

target_encoders = load_target_encoders()
onehot_encoder = load_onehot_encoder()
label_encoder = load_label_encoder()

#Define general variables
summer_bill = st.session_state["summer_bill"]
winter_bill = st.session_state["winter_bill"]
baseline = st.session_state["baseline"]
heating_period = st.session_state["heating_period"]
cooling_period = st.session_state["cooling_period"]
energystar_zone = st.session_state["energystar_zone"]
lifespan = 15

def show_results(df):
    for i, row in df.iterrows():
        if (df["cooling_load"] == 0).all() and "cost_difference" in df.columns:
            # stars = "⭐" * max(3 - i, 0)
            st.markdown(
                # f"**{stars}{row['window_name']}🪟** \n"
                f"**{row['window_name']}🪟** \n"
                f"- Your house has no cooling need! ❄️\n"
                f"- Window Lifetime Heating Cost Save ($): {row['heating_difference']:.2f} 💲\n"
            )
            # plot_energy_contributions(row)
        elif (df["heating_load"] == 0).all() and "cost_difference" in df.columns:
            # stars = "⭐" * max(3 - i, 0)
            st.markdown(
                # f"**{stars}{row['window_name']}🪟** \n"
                f"**{row['window_name']}🪟** \n"
                f"- Window Lifetime Cooling Cost Save ($): {row['cooling_difference']:.2f} 💲\n"
                f"- Your house has no heating need! 🔥\n"
            )
            # plot_energy_contributions(row)
        elif "cost_difference" in df.columns:
            # stars = "⭐" * max(3 - i, 0)
            st.markdown(
                # f"**{stars}{row['window_name']}🪟** \n"
                f"**{row['window_name']}🪟** \n"
                f"- Window Lifetime Cooling Cost Save ($): {row['cooling_difference']:.2f} 💲\n"
                f"- Window Lifetime Heating Cost Save ($): {row['heating_difference']:.2f} 💲\n"
            )
            # plot_energy_contributions(row)
        else:
            st.markdown(
                f"**{row['window_name']}🪟** \n"
                # f"- Window Cooling Contribution (%): {row['cooling_window_percent']:.2f}% ❄️\n"
                # f"- Window Heating Contribution (%): {row['heating_window_percent']:.2f}% 🔥\n"
                f"- Monthly Cooling Cost Related to Window ($): {row['monthly_cooling_cost']:.2f} 💲\n"
                f"- Window Lifetime Cooling Cost ($): {row['lifetime_cooling_cost']:.2f} 💲\n"
                f"- Monthly Heating Cost Related to Window ($): {row['monthly_heating_cost']:.2f} 💲\n"
                f"- Window Lifetime Heating Cost ($): {row['lifetime_heating_cost']:.2f} 💲\n"

            )

    st.markdown("<p style='text-align: center;'>Percentage of heating/cooling energy contributed through windows</p>",
    unsafe_allow_html=True)
    plot_energy_contributions(df)

st.write(f"**Summary of your house properties:**")
# Display summary
if "zip_code" in st.session_state:
    st.write(f"Zip Code: {st.session_state['zip_code']}")
if "energystar_zone" in st.session_state:
    st.write(f"Energy Star Zone: {st.session_state['energystar_zone']}")
if "vintage" in st.session_state:
    st.write(f"Vintage: {st.session_state['vintage']}")
# if "house_type" in st.session_state:
#     st.write(f"House Type: {st.session_state['house_type']}")
# if "heating_setpoint" in st.session_state:
#     st.write(f"Heating Setpoint: {st.session_state['heating_setpoint']} °F")
# if "cooling_setpoint" in st.session_state:
#     st.write(f"Cooling Setpoint: {st.session_state['cooling_setpoint']} °F")
if "conditioned_area" in st.session_state:
    st.write(f"Floor Area: {st.session_state['conditioned_area']} sq ft")
# if "window_wall_ratio" in st.session_state:
#     st.write(f"Window-to-Wall Ratio: {st.session_state['window_wall_ratio']}%")


# Check if combined_window_database and necessary predictors are available
if "combined_window_database" in st.session_state and all(
    key in st.session_state for key in ['climatezone', 'zip_code', 'vintage', 'orientation',
                                        'conditioned_area', 'sv', 'cooling_setpoint', 'heating_setpoint',
                                        'wwr', 'window_area',
                                        'HDH', 'CDH', 'winter_avg_temp', 'summer_avg_temp', 'GHI']
):
    combined_window_database = st.session_state["combined_window_database"]
    # st.write(combined_window_database)
    # Initialize results DataFrame
    results = combined_window_database[["window_name"]].copy()

    # Prepare predictors for each window
    for _, row in combined_window_database.iterrows():
        predictors = []
        predictors.append({
            "climatezone": st.session_state["climatezone"],
            "zip_code": st.session_state["zip_code"],
            "vintage": st.session_state["vintage"],
            "orientation": st.session_state["orientation"],
            # "window_type": row["window_type"],
            "wwr": st.session_state["wwr"],
            "window_area": st.session_state["window_area"],
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
        label_encoded = label_encoder.fit_transform(predictors_df[label_encoded_conditions])
        # Convert the NumPy array to a DataFrame with appropriate column names
        label_encoded_df = pd.DataFrame(
            label_encoded,
            columns=label_encoded_conditions,
            index=predictors_df.index  # Use the same index as the original DataFrame
        )
        # Apply onehot encoding
        predictors_ready = predictors_df.drop(columns=label_encoded_conditions, axis=1).join(label_encoded_df)

        # Make predictions for each target using the respective model
        for target, model in models.items():
            # Apply target-specific encoding
            encoder = target_encoders[target]
            encoded_predictors = encoder.transform(predictors_ready[target_encoded_conditions])
            X = predictors_ready.drop(columns=target_encoded_conditions, axis=1).join(encoded_predictors)
            # Ensure compatibility with the model
            X = X[model["features"]].to_numpy()

            # Make predictions
            predictions = model["model"].predict(X)[0]

            # Add the prediction to the results DataFrame
            if target not in results.columns:
                results[target] = None  # Initialize the column if it doesn't exist

            results.loc[results["window_name"] == row["window_name"], target] = predictions
    # embed()
    # Apply Logic to Update Results
    results.loc[results["cooling_load"] < 5, ["cooling_load"]] = 0
    results.loc[results["heating_load"] < 5, ["heating_load"]] = 0

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
    results["monthly_cooling_cost"] = results.apply(
        lambda row: (row["cooling_window_percent"]/100 * summer_bill) if row["cooling_load"] > 1 else 0, axis = 1
    )
    results["lifetime_cooling_cost"] = results["monthly_cooling_cost"]*lifespan*cooling_period
    results["monthly_heating_cost"] = results.apply(
        lambda row: (row["heating_window_percent"]/100 * winter_bill) if row["heating_load"] > 1 else 0, axis=1
    )
    results["lifetime_heating_cost"] = results["monthly_heating_cost"] * lifespan * heating_period

    # Total bills for window cooling + heating
    results["monthly_total_cost"] = results.apply(
        lambda row: (row["monthly_cooling_cost"] + row["monthly_heating_cost"]), axis=1
    )
    results["lifetime_total_cost"] = results["lifetime_cooling_cost"]+results["lifetime_heating_cost"]

    # Baseline result
    baseline_result = results.loc[results["window_name"] == baseline]

    # Money saved compared to the baseline model

    results["cost_difference"] = baseline_result["monthly_total_cost"].values[0] - results["monthly_total_cost"]
    results["cooling_difference"] = (baseline_result["monthly_cooling_cost"].values[0] - results["monthly_cooling_cost"])*cooling_period*lifespan
    results["heating_difference"] = (baseline_result["monthly_heating_cost"].values[0] - results["monthly_heating_cost"])*heating_period*lifespan
    sorted_results = results.sort_values(by="lifetime_total_cost", ascending=True).reset_index(drop=True)
    # top_3_results = sorted_results.head(3)
    energystar_results = results.loc[results["window_name"].str.contains(energystar_zone)]

    st.write("### Baseline window performance:")
    show_results(baseline_result)

    # top3 = st.button("🏆Make recommendations!")
    # if top3:
    #     st.write("### Top 3 Recommended Windows:")
    #     show_results(top_3_results)

    energystar = st.button("🏆Make recommendations for Energy Star Windows!")
    if energystar:
        st.write("### Energy Star Recommended Windows:")
        show_results(energystar_results)

    # Add a button to toggle showing all results
    show_all = st.toggle("Show All Results")
    if show_all:
        st.write(sorted_results)

else:
    st.error("Missing necessary data or predictors. Please complete previous sections.")


Home()