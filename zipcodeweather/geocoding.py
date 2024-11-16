# geocoding.py

import requests

def get_coordinates(zip_code, country_code="US"):
    """
    Convert a zip code to latitude and longitude using OpenStreetMap's Nominatim API.

    Parameters:
    - zip_code (str): The zip code to convert.
    - country_code (str): The country code (default is "US" for United States).

    Returns:
    - tuple: Latitude and longitude as floats.
    """
    url = f"https://nominatim.openstreetmap.org/search?postalcode={zip_code}&countrycodes={country_code}&format=json"
    response = requests.get(url, headers={'User-Agent': 'zip-code-weather'})
    data = response.json()

    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    else:
        raise ValueError("Invalid zip code or location not found.")