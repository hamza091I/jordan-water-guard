import streamlit as st
import pandas as pd
import joblib

# 1. Load the model and the label encoder
model = joblib.load('price_predictor_model.pkl')
le = joblib.load('district_encoder.joblib') # Use LOAD, not DUMP here!

st.set_page_config(page_title="Jordan Water Guard", page_icon="💧")

st.title("💧 Jordan Water Tanker Price Guard")
st.markdown("Check if you are paying a fair price for your water tanker.")

# 2. User Inputs
district = st.selectbox("Select your District:", le.classes_)
size = st.select_slider("Tanker Size (Cubic Meters):", options=[6, 10, 20])
distance = st.slider("Approx. distance from nearest well (km):", 5, 50, 15)
is_summer = st.toggle("Is there a water crisis/maintenance right now?")

# 3. Processing & Prediction
# We convert the district name back to the number the AI understands
dist_encoded = le.transform([district])[0]
input_data = pd.DataFrame([[dist_encoded, size, distance, 1 if is_summer else 0, 1]], 
                          columns=['District_Encoded', 'Size_m3', 'Distance_km', 'Is_Crisis', 'Has_Sticker'])

if st.button("Calculate Fair Price"):
    prediction = model.predict(input_data)[0]
    
    st.subheader(f"Fair Market Price: {round(prediction, 2)} JOD")
    
    # Logic for the "Non-Technical" Help
    st.info(f"💡 Standard price in {district} for a {size}m³ tank is usually between {round(prediction-2, 1)} and {round(prediction+2, 1)} JOD.")
    
    if is_summer:
        st.warning("⚠️ Prices are currently higher due to seasonal demand.")