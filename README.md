# 🚀 AI-Powered Demand & Supply Chain Dashboard

This is an interactive Streamlit web application that uses machine learning to forecast demand, analyze supply chain risks, and provide prescriptive recommendations.



<img width="1704" height="979" alt="Screenshot 2025-10-31 at 5 19 19 AM" src="https://github.com/user-attachments/assets/76f840a3-24fb-463d-b4e8-39d97bfcb0c4" />


<img width="1390" height="611" alt="Screenshot 2025-10-31 at 5 19 33 AM" src="https://github.com/user-attachments/assets/2c2c0d54-82cd-48b8-b464-4a80d93d3688" />


<img width="1390" height="793" alt="Screenshot 2025-10-31 at 5 19 41 AM" src="https://github.com/user-attachments/assets/933258b9-531e-44d1-9bdc-e2af34a5ac4b" />


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
