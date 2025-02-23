import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os

API_URL = "https://production.api.coindesk.com/v2/tb/price/ticker?assets=all"
DATA_FILE = "crypto_data.csv"

data=[]

# Function to fetch live data from the API
def fetch_live_data():
    response = requests.get(API_URL)
    data = response.json()
    
    # Create a dictionary to store required fields
    live_data = []
    for asset, details in data['data'].items():
        live_data.append({
            "name": asset,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "o": details['ohlc']['o'],
            "h": details['ohlc']['h'],
            "l": details['ohlc']['l'],
            "c": details['ohlc']['c']
        })
    
    return pd.DataFrame(live_data)

# Function to save data to CSV file
def save_data(df):
    if not os.path.exists(DATA_FILE):
        df.to_csv(DATA_FILE, index=False)
    else:
        df.to_csv(DATA_FILE, mode='a', header=False, index=False)

# Function to fill missing days
def fetch_missing_data():
    if os.path.exists(DATA_FILE):
        # Load the existing data
        existing_data = pd.read_csv(DATA_FILE)
        
        # Find the last date from the existing data
        last_date = pd.to_datetime(existing_data['date']).max()
        
        # Get the current date
        current_date = datetime.now()

        # Check if any days are missing
        missing_days = (current_date - last_date).days
        if missing_days > 1:
            print(f"Fetching data for {missing_days - 1} missing days...")
            # Fill missing data
            for day in range(1, missing_days):
                missing_date = last_date + timedelta(days=day)
                print(f"Fetching data for {missing_date.strftime('%Y-%m-%d')}...")
                # Simulate fetching data for that specific date (if API supports it)
                # Here, we just fetch live data for demonstration
                live_data = fetch_live_data()
                live_data['date'] = missing_date.strftime("%Y-%m-%d %H:%M:%S")
                save_data(live_data)

# Main function to collect data continuously
def collect_data():
    # First, fill missing data if any
    fetch_missing_data()
    
    while True:
        # Fetch live data
        live_data = fetch_live_data()
        
        # Save the fetched data to the CSV file
        save_data(live_data)
        
        print(f"Fetched data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Sleep for 1 hour (or as per the frequency you want to collect)
        time.sleep(3600)

if __name__ == "__main__":
    collect_data()
