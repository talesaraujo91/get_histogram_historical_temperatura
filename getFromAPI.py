import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

def get_response(lat, lon, start_date, end_date):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
    	"latitude": lat,
    	"longitude": lon,
    	"start_date": start_date,
    	"end_date": end_date,
    	"hourly": ["temperature_2m", "relative_humidity_2m", "precipitation"]
    }
    responses = openmeteo.weather_api(url, params=params)
    
    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")

    
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    
    hourly_data = {"date": pd.date_range(
    	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
    	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
    	freq = pd.Timedelta(seconds = hourly.Interval()),
    	inclusive = "left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["precipitation"] = hourly_precipitation
    
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    
    return hourly_dataframe
"""
text = get_response(-25.4297, -49.2711,"2024-08-21","2024-09-05")  

import matplotlib.pyplot as plt

# Assuming your dataframe is named 'text'
# and it has a column named 'temperature_2m'

# Plotting the histogram
plt.figure(figsize=(10, 6))
plt.hist(text['temperature_2m'], bins=30, edgecolor='k', alpha=0.7)
plt.title('Histogram of Temperature at 2m')
plt.xlabel('Temperature (°C)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
# Trend
plt.plot(text['temperature_2m'], marker='o', linestyle='-', color='b')
plt.title('Trend Chart of Temperature at 2m')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.show()



hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)
"""