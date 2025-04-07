import pandas as pd
from .config import ZIPCODE_STATE_PATH

# Load once at module level
zipcode_df = pd.read_csv(ZIPCODE_STATE_PATH)
zipcode_df["Zip Code"] = zipcode_df["Zip Code"].astype(str)


def get_state_from_zip(zip_code):
    """
    Get the state abbreviation from a zip code using a local CSV dataset.

    Parameters:
    - zip_code (str or int): U.S. ZIP code

    Returns:
    - str: 2-letter state code (e.g. 'CA', 'PA')
    """
    zip_code = str(zip_code)
    match = zipcode_df[zipcode_df["Zip Code"] == zip_code]

    if not match.empty:
        return match.iloc[0]["State Abbrev."].upper()
    else:
        raise ValueError(f"Could not find state for zip code {zip_code}")