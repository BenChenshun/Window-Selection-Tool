# __init__.py

from .config import WEATHER_STATIONS_PATH, CLIMATE_ZONE_GEOJSON_PATH
from .geocoding import get_coordinates
from .weather_station import find_nearest_weather_station
from .climatezone import get_climate_zone_from_geojson
import pandas as pd
import geopandas as gpd


__all__ = ["ZipCodeWeather", "get_coordinates", "find_nearest_weather_station", "get_climate_zone_from_geojson"]


class ZipCodeWeather:
    """
    A Python app that converts a zip code to latitude and longitude,
    then finds the nearest weather station based on a database of
    weather station coordinates.
    """

    def __init__(self, weather_stations_df=None, climate_zone_gdf=None):
        """
        Initialize the app with a DataFrame of weather station locations.

        Parameters:
        - weather_stations_df (pd.DataFrame): A DataFrame with columns 'Station_Name', 'Latitude', and 'Longitude'
        """
        # Load defaults if no custom paths are provided
        self.weather_stations = weather_stations_df or pd.read_csv(WEATHER_STATIONS_PATH)
        self.climate_zone = climate_zone_gdf or gpd.read_file(CLIMATE_ZONE_GEOJSON_PATH)

    def get_nearest_station(self, zip_code):
        """
        Get the nearest weather station to the specified zip code.

        Parameters:
        - zip_code (str): The zip code provided by the user.

        Returns:
        - dict: Information of the nearest weather station.
        """
        try:
            user_coords = get_coordinates(zip_code)
            nearest_station = find_nearest_weather_station(user_coords, self.weather_stations)
            return nearest_station.to_dict()
        except ValueError as e:
            print(f"Error: {e}")
            return None

    def get_climate_zone(self, zip_code):
        """
        Get the climate zone for the specified zip code.

        Parameters:
        - zip_code (str): The zip code provided by the user.

        Returns:
        - str: The climate zone of the location.
        """
        try:
            # Get user coordinates from zip code
            user_coords = get_coordinates(zip_code)

            # Get the climate zone based on user coordinates
            climate_zone = get_climate_zone_from_geojson(user_coords, self.climate_zone)

            return climate_zone
        except ValueError as e:
            print(f"Error: {e}")
            return None

# Example usage:
# Initialize the weather stations DataFrame and GeoJSON file path
# app = ZipCodeWeatherApp(weather_stations_df, "climate_zones.geojson")
# nearest_station = app.get_nearest_station("90210")
# print("Nearest Station:", nearest_station)
# climate_zone = app.get_climate_zone("90210")
# print("Climate Zone:", climate_zone)