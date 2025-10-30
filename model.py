import pandas as pd
from prophet import Prophet
# from prophet.plot import plot_plotly  <-- WE ARE REMOVING THIS
import plotly.graph_objects as go  # <-- WE ARE ADDING THIS
from typing import Optional, Tuple

def train_prophet_model(
    data: pd.DataFrame, 
    days_to_forecast: int, 
    risk_factor: float,
    trends_df: Optional[pd.DataFrame] = None,
    weather_df: Optional[pd.DataFrame] = None
) -> Tuple[pd.DataFrame, object]:
    """
    Trains the Prophet model, adding any provided external regressors.
    Returns the forecast DataFrame and the Plotly figure.
    """
    df_prophet = data.rename(columns={"date": "ds", "sales": "y"})
    df_prophet['cap'] = df_prophet['y'].max() * 1.5
    df_prophet['floor'] = 0
    
    model = Prophet(weekly_seasonality=True, daily_seasonality=False, growth='logistic')
    
    # --- DYNAMICALLY ADD REGRESSORS ---
    df_prophet['ds'] = pd.to_datetime(df_prophet['ds']).dt.tz_localize(None)

    if trends_df is not None:
        model.add_regressor('trends', prior_scale=0.5, mode='multiplicative')
        trends_df['ds'] = pd.to_datetime(trends_df['ds']).dt.tz_localize(None)
        df_prophet = pd.merge(df_prophet, trends_df, on='ds', how='left')

    if weather_df is not None:
        model.add_regressor('temp', prior_scale=0.5, mode='multiplicative')
        weather_df['ds'] = pd.to_datetime(weather_df['ds']).dt.tz_localize(None)
        df_prophet = pd.merge(df_prophet, weather_df, on='ds', how='left')

    df_prophet = df_prophet.fillna(method='ffill').fillna(method='bfill')
    
    print("Training Prophet model...")
    model.fit(df_prophet)
    
    # --- Build Future ---
    future = model.make_future_dataframe(periods=days_to_forecast)
    future['cap'] = df_prophet['cap'].max()
    future['floor'] = 0
    
    if trends_df is not None:
        future = pd.merge(future, trends_df, on='ds', how='left')
    
    if weather_df is not None:
        future = pd.merge(future, weather_df, on='ds', how='left')
        
    future = future.fillna(method='ffill').fillna(method='bfill')

    # --- Predict ---
    forecast = model.predict(future)
    
    # --- APPLY THE RISK/TARIFF FACTOR ---
    forecast['yhat'] = forecast['yhat'] * risk_factor
    forecast['yhat_lower'] = forecast['yhat_lower'] * risk_factor
    forecast['yhat_upper'] = forecast['yhat_upper'] * risk_factor

    print("Forecast generated successfully.")
    
    # --- (NEW) Manually Create the Plot ---
    fig = go.Figure()

    # 1. Add the Upper and Lower forecast bounds (the shaded area)
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat_upper'],
        mode='lines',
        line=dict(color='rgba(173, 216, 230, 0.5)'), # Light blue
        name='Upper Bound'
    ))
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat_lower'],
        mode='lines',
        line=dict(color='rgba(173, 216, 230, 0.5)'),
        fill='tonexty', # This shades the area between Upper and Lower
        fillcolor='rgba(173, 216, 230, 0.3)',
        name='Confidence Interval'
    ))

    # 2. Add the main forecast line
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat'],
        mode='lines',
        line=dict(color='blue', width=3),
        name='Forecast (yhat)'
    ))
    
    # 3. Add the historical data (black dots)
    fig.add_trace(go.Scatter(
        x=df_prophet['ds'],
        y=df_prophet['y'],
        mode='markers',
        marker=dict(color='black', size=5),
        name='Actual Sales'
    ))

    fig.update_layout(
        title="AI Sales Forecast (Manual Plot)",
        xaxis_title="Date",
        yaxis_title="Sales",
        hovermode="x unified"
    )

    return forecast, fig