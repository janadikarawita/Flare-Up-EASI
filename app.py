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
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

        .stApp {
            background: linear-gradient(to bottom, #A1C4FD, #C2E9FB);
            font-family: 'Montserrat', sans-serif;
        }
        .title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            font-style: italic;
            color: #1F1F1F;
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            background: linear-gradient(to right, #6A11CB, #2575FC);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtext {
            text-align: center;
            font-size: 18px;
            color: black;
        }
        .logo-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
        }
        .logo {
            width: 100px;
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
            transform: scale(1.05);
        }
        .result-card {
            background: rgba(255, 255, 255, 0.8);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            text-align: center;
            backdrop-filter: blur(10px);
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
            animation: flicker 1s infinite alternate;
        }
        @keyframes flicker {
            0% { opacity: 1; }
            100% { opacity: 0.5; }
        }
        .glow-effect {
            animation: glow 1.5s infinite alternate;
        }
        @keyframes glow {
            0% { box-shadow: 0 0 5px #6A11CB; }
            100% { box-shadow: 0 0 20px #2575FC; }
        }
    </style>
""", unsafe_allow_html=True)

# 💼 **Logo Placement**
st.markdown("""
    <div class="logo-container">
        <img src="logo.png.png" class="logo">
        <h1 class='title'>EASI Score & Flare-Up Prediction Tool</h1>
        <img src="tsmu_logo.png.png" class="logo">
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
erc = st.number_input("Eosinophil Relative Count (ERC, Raw %):", min_value=0.0, max_value=50.0, step=0.1, format="%.2f", key="erc_input", help="Enter raw ERC value from blood test.")
elr = st.number_input("Eosinophil-to-Lymphocyte Ratio (ELR, Raw):", min_value=0.0, max_value=5.0, step=0.01, format="%.2f", key="elr_input", help="Enter calculated ELR value.")

# 🚀 Prediction Logic
if st.button("Predict", key="predict_button"):
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
