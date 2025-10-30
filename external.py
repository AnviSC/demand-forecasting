import pandas as pd
from pytrends.request import TrendReq
import pyowm
from datetime import datetime

# --- CONFIGURATION ---
# PASTE YOUR FREE API KEY HERE
OPENWEATHER_API_KEY = "b6b7d61dc901c0612b1273ef0f953b79" 
OWM = pyowm.OWM(OPENWEATHER_API_KEY)
WeatherMgr = OWM.weather_manager()

def get_google_trends(keyword: str):
    """
    Gets Google Trends data for the last 5 years.
    Returns a DataFrame or None.
    """
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        timeframe = 'today 5-y' 
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='', gprop='')
        trends_df = pytrends.interest_over_time()
        
        if trends_df.empty or keyword not in trends_df.columns:
            print(f"Google Trends: No data found for keyword '{keyword}'")
            return None
            
        trends_df = trends_df.reset_index().rename(columns={"date": "ds", keyword: "trends"})


        print("Google Trends data fetched successfully.")
        return trends_df[['ds', 'trends', 'floor', 'cap']]
    except Exception as e:
        print(f"Google Trends Error: {e}")
        return None

def get_weather_forecast(location: str = 'London,GB'):
    """
    Gets the 5-day/3-hour forecast and resamples to daily average.
    Returns a DataFrame or None.
    """
    try:
        forecast = WeatherMgr.forecast_at_place(location, '3h').forecast
        weather_data = []
        for weather in forecast:
            date = weather.reference_time('datetime')
            temp = weather.temperature('celsius')['temp']
            weather_data.append({'ds': date, 'temp': temp})
            
        weather_df = pd.DataFrame(weather_data)
        weather_df['ds'] = pd.to_datetime(weather_df['ds']).dt.tz_localize(None)
        weather_df = weather_df.set_index('ds').resample('D').mean().reset_index()
        
        
        print("Weather data fetched successfully.")
        return weather_df
    except Exception as e:
        print(f"Weather API Error: {e}. (Have you set your API key in external.py?)")
        return None