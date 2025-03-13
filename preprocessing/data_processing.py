#%% md
# ## Weather data processing
#%%
from zipcodeweather import *
import pandas as pd

weather = ZipCodeWeather()

def get_weather_info(zip_code):
    """
    Retrieve weather station and climate zone information for a given zip code.

    Parameters:
    - zip_code (str): Zip code of the location.

    Returns:
    - pd.DataFrame: A DataFrame containing zip code, coordinates, nearest weather station info, and climate zone.
    """
    try:
        # Step 1: Find nearest weather station (returns a Series)
        nearest_station = weather.get_nearest_station(zip_code)

        # Step 2: Retrieve the climate zone as a string
        climate_zone = weather.get_climate_zone(zip_code)

        # Step 4: Combine all data into a DataFrame
        data = {
            "Zip Code": [zip_code],
            "winter_avg_temp": nearest_station['winter_avg_temp'],
            "summer_avg_temp": nearest_station['summer_avg_temp'],
            "Climate Zone": [climate_zone],
            "HDH": nearest_station['HDH'],
            "CDH": nearest_station['CDH'],
            "HDD": nearest_station['HDD'],
            "CDD": nearest_station['CDD'],
            "GHI": nearest_station['GHI']
        }
        
        # Concatenate both DataFrames along the columns
        final_df = pd.DataFrame(data)
        
        return final_df

    except ValueError as e:
        print(f"Error: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Example usage
if __name__ == "__main__":
    zip_code = "16803"  # Example zip code
    df = get_weather_info(zip_code)
    print(df)

#%%
def get_energystar_zone(zip_code):
    try:
        df = pd.read_csv('data/ClimateZones_County.csv')
        energystar_zone = df.loc[df['Zip Code'] == int(zip_code), 'ENERGY STAR Zone'].values[0]
        return energystar_zone

    except ValueError as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    zip_code = "16803"  # Example zip code
    energystar_zone = get_energystar_zone(int(zip_code))
    print(energystar_zone)

#%%
import numpy as np

# Function to calculate predicted window area
def calculate_predicted_window_area(conditioned_area, building_type, stories, wwr, foundation):
    if foundation == 'Heated Basement' and building_type == 'Single-Family Detached':
        foundation_area = conditioned_area / (stories + 1)
        solution = np.sqrt(foundation_area / 1.8)
        c = (solution + solution * 1.8) * 2
        return c * 8 * stories * (wwr * 0.01)

    elif foundation == 'Heated Basement' and building_type == 'Single-Family Attached':
        foundation_area = conditioned_area / (stories + 1)
        solution = np.sqrt(foundation_area / 0.5556)
        c = (solution + solution * 0.5556) * 2
        return c * 8 * stories * (wwr * 0.01)

    elif foundation != 'Heated Basement' and building_type == 'Single-Family Detached':
        foundation_area = conditioned_area / stories
        solution = np.sqrt(foundation_area / 1.8)
        c = (solution + solution * 1.8) * 2
        return c * 8 * stories * (wwr * 0.01)

    elif foundation != 'Heated Basement' and building_type == 'Single-Family Attached':
        foundation_area = conditioned_area / stories
        solution = np.sqrt(foundation_area / 0.5556)
        c = (solution + solution * 0.5556) * 2
        return c * 8 * stories * (wwr * 0.01)

    elif building_type == 'Apartment Unit':
        solution = np.sqrt(conditioned_area / 0.5556)
        c = (solution + solution * 0.5556) * 2
        return c * 8 * (wwr * 0.01)

    elif building_type == 'Mobile Home':
        solution = np.sqrt(conditioned_area / 1.8)
        c = (solution + solution * 1.8) * 2
        return c * 8 * (wwr * 0.01)
#%%
# surface area / volume
# Processed variables
def calculate_surface_volume_ratio(conditioned_area, building_type, stories, foundation):
    if foundation == 'Heated Basement' and building_type == 'Single-Family Detached':
        foundation_area = conditioned_area / (stories + 1)
        solution = np.sqrt(foundation_area / 1.8)
        volume = foundation_area * (stories + 1) * 8
        c = (solution + solution * 1.8) * 2
        surface_area = c * (stories + 1) * 8 + foundation_area
        return surface_area/volume

    elif foundation == 'Heated Basement' and building_type == 'Single-Family Attached':
        foundation_area = conditioned_area / (stories + 1)
        solution = np.sqrt(foundation_area / 0.5556)
        volume = foundation_area * (stories + 1) * 8
        c = (solution + solution * 0.5556) * 2
        surface_area = c * (stories + 1) * 8 + foundation_area
        return surface_area/volume

    elif foundation != 'Heated Basement' and building_type == 'Single-Family Detached':
        foundation_area = conditioned_area / stories
        solution = np.sqrt(foundation_area / 1.8)
        volume = foundation_area * stories * 8
        c = (solution + solution * 1.8) * 2
        surface_area = c * stories * 8 + foundation_area
        return surface_area/volume

    elif foundation != 'Heated Basement' and building_type == 'Single-Family Attached':
        foundation_area = conditioned_area / stories
        solution = np.sqrt(foundation_area / 0.5556)
        volume = foundation_area * stories * 8
        c = (solution + solution * 0.5556) * 2
        surface_area = c * stories * 8 + foundation_area
        return surface_area/volume

    elif building_type == 'Apartment Unit':
        solution = np.sqrt(conditioned_area / 0.5556)
        volume = conditioned_area * 8
        c = (solution + solution * 0.5556) * 2
        surface_area = c * 8 + conditioned_area
        return surface_area/volume

    elif building_type == 'Mobile Home':
        solution = np.sqrt(conditioned_area / 1.8)
        volume = conditioned_area * 8
        c = (solution + solution * 1.8) * 2
        surface_area = c * 8 + conditioned_area
        return surface_area/volume

#%%
# Convert orientation from str to number
def convert_orientation(orientation):
    if orientation == 'North': return 0
    if orientation == 'Northeast': return 45
    if orientation == 'East': return 90
    if orientation == 'Southeast': return 135
    if orientation == 'South': return 180
    if orientation == 'Southwest': return 225
    if orientation == 'West': return 270
    if orientation == 'Northwest': return 315

#%%
# Calculate heating & cooling period
def calculate_period(HDD, CDD):
    heating_period = HDD/(HDD+CDD)*12
    cooling_period = CDD/(HDD+CDD)*12
    return heating_period, cooling_period

