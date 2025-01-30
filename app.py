import streamlit as st
import numpy as np
import joblib

# Load the updated trained models
easi_model = joblib.load('easi_prediction_model.pkl')  # Updated model for predicting EASI scores
flare_model = joblib.load('flare_prediction_model.pkl')  # Updated model for predicting flare-up risk

# App title
st.title("EASI Score and Flare-Up Prediction Tool")
st.write("Predict future EASI scores and flare-ups based on ERC and ELR values.")

# Input fields for required features
erc = st.number_input("Eosinophil Relative Count (ERC, normalized):", min_value=0.0, max_value=1.0, step=0.01)
elr = st.number_input("Eosinophil-to-Lymphocyte Ratio (ELR, normalized):", min_value=0.0, max_value=1.0, step=0.01)

# Predict button
if st.button("Predict"):
    # Prepare input for prediction
    input_data = np.array([[erc, elr]])

    try:
        # Predict future EASI score
        predicted_easi = easi_model.predict(input_data)

        # Predict flare-up
        flare_prediction = flare_model.predict(input_data)
        flare_risk = "Yes" if flare_prediction[0] == 1 else "No"

        # Display results
        st.write(f"Predicted Future EASI Score: {predicted_easi[0]:.2f}")
        st.write(f"Future Flare-Up Risk: {flare_risk}")
    except ValueError as e:
        st.error(f"An error occurred during prediction: {e}")
