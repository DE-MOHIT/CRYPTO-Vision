import pandas as pd
from prophet import Prophet  # Install the package using `pip install prophet`
import matplotlib.pyplot as plt
import streamlit as st
from data_fetch import fetch_live_data

#background color
css_code = """
<style>
    [data-testid="stAppViewContainer"] {
     background-color: #e5e5f7;
    opacity: 0.8;
    background-image: radial-gradient(circle at center center, #444cf7, #e5e5f7), repeating-radial-gradient(circle at center center, #444cf7, #444cf7, 10px, transparent 20px, transparent 10px);
    background-blend-mode: multiply;
    }
    [data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
    }
    [data-testid="element-container"] {
    background-color: rgba(0, 0, 0, 0);
    opacity: 1;
    }

</style>
"""

st.markdown(css_code, unsafe_allow_html=True)

csv_file_path = "crypto_data.csv"
#Title of the web app
st.title("Cryptocurrency Price Prediction")

#setup siderbar

# Fetch the live data
live_data = fetch_live_data()

# Center Table
st.subheader("Live Bitcoin Price Data")
price_data = pd.read_csv(csv_file_path, header=None, names=["name", "timestamp", "o", "h", "l", "c"])
  # Convert dictionary to pandas DataFrame
price_data = pd.DataFrame(live_data)
st.write(price_data)

# Display the historical data
#st.subheader("Historical Data")price_data1 = pd.read_csv("new_BTC_data.csv ", header=None, names=["ds", "y"])
  # Convert dictionary to pandas DataFrameprice_data1 = pd.DataFrame()
# Display the chart with historical datafig, ax = plt.subplots()ax.plot(price_data1['ds'], price_data1['y'])plt.xticks(rotation=45)st.pyplot(fig)live_data

# Load the dataset

df = pd.read_csv("new_BTC_data.csv")
df['ds'] = df['ds'].fillna(method='ffill')  # forward fill (fill with the previous value)
df['y'] = df['y'].fillna(method='ffill')
df['ds'] = pd.to_datetime(df['ds'], errors='coerce')
#df.rename(columns={'ds'}, inplace=True)


# Prepare the dataframe for Prophet model
prophet_df = df[['ds', 'y']].copy()
#prophet_df.rename(columns={'date': 'ds', 'c': 'y'}, inplace=True)

# Convert 'ds' to datetime format
prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])

# Initialize the model
m = Prophet()

# Train the model
m.fit(prophet_df)

# Make future predictions for the next 3 years (1095 days)
future = m.make_future_dataframe(periods=1095)
forecast = m.predict(future)

# Plot the forecast
st.subheader("Daily Forecast")
plt.figure(figsize=(10, 6))
m.plot(forecast)
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title('Bitcoin Price Prediction')
plt.show()
st.pyplot(plt)

st.subheader("Weakly Forecast")
fig2 = m.plot_components(forecast)
st.pyplot(fig2)

# Save the forecast to a CSV
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv('forecast.csv', index=False)

# ploting graph fromforecast.csv
#fc = pd.read_csv('forecast.csv')
#fig, ax = plt.subplots()
#fig1 = m.plot(fc)
#st.pyplot(fig1)