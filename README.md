\# ⚡ Eskom Energy Load Forecasting



\## 📌 Overview

This project is an enterprise-grade machine learning pipeline designed to forecast South Africa's \*\*Residual Energy Demand\*\* (MW) based on historical weather data and Eskom grid performance metrics.



By predicting demand, this tool helps in understanding grid stress, forecasting load-shedding risks, and optimizing energy trading strategies.



\## 🛠️ Tech Stack

\- \\Data Engineering:\\ Python, Pandas, NumPy

\- \\Machine Learning:\\ XGBoost, Scikit-learn

\- \\Deployment:\\ Streamlit

\- \\Data Sources:\\ [Open-Meteo API](https://open-meteo.com/) (Weather), [Eskom Data Portal](https://www.eskom.co.za/dataportal/) (Grid Demand)



\## 🧠 Methodology 

1\. \\Missing Data Decision Matrix:\\ Handled minimal missing values (<5%) using row deletion to preserve distribution variance.

2\. \\Outlier Neutralization:\\ Applied IQR Winsorization (`numpy.clip`) to cap extreme demand spikes without breaking the time-series sequence.

3\. \\Vectorized Feature Engineering:\\ Engineered time features (`hour`, `month`), Lag features (`demand\_lag\_1`, `demand\_lag\_24`), and Rolling Averages (`temp\_rolling\_24`) using Pandas vectorization.

4\. \\Time-Based Splitting:\\ Trained on 2022-2025 data and strictly tested on 2026 data to prevent data leakage.



\## 📊 Model Performance

The XGBoost Regressor vastly outperformed the Naive 24-hour baseline:

\- \\Naive Baseline RMSE:\\ 1756.32

\- \\XGBoost RMSE:\\ 363.20

\- \\XGBoost MAPE:\\ 0.98%



\## 🔍 Key Findings (Feature Importance)

The model reveals that the time of day (`hour`), immediate past demand (`demand\_lag\_1`), and temperature (`temperature\_2m`) are the strongest predictors of energy demand, confirming the "Merit Order" dynamics where weather drives heating/cooling demand.


## 🚀 How to Run Locally
```bash
# 1. Clone the repository
git clone https://github.com/TshiamoMatshaba/eskom-energy-forecasting.git
cd eskom-energy-forecasting

# 2. Create a virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Streamlit app
streamlit run app.py

Author: Tshiamo Matshaba