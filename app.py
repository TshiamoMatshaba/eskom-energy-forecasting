import streamlit as st
import pandas as pd
import joblib

# 1. Setup the page
st.set_page_config(page_title="Eskom Demand Forecaster", page_icon="⚡", layout="wide")

st.title("⚡ Eskom Energy Demand Forecasting")
st.markdown("""
This interactive dashboard uses an **XGBoost Machine Learning model** to predict South Africa's Residual Energy Demand based on weather and grid conditions.
*Built by Tshiamo Matshaba*
""")

# 2. Load the model
@st.cache_resource
def load_model():
    return joblib.load('models/eskom_xgb_model.pkl')

model = load_model()

# 3. Create the Sidebar for User Inputs
st.sidebar.header("Simulate Grid Conditions")

hour = st.sidebar.slider("Hour of the Day (0-23)", 0, 23, 18) # Default to 6 PM
temp = st.sidebar.slider("Temperature (°C)", -5.0, 40.0, 15.0)
uclf = st.sidebar.slider("Total UCLF (Unplanned Outages %)", 0.0, 30.0, 10.0)

# We need to provide baseline values for the other features the model needs
# (In a real production app, these would be pulled from live data)
st.sidebar.markdown("---")
st.sidebar.markdown("*Using average historical values for Lag features*")
demand_lag_1 = 22000.0 # Average MW
demand_lag_24 = 21000.0 
temp_rolling_24 = 14.0
uclf_rolling_24 = 10.0

# 4. Construct the input dataframe
input_data = pd.DataFrame({
    'temperature_2m': [temp],
    'relative_humidity_2m': [50.0], # default
    'wind_speed_10m': [10.0], # default
    'hour': [hour],
    'day_of_week': [1], # Tuesday (default)
    'is_weekend': [0],
    'month': [6], # June (Winter - default)
    'demand_lag_1': [demand_lag_1],
    'demand_lag_24': [demand_lag_24],
    'temp_rolling_24': [temp_rolling_24],
    'uclf_rolling_24': [uclf_rolling_24]
})

# 5. Make the prediction
prediction = model.predict(input_data)[0]

# 6. Display the result
st.markdown("### Predicted Residual Demand")
st.metric(label="Estimated Demand (Megawatts)", value=f"{prediction:,.0f} MW")

if prediction > 28000:
    st.error("🚨 **CRITICAL LOAD:** Demand is extremely high. High risk of Load Shedding if outages (UCLF) remain this high.")
elif prediction > 24000:
    st.warning("⚠️ **ELEVATED LOAD:** Demand is peaking. Grid is under stress.")
else:
    st.success("✅ **STABLE GRID:** Demand is well within safe operational limits.")

st.markdown("---")
st.markdown("**Business Value:** This tool allows grid operators to simulate how changes in weather (temperature) and infrastructure failures (UCLF) impact the need for expensive peaking plants (like OCGTs).")