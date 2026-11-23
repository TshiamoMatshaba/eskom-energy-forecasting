import requests
import pandas as pd
import os

# Johannesburg coordinates
LATITUDE = -26.2041
LONGITUDE = 28.0473

# We will fetch 2 years of data to give the model enough history
START_DATE = "2022-0-01"
END_DATE = "2023-12-31"

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": START_DATE,
    "end_date": END_DATE,
    # We are pulling temperature, humidity, and wind speed
    "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
    "timezone": "Africa/Johannesburg"
}

print(f"Fetching weather data from {START_DATE} to {END_DATE}...")
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    # Convert to Pandas DataFrame
    df = pd.DataFrame(data['hourly'])
    
    # Rename 'time' to 'timestamp' and convert to datetime
    df.rename(columns={'time': 'timestamp'}, inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Ensure the data folder exists
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    filepath = 'data/joburg_weather.csv'
    df.to_csv(filepath, index=False)
    
    print(f"Success! {len(df)} hours of weather data saved to {filepath}")
    print(df.head())
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")