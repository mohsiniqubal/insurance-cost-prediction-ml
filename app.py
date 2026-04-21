import streamlit as st
import pickle
import json
import numpy as np

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Insurance Predictor",
    page_icon="💰",
    layout="centered"
)

# ==============================
# CUSTOM CSS
# ==============================
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1 {
    text-align: center;
    color: #00C9A7;
}
.stButton>button {
    background-color: #00C9A7;
    color: white;
    font-size: 18px;
    border-radius: 10px;
    height: 50px;
    width: 100%;
}
.stButton>button:hover {
    background-color: #009e87;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# TITLE
# ==============================
st.title("💰 Insurance Cost Prediction")
st.info("⚠️ This prediction is based on a machine learning model and may vary.")
st.markdown("Enter your details below to estimate your insurance cost.")

# ==============================
# LOAD MODEL
# ==============================
try:
    with open('insurance_model.pkl', 'rb') as file:
        model = pickle.load(file)

    with open('columns.json', 'r') as f:
        columns = json.load(f)

except Exception as e:
    st.error(f"Error loading model or columns: {e}")
    st.stop()

# ==============================
# INPUT UI
# ==============================
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 100, 25)

    bmi = st.number_input(
        "BMI",
        min_value=0.0,
        max_value=60.0,
        value=25.0,
        step=0.1,
        help="Normal BMI range: 18.5 - 24.9"
    )

    if bmi <= 0:
        st.warning("⚠️ Please enter a valid BMI greater than 0.")

    st.caption("📊 Normal BMI range: 18.5 – 24.9")

    children = st.slider("Children", 0, 5, 0)

with col2:
    gender = st.radio(
        "Gender",
        ["👨 Male", "👩 Female"],
        horizontal=True
    )

    smoker = st.radio(
        "Smoker",
        ["🚬 Yes", "❌ No"],
        horizontal=True
    )

    region = st.selectbox(
        "Region",
        ["northeast", "northwest", "southeast", "southwest"]
    )

# ==============================
# DATA PREPARATION
# ==============================

# Convert UI → Model format
sex = 1 if "Male" in gender else 0
smoker = 1 if "Yes" in smoker else 0

# Validation
is_valid = True
if bmi <= 0:
    is_valid = False

# Create input array
input_data = np.zeros(len(columns))

# Map inputs
input_dict = {
    'age': age,
    'sex': sex,
    'bmi': bmi,
    'children': children,
    'smoker': smoker,
    f'region_{region}': 1
}

# Fill input array
for i, col in enumerate(columns):
    if col in input_dict:
        input_data[i] = input_dict[col]

# ==============================
# PREDICTION
# ==============================
if st.button("🚀 Predict Insurance Cost") and is_valid:
    prediction = model.predict([input_data])

    st.markdown(f"""
    <div style="background-color:#1c1f26;padding:20px;border-radius:10px">
        <h3 style="color:#00C9A7;text-align:center;">
        Estimated Cost: ₹ {prediction[0]:,.2f}
        </h3>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit by Mohsin")