import pandas as pd
import numpy as np

def analyze_supply_chain(historical_sales: pd.DataFrame, forecast_data: pd.DataFrame):
    """
    Takes historical sales and forecast data, runs supply chain
    analysis, and returns a dictionary of results.
    """
    
    # 1. Analyze Historicals
    avg_sales = historical_sales['sales'].mean()
    std_dev = historical_sales['sales'].std()
    
    # 2. Simulate Inventory (We simulate this for the demo)
    simulated_stock = avg_sales * np.random.uniform(5, 25) # 5 to 25 days of stock
    days_of_stock = simulated_stock / avg_sales
    
    status = "normal"
    if days_of_stock < 7: status = "understocked"
    if days_of_stock > 20: status = "overstocked"
    
    inventory_status = {
        "Avg Historical Sales": f"{avg_sales:,.2f} units/day",
        "Simulated Stock": f"{simulated_stock:,.0f} units",
        "Days of Stock (str)": f"{days_of_stock:.1f} days", # <-- RENAMED
        "Days of Stock (num)": days_of_stock,            # <-- NEW
        "Volatility": "High" if std_dev > (avg_sales * 0.5) else "Normal",
        "Status": status
    }
    
    # 3. Generate Alerts
    alerts = []
    if inventory_status["Status"] == "understocked":
        alerts.append({"Priority": "High", "Product": "Total Sales", "Alert": f"Low stock: Only {inventory_status['Days of Stock (str)']} of inventory remaining"})
    if inventory_status["Status"] == "overstocked":
        alerts.append({"Priority": "Medium", "Product": "Total Sales", "Alert": f"Overstock detected: {inventory_status['Days of Stock (str)']} of inventory on hand"})
    if inventory_status["Volatility"] == "High":
        alerts.append({"Priority": "Medium", "Product": "Total Sales", "Alert": "Unusual consumption pattern detected - high demand volatility"})

    # 4. Generate Recommendations (based on REAL forecast)
    recommendations = []
    # Get the average forecasted sales for the next 30 days
    future_avg = forecast_data[forecast_data['ds'] > pd.Timestamp.now(tz=None)]['yhat'].head(30).mean()

    # Check if future_avg is a valid number
    if pd.isna(future_avg):
        future_avg = avg_sales # Fallback to historical average

    if inventory_status["Status"] == "understocked":
        order_qty = (future_avg * 30) - simulated_stock # 30-day safety stock
        recommendations.append({
            "Priority": "Urgent",
            "Action": f"Order {order_qty:,.0f} units immediately",
            "Reason": "Stock level below safety threshold based on AI forecast"
        })
    
    if future_avg > (avg_sales * 1.3):
        recommendations.append({
            "Priority": "High",
            "Action": "Increase production capacity by 30%",
            "Reason": "AI forecasts a significant demand increase"
        })

    print("Supply chain analysis complete.")
    
    return {
        "inventory": inventory_status,
        "alerts": pd.DataFrame(alerts) if alerts else pd.DataFrame(columns=["Priority", "Product", "Alert"]),
        "recommendations": pd.DataFrame(recommendations) if recommendations else pd.DataFrame(columns=["Priority", "Action", "Reason"])
    }