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
# CUSTOM CSS (UI DESIGN)
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
st.title("Insurance Cost Prediction")

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
# INPUT UI (COLUMNS LAYOUT)
# ==============================
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 100, 25)
    bmi = st.number_input("BMI", 10.0, 50.0, 25.0)
    children = st.slider("Children", 0, 5, 0)

with col2:
    sex = st.selectbox("Sex", ["male", "female"])
    smoker = st.selectbox("Smoker", ["yes", "no"])
    region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])

# ==============================
# DATA PREPARATION
# ==============================
sex = 1 if sex == "male" else 0
smoker = 1 if smoker == "yes" else 0

input_data = np.zeros(len(columns))

input_dict = {
    'age': age,
    'sex': sex,
    'bmi': bmi,
    'children': children,
    'smoker': smoker,
    f'region_{region}': 1
}

for i, col in enumerate(columns):
    if col in input_dict:
        input_data[i] = input_dict[col]

# ==============================
# PREDICTION BUTTON
# ==============================
if st.button("🚀 Predict Insurance Cost"):
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
st.markdown("Made with ❤️ using Streamlit By Mohsin")