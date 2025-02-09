import streamlit as st
import joblib
import numpy as np
import subprocess

# Ensure required dependencies are installed
required_packages = ["micropip"]
for package in required_packages:
    try:
        __import__(package)
    except ModuleNotFoundError:
        subprocess.check_call(["pip", "install", package])

# Load the trained models safely
def load_model(model_path):
    try:
        return joblib.load(model_path)
    except FileNotFoundError:
        st.error(f"Error: {model_path} not found. Please ensure the model file is uploaded.")
        return None

easi_model = load_model("easi_prediction_model.pkl")
flare_model = load_model("flare_prediction_model.pkl")

# 🌟 Page Config (Title & Theme)
st.set_page_config(
    page_title="EASI Score & Flare-Up Predictor",
    layout="centered",
    initial_sidebar_state="expanded",
)

# 🎨 Custom Styling
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to bottom, #A1C4FD, #C2E9FB);
        }
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            font-style: italic;
            color: #1F1F1F;
        }
        .subtext {
            text-align: center;
            font-size: 18px;
            color: #333333;
        }
        .logo-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            width: 120px;
        }
        div.stButton > button {
            width: 100%;
            border-radius: 10px;
            background: linear-gradient(to right, #6A11CB, #2575FC);
            color: white;
            font-size: 18px;
            padding: 10px;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background: linear-gradient(to right, #2575FC, #6A11CB);
        }
        .result-card {
            background: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .result-text {
            font-size: 22px;
            font-weight: bold;
        }
        .flare-no {
            color: #28a745;
        }
        .flare-yes {
            color: #dc3545;
        }
    </style>
""", unsafe_allow_html=True)

# 💼 **Logo Placement**
st.markdown("""
    <div class="logo-container">
        <img src="/mnt/data/logo.png.png" class="logo">
        <h1 class='title'>EASI Score & Flare-Up Prediction Tool</h1>
        <img src="/mnt/data/tsmu_logo.png.png" class="logo">
    </div>
""", unsafe_allow_html=True)

st.markdown("<p class='subtext'>Predict future EASI scores and flare-ups based on ERC and ELR values.</p>", unsafe_allow_html=True)
st.write("---")

# 📂 Sidebar Instructions
with st.sidebar:
    st.header("How to Use:")
    st.write("1️⃣ Enter ERC (Eosinophil Relative Count) from blood test.")
    st.write("2️⃣ Enter ELR (Eosinophil-to-Lymphocyte Ratio).")
    st.write("3️⃣ Click **Predict** to see the results.")

# 🔢 Input Fields
erc = st.number_input("Eosinophil Relative Count (ERC, Raw %):", min_value=0.0, max_value=50.0, step=0.1, format="%.2f")
elr = st.number_input("Eosinophil-to-Lymphocyte Ratio (ELR, Raw):", min_value=0.0, max_value=5.0, step=0.01, format="%.2f")

# 🚀 Prediction Logic
if st.button("Predict"):
    if easi_model is not None and flare_model is not None:
        input_data = np.array([[erc, elr]])
        easi_score = easi_model.predict(input_data)[0]
        flare_risk = flare_model.predict(input_data)[0]
        flare_risk_text = "Yes" if flare_risk == 1 else "No"
        flare_risk_class = "flare-yes" if flare_risk == 1 else "flare-no"

        # 🔄 Display Results in a Card
        st.markdown(f"""
            <div class='result-card'>
                <p class='result-text'>Predicted Future EASI Score: {easi_score:.2f}</p>
                <p class='result-text {flare_risk_class}'>Future Flare-Up Risk: {flare_risk_text}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Model loading failed. Please check the model files and try again.")
