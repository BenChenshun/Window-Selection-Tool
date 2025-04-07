# __init__.py

from zipcodeweather import ZipCodeWeather  # Import the main class from zipcodeweather.py
from .data_processing import (  # Import functions from data_processing.py
    get_weather_info,
    get_energystar_zone,
    calculate_predicted_window_area,
    calculate_surface_volume_ratio,
    convert_orientation,
    calculate_period,
    get_floor_area_bin,
    get_infiltration
)

# Initialize ZipCodeWeather instance
weather = ZipCodeWeather()

# Define __all__ to specify public objects of the module
__all__ = [
    "ZipCodeWeather",
    "get_weather_info",
    "get_energystar_zone",
    "calculate_predicted_window_area",
    "calculate_surface_volume_ratio",
    "convert_orientation",
    "calculate_period",
    "get_floor_area_bin",
    "get_infiltration"
]