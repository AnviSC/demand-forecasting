# 🚀 AI-Powered Demand & Supply Chain Dashboard

This is an interactive Streamlit web application that uses machine learning to forecast demand, analyze supply chain risks, and provide prescriptive recommendations.

![Dashboard Screenshot]([https://i.imgur.com/gLz8n2T.png](https://imagizer.imageshack.com/img924/250/rwywAm.png))

<img width="1704" height="979" alt="Screenshot 2025-10-31 at 5 19 19 AM" src="https://github.com/user-attachments/assets/76f840a3-24fb-463d-b4e8-39d97bfcb0c4" />

---

## ✨ Core Features

* **AI Forecasting:** Uses Facebook's `Prophet` model to analyze historical sales data and generate a robust, long-term forecast.
* **Live Data Integration:** Enriches the AI model with external data from **Google Trends** (for public interest) and **OpenWeatherMap** (for logistical planning).
* **"What-If" Risk Simulation:** An interactive "Risk/Tariff Factor" slider allows managers to instantly model the impact of external events (like new taxes or disruptions) on the forecast.
* **Prescriptive Analysis:** The dashboard automatically runs a supply chain analysis to generate:
    * **KPI Cards** (Avg. Sales, Inventory Status)
    * An **Inventory Gauge** (Days of Stock on Hand)
    * **Critical Alerts** (e.g., "Understocked," "High Volatility")
    * **Actionable Recommendations** (e.g., "Order 1,500 units immediately")

---

## 🛠️ Tech Stack

* **Frontend / UI:** Streamlit
* **Backend / Logic:** Python
* **Data Science:** Pandas, Prophet
* **External APIs:** Pytrends, PyOWM
* **Visualization:** Plotly (for charts)

---

## 🏃 How to Run

1.  **Clone/Download the Project:**
    (You already have this).

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the App:**
    ```bash
    streamlit run main_app.py
    ```
