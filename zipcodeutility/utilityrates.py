import pandas as pd
from .zipcode_state import get_state_from_zip
from .config import UTILITY_RATES_PATH

class ZipCodeUtility:
    """
    A class to get electricity and heating fuel rates by zip code and fuel type.
    """

    def __init__(self, rates_df=None):
        self.rates_df = rates_df or pd.read_csv(UTILITY_RATES_PATH)

    def get_rates(self, zip_code, fuel_type):
        """
        Return both the electricity rate and the selected heating fuel rate
        for a given zip code.

        Parameters:
        - zip_code (str or int): The user's zip code.
        - fuel_type (str): One of the fuel types like 'Natural Gas', 'Propane', etc.

        Returns:
        - dict: A dictionary with 'electricity_rate' and 'heating_fuel_rate'.
        """
        try:
            state = get_state_from_zip(zip_code).upper()
            fuel = fuel_type.title()  # Capitalize to match dataset columns

            if fuel not in self.rates_df.columns:
                return {"error": f"Fuel type '{fuel_type}' not found in dataset."}

            match = self.rates_df[self.rates_df["State"].str.upper() == state]

            if not match.empty:
                electricity_rate = float(match["Electricity"].values[0])*0.01/0.003413
                heating_fuel_rate = float(match[fuel].values[0])
                return {
                    "electricity_rate": electricity_rate,
                    "heating_fuel_rate": heating_fuel_rate
                }
            else:
                return {"error": f"No data found for state '{state}'."}
        except Exception as e:
            return {"error": str(e)}