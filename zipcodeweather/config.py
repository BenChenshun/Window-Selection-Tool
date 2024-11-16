# config.py

import os

# Base directory of the package
BASE_DIR = os.path.dirname(__file__)

# Paths to data files
WEATHER_STATIONS_PATH = os.path.join(BASE_DIR, '../data/weather_data.csv')
CLIMATE_ZONE_GEOJSON_PATH = os.path.join(BASE_DIR, '../data/Climate_Zones_-_DOE_Building_America_Program.geojson')