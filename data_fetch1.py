import requests
import pandas as pd
from datetime import datetime

# Function to fetch data from the API
def fetch_crypto_data():
    today_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
    url = f"https://production.api.coindesk.com/v2/tb/price/values/BTC?start_date=2017-01-01T12:00&end_date={today_date}&ohlc=true&interval=1d"
    response = requests.get(url)
    data = response.json()['data']['entries']

    # Prepare data into a DataFrame
    df_bitcoin = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
    df_bitcoin['timestamp'] = pd.to_datetime(df_bitcoin['timestamp'], unit='ms')
    df_bitcoin.rename(columns={'timestamp': 'Date', 'close': 'Close'}, inplace=True)
    
    
    return df_bitcoin

# Save the data to a CSV
def update_csv(df, file_path='Crypto_data1.csv'):
    try:
        # Load existing data if available
        old_data = pd.read_csv(file_path)
        
        # Convert 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Drop rows where 'Date' could not be parsed
        df = df.dropna(subset=['Date'])

        # Combine and sort
        df_combined = pd.concat([old_data, df]).drop_duplicates(subset='Date').sort_values('Date')
        

    except FileNotFoundError:
        df_combined = df  # If file doesn't exist, use new data only
    
    # Save the updated data
    df_combined.to_csv(file_path, index=False)

# Fetch data and update CSV
df_bitcoin = fetch_crypto_data()
update_csv(df_bitcoin)
