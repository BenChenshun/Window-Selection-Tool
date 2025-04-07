# climatezone.py

import geopandas as gpd
from shapely.geometry import Point
import os

# Load the default weather stations DataFrame
BASE_DIR = os.path.dirname(__file__)
CLIMATE_ZONE_GEOJSON_PATH = os.path.join(BASE_DIR, '../data/Climate_Zones_-_DOE_Building_America_Program.geojson')
default_climate_zone = gpd.read_file(CLIMATE_ZONE_GEOJSON_PATH)

def get_climate_zone_from_geojson(user_coords, climate_zone=None):
    """
    Determine the climate zone based on latitude and longitude by checking
    if the point falls within any of the climate zones in a GeoJSON file.

    Parameters:
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.
    - climate_zones (gpd.DataFrame): A geopanda DataFrame containing climate zones and geometries (Polygons).

    Returns:
    - str: The climate zone that the point falls within.
    """

    # Use default if no weather_stations DataFrame is provided
    if climate_zone is None:
        climate_zone = default_climate_zone

    lat = user_coords[0]
    lon = user_coords[1]

    # Create a point from the latitude and longitude
    point = Point(lon, lat)

    # Check each polygon to see if the point falls within
    for _, row in climate_zone.iterrows():
        if row['geometry'].contains(point):
            return {
                'BA_Climate_Zone': row['BA_Climate_Zone'],
                'ASHRAE_IECC_Climate_Zone': f"{row['IECC_Climate_Zone']}{row['IECC_Moisture_Regime']}"
            }


    raise ValueError("Climate zone not found for this location.")