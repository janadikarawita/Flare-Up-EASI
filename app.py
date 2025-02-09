import streamlit as st
import joblib
import numpy as np
from PIL import Image
import time

# Load models
easi_model = joblib.load("easi_prediction_model.pkl")
flare_model = joblib.load("flare_prediction_model.pkl")

# Set page config
st.set_page_config(page_title="EASI Score & Flare-Up Prediction Tool", layout="wide")

# Sidebar with instructions and dark mode toggle
with st.sidebar:
    st.header("How to Use:")
    st.markdown("1️⃣ **Enter ERC (Eosinophil Relative Count)** from blood test.")
    st.markdown("2️⃣ **Enter ELR (Eosinophil-to-Lymphocyte Ratio).**")
    st.markdown("3️⃣ **Click Predict** to see the results.")
    dark_mode = st.checkbox("🌙 Dark Mode")

# Custom CSS for background color and improved layout
st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] > .main {
            background-color: #f6f0ff !important;
            background-attachment: fixed !important;
        }
        .title-text {
            font-family: 'Montserrat', sans-serif;
            font-size: 3rem;
            font-weight: bold;
            color: white;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.6);
            text-align: center;
        }
        .small-text {
            font-weight: bold;
            color: white !important;
            font-size: 1rem;
        }
        .circular-img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: block;
            margin: auto;
        }
        .predict-button {
            display: block;
            width: 100%;
            padding: 12px;
            font-size: 1.2rem;
            font-weight: bold;
            color: white;
            text-align: center;
            background: linear-gradient(90deg, #6a11cb, #2575fc);
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }
        .predict-button:hover {
            background: linear-gradient(90deg, #2575fc, #6a11cb);
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load and display logos
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    logo1 = Image.open("logo.png.png").resize((40, 40))
    st.image(logo1, use_container_width=True, output_format='PNG')
with col3:
    logo2 = Image.open("tsmu_logo.png.png").resize((40, 40))
    st.image(logo2, use_container_width=True, output_format='PNG')

# Title
st.markdown('<div class="title-text">EASI Score & Flare-Up Prediction Tool</div>', unsafe_allow_html=True)

# Input fields
st.markdown("### <span class='small-text'>Eosinophil Relative Count (ERC, Raw %):</span>", unsafe_allow_html=True)
erc = st.number_input("", min_value=0.0, max_value=100.0, step=0.01, key="erc")
st.markdown("### <span class='small-text'>Eosinophil-to-Lymphocyte Ratio (ELR, Raw):</span>", unsafe_allow_html=True)
elr = st.number_input("", min_value=0.0, max_value=10.0, step=0.01, key="elr")

# Predict button
if st.button("Predict", key="predict", help="Click to predict"):
    with st.spinner("Processing..."):
        time.sleep(2)
        easi_score = easi_model.predict(np.array([[erc, elr]]))[0]
        flare_risk = flare_model.predict(np.array([[erc, elr]]))[0]
    
    # Show confetti animation if flare-up risk is low
    if flare_risk:
        st.markdown("""<h3 style='color:red; text-align:center;'>🔥 Future Flare-Up Risk: Yes</h3>""", unsafe_allow_html=True)
        st.markdown("""<h3 style='text-align:center;'>⚠️ Please consult with a specialist.</h3>""", unsafe_allow_html=True)
        
        # Display fire animation with "This is Fine" dog meme
        fire_gif = "https://media.tenor.com/7N8FsLxyxFIAAAAd/this-is-fine.gif"
        st.image(fire_gif, caption="This is fine", use_container_width=True)
    else:
        st.balloons()
        st.markdown("""<h3 style='color:green; text-align:center;'>🎉 Future Flare-Up Risk: No</h3>""", unsafe_allow_html=True)
    
    st.markdown(f"""<h2 style='color:#333; text-align:center;'>Predicted Future EASI Score: {easi_score:.2f}</h2>""", unsafe_allow_html=True)

