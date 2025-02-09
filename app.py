import streamlit as st
import joblib
import numpy as np
from PIL import Image
import time
import random

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

# Custom CSS for background gradient and animations
background_css = """
<style>
    body {
        background: linear-gradient(135deg, #dfc2fc, #5f5ed4, #4993de) !important;
        background-attachment: fixed;
    }
    .title-text {
        font-family: 'Montserrat', sans-serif;
        font-size: 3rem;
        font-weight: bold;
        color: white;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.6);
        text-align: center;
        animation: glow 1.5s infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.6); }
        to { text-shadow: 6px 6px 12px rgba(0, 0, 0, 0.8); }
    }
    .small-text {
        color: black;
        font-size: 1rem;
    }
    .circular-img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }
</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

# Load and display logos
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    logo1 = Image.open("logo.png.png").resize((40, 40))
    st.image(logo1, use_container_width=False)
with col3:
    logo2 = Image.open("tsmu_logo.png.png").resize((40, 40))
    st.image(logo2, use_container_width=False)

# Title with animated effects
st.markdown('<div class="title-text">EASI Score & Flare-Up Prediction Tool</div>', unsafe_allow_html=True)

# Input fields
st.markdown("### <span class='small-text'>Eosinophil Relative Count (ERC, Raw %):</span>", unsafe_allow_html=True)
erc = st.number_input("", min_value=0.0, max_value=100.0, step=0.01, key="erc")
st.markdown("### <span class='small-text'>Eosinophil-to-Lymphocyte Ratio (ELR, Raw):</span>", unsafe_allow_html=True)
elr = st.number_input("", min_value=0.0, max_value=10.0, step=0.01, key="elr")

# Predict button
if st.button("Predict"):
    with st.spinner("Processing..."):
        time.sleep(2)
        easi_score = easi_model.predict(np.array([[erc, elr]]))[0]
        flare_risk = flare_model.predict(np.array([[erc, elr]]))[0]
    
    # Show confetti animation if flare-up risk is low
    if flare_risk:
        st.markdown("""<h3 style='color:red; text-align:center;'>🔥 Future Flare-Up Risk: Yes</h3>""", unsafe_allow_html=True)
        st.markdown("""<h3 style='text-align:center;'>⚠️ Please consult with a specialist.</h3>""", unsafe_allow_html=True)
    else:
        st.markdown("""
            <script>
                function confettiEffect() {
                    const duration = 5 * 1000;
                    const animationEnd = Date.now() + duration;
                    const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };
                    
                    function randomInRange(min, max) {
                        return Math.random() * (max - min) + min;
                    }
                    
                    const interval = setInterval(function() {
                        const timeLeft = animationEnd - Date.now();
                        if (timeLeft <= 0) {
                            return clearInterval(interval);
                        }
                        const particleCount = 50 * (timeLeft / duration);
                        confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.9), y: Math.random() - 0.2 } }));
                    }, 250);
                }
                confettiEffect();
            </script>
        """, unsafe_allow_html=True)
        st.markdown("""<h3 style='color:green; text-align:center;'>🎉 Future Flare-Up Risk: No</h3>""", unsafe_allow_html=True)
    
    st.markdown(f"""<h2 style='color:white; text-align:center;'>Predicted Future EASI Score: {easi_score:.2f}</h2>""", unsafe_allow_html=True)



