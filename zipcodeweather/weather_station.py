# weather_station.py

from geopy.distance import geodesic
import pandas as pd
import os

# Load the default weather stations DataFrame
BASE_DIR = os.path.dirname(__file__)
WEATHER_STATIONS_PATH = os.path.join(BASE_DIR, '../data/weather_data.csv')
default_weather_stations = pd.read_csv(WEATHER_STATIONS_PATH)

def find_nearest_weather_station(user_coords, weather_stations=None):
    """
    Find the nearest weather station based on user's coordinates.

    Parameters:
    - user_coords (tuple): Latitude and longitude of the user's location.
    - weather_stations (pd.DataFrame): A DataFrame with columns 'Station_Name', 'Latitude', 'Longitude', and other weather parameters.

    Returns:
    - pd.Series: Information of the nearest weather station.
    """

    # Use default if no weather_stations DataFrame is provided
    if weather_stations is None:
        weather_stations = default_weather_stations

    distances = weather_stations.apply(
        lambda row: geodesic(user_coords, (row['Latitude'], row['Longitude'])).km, axis=1
    )
    closest_station = weather_stations.loc[distances.idxmin()]
    return closest_station