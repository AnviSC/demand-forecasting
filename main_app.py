import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from model import train_prophet_model
from external import get_google_trends, get_weather_forecast
from supply import analyze_supply_chain

# --- Page Setup ---
st.set_page_config(
    page_title="AI Demand Forecaster",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI-Powered Demand & Supply Chain Dashboard")

# --- Helper Function for Gauge ---
def create_gauge_chart(days):
    """Creates a Plotly gauge chart for days of stock."""
    if days > 30: # Cap the gauge at 30
        days = 30
        
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = days,
        title = {'text': "Days of Stock on Hand (Simulated)"},
        gauge = {
            'axis': {'range': [0, 30], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': "rgba(0,0,0,0.1)"}, # background
            'steps': [
                {'range': [0, 7], 'color': "#dc3545"},  # Red (Danger)
                {'range': [7, 20], 'color': "#28a745"}, # Green (Safe)
                {'range': [20, 30], 'color': "#ffc107"} # Yellow (Overstock)
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': days
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# --- Sidebar (Controls) ---
with st.sidebar:

    uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])
    
    st.subheader("AI Parameters")
    
    use_google_trends = st.checkbox("Include Google Trends", value=True)
    keyword = st.text_input("Google Trends Keyword", "sales")
    
    use_weather = st.checkbox("Include Weather Forecast", value=True)
    location = st.text_input("Weather Location (e.g., London,GB)", "London,GB")
    
    st.subheader("Risk Simulation")
    risk_factor = st.slider(
        "Risk/Tariff Factor", 
        min_value=0.5, 
        max_value=2.0, 
        value=1.0, 
        step=0.1,
        help="Simulate taxes or risk. 1.0 = normal, 1.2 = 20% cost increase, 0.8 = 20% demand drop."
    )
    
    days_to_forecast = st.slider("Days to Forecast", 7, 365, 30)
    
    run_button = st.button("Generate Forecast", type="primary")

# --- Main Page (Results) ---
if run_button and uploaded_file is not None:
    try:
        # 1. Load Data
        data = pd.read_csv(uploaded_file)
        data['date'] = pd.to_datetime(data['Date'], format='mixed')
        data['sales'] = data['Sales']
        
        st.subheader("1. Data Preview (First 5 Rows)")
        st.dataframe(data.head())
        
        with st.spinner("🧠 AI is thinking... (Fetching APIs and training model)"):
            
            # 2. Get External Data
            trends_df = get_google_trends(keyword) if use_google_trends else None
            weather_df = get_weather_forecast(location) if use_weather else None

            # 3. Train AI Model
            forecast_df, forecast_fig = train_prophet_model(
                data=data,
                days_to_forecast=days_to_forecast,
                risk_factor=risk_factor,
                trends_df=trends_df,
                weather_df=weather_df
            )
            
            # 4. Run Supply Chain Analysis
            analysis = analyze_supply_chain(data, forecast_df)
        
        st.success("🎉 Forecast and Analysis Complete!")
        
        # --- (MODIFIED) Visual 1: KPI Cards ---
        st.subheader("1. Key Performance Indicators (KPIs)")
        
        # Get data for KPIs
        avg_sales_hist = analysis['inventory']['Avg Historical Sales']
        
        col1, col2 = st.columns(2) # <-- Changed from 3 to 2 columns
        col1.metric( # <-- Changed from col2 to col1
            label="Avg Historical Sales",
            value=f"{avg_sales_hist}"
        )
        col2.metric( # <-- Changed from col3 to col2
            label="Inventory Status",
            value=analysis['inventory']['Status'].upper()
        )
        st.divider() # Adds a horizontal line

        # 6. Display Main Forecast
        st.subheader("2. AI-Powered Sales Forecast")
        st.plotly_chart(forecast_fig, use_container_width=True)
        
        st.divider()
        
        # 7. Visual: Supply Chain Dashboard
        st.subheader("3. AI-Powered Supply Chain Analysis")
        col1, col2 = st.columns([1, 2]) # Make the 2nd column 2x wider
        
        with col1:
            st.write("#### Inventory Status")
            days_num = analysis['inventory']['Days of Stock (num)']
            gauge_fig = create_gauge_chart(days_num)
            st.plotly_chart(gauge_fig, use_container_width=True)
            st.write(analysis['inventory'])

        with col2:
            st.write("#### 🚨 Prescriptive Alerts")
            for _, row in analysis['alerts'].iterrows():
                if row['Priority'] == 'High':
                    st.error(f"**{row['Product']}:** {row['Alert']}")
                elif row['Priority'] == 'Medium':
                    st.warning(f"**{row['Product']}:** {row['Alert']}")
                else:
                    st.info(f"**{row['Product']}:** {row['Alert']}")

            st.write("#### 💡 Recommendations")
            st.dataframe(analysis['recommendations'], use_container_width=True)

        st.divider()
        
        with st.expander("See Raw Forecast Data"):
            st.dataframe(forecast_df.tail(days_to_forecast))

    except FileNotFoundError:
        st.error(f"Error: The file '{uploaded_file.name}' was not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.exception(e) 
        
elif run_button and uploaded_file is None:
    st.warning("Please upload a CSV file to begin.")

else:
    st.info("Upload your 'sales_data.csv' and configure the AI parameters in the sidebar to start.")