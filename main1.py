import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import streamlit as st
from data_fetch import fetch_live_data
from datetime import datetime

# CSS for background styling
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
    [data-testid="stSidebar"] { background-color: #26027B;
        opacity: 1;
    }
    [data-testid="element-container"] {
        background-color: rgba(0, 0, 0, 0);
        opacity: 1;
    }
    .big-font {
        font-size:24px !important;
        font-weight: bold;
        color: black;  /* Changed subheader color to black */
    }
    table {
        background-color: transparent !important;
        width: 100%;
    }
    .stTable td, .stTable th {
        background-color: rgba(255, 255, 255, 0.3) !important;
        color: black;
    }
</style>
"""

st.markdown(css_code, unsafe_allow_html=True)

# Title of the web app
st.title("Cryptocurrency Price Prediction")

# Sidebar navigation with selectbox for persistent options
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a Page", ["Home", "Live Data", "Historical Data", "Forecasting"])

# Home Page
if page == "Home":
    st.subheader("Welcome to the Cryptocurrency Price Prediction App")
    st.write("Use the sidebar to navigate between live data, historical data, and forecasting sections.")

# Live Data Page
elif page == "Live Data":
    st.markdown('<p class="big-font">Live Bitcoin Price Data</p>', unsafe_allow_html=True)
    live_data = fetch_live_data()
    price_data = pd.DataFrame(live_data)
    st.write(price_data)

# Historical Data Page
elif page == "Historical Data":
    st.markdown('<p class="big-font">Historical Data</p>', unsafe_allow_html=True)
    csv_file_path = "crypto_data.csv"
    price_data = pd.read_csv(csv_file_path, header=None, names=["name", "timestamp", "o", "h", "l", "c"])
    st.write(price_data)

# Forecasting Page
elif page == "Forecasting":
    st.markdown('<p class="big-font">Bitcoin Price Forecasting</p>', unsafe_allow_html=True)

    # Load the dataset for forecasting
    df = pd.read_csv("new_BTC_data.csv")
    df['ds'] = pd.to_datetime(df['ds'].fillna(method='ffill'), errors='coerce')
    df['y'] = df['y'].fillna(method='ffill')
    
    # Prepare the dataframe for Prophet model
    prophet_df = df[['ds', 'y']].copy()

    # Initialize the model and train it
    m = Prophet()
    m.fit(prophet_df)

    # Make future predictions for the next 3 years (1095 days)
    future = m.make_future_dataframe(periods=1095)
    forecast = m.predict(future)

    # Convert min_date and max_date to native datetime for compatibility with st.slider
    min_date = forecast['ds'].min().to_pydatetime()
    max_date = forecast['ds'].max().to_pydatetime()
    
    # Date range slider
    selected_date_range = st.slider(
        "Select Date Range for Bitcoin Price Forecast",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )

    # Filter forecast data based on selected date range
    filtered_forecast = forecast[(forecast['ds'] >= selected_date_range[0]) & (forecast['ds'] <= selected_date_range[1])]
    
    # Display filtered forecast data
    st.write("Filtered Forecast Data:")
    st.write(filtered_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

    # Plot filtered forecast
    st.subheader("Filtered Forecast Plot")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(filtered_forecast['ds'], filtered_forecast['yhat'], label='Predicted Price')
    ax.fill_between(filtered_forecast['ds'], filtered_forecast['yhat_lower'], filtered_forecast['yhat_upper'], color='lightgray', label='Confidence Interval')
    plt.xlabel('Date')
    plt.ylabel('Predicted Close Price')
    plt.title('Bitcoin Price Forecast for Selected Date Range')
    plt.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Save the forecast to a CSV file
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv('forecast.csv', index=False)

    st.write("Forecast saved as 'forecast.csv'")
