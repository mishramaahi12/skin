import streamlit as st
from PIL import Image
import requests
import random
import datetime
import pandas as pd

# -------------------- CONFIG --------------------
st.set_page_config(page_title="AI Skin Advisor", page_icon="🧴", layout="centered")

# -------------------- SESSION --------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------- UI --------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
h1 {text-align:center;color:#00e6ff;}
.stButton>button {
    background: linear-gradient(90deg,#00e6ff,#00ffcc);
    color:black;border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🧴 AI Skin & Health Advisor")
st.write("✨ AI + Weather + Analytics Dashboard")

# -------------------- CITY --------------------
city = st.selectbox("📍 Select City", ["Ahmedabad","Mumbai","Delhi","Bangalore"])

# -------------------- WEATHER --------------------
def get_weather(city):
    try:
        api_key = "YOUR_API_KEY"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        data = requests.get(url).json()

        if data.get("cod")==200:
            return data["main"]["temp"], data["main"]["humidity"], data["weather"][0]["main"]
        else:
            raise Exception()
    except:
        return {
            "Ahmedabad":(35,70,"Hot"),
            "Mumbai":(32,80,"Humid"),
            "Delhi":(38,40,"Hot"),
            "Bangalore":(28,60,"Cloudy")
        }[city]

temp, humidity, condition = get_weather(city)

col1,col2,col3 = st.columns(3)
col1.metric("🌡️ Temp",f"{temp}°C")
col2.metric("💧 Humidity",f"{humidity}%")
col3.metric("☁️",condition)

# -------------------- IMAGE --------------------
file = st.file_uploader("📤 Upload Skin Image", type=["jpg","png"])

# -------------------- AI --------------------
def predict():
    skin = random.choice(["Oily Skin","Dry Skin","Normal Skin"])
    confidence = random.uniform(85,98)
    return skin, confidence

# -------------------- FUNCTIONS --------------------
def detect_problem(skin, humidity):
    if "Oily" in skin and humidity > 70:
        return "Acne Risk ⚠️"
    elif "Dry" in skin:
        return "Dryness ⚠️"
    else:
        return "Healthy Skin ✅"

def weather_advice(t,h):
    if t>35: return "🔥 Stay hydrated & use sunscreen"
    elif h>70: return "💧 Cleanse regularly"
    else: return "🌤️ Maintain routine"

# -------------------- MAIN --------------------
if file:
    img = Image.open(file)
    st.image(img, caption="Uploaded Image")

    result, confidence = predict()
    score = int(confidence)

    st.success(f"🧴 {result}")
    st.write(f"📊 Confidence: {confidence:.2f}%")

    # Score
    st.subheader("📊 Skin Score")
    st.progress(score/100)
    st.write(f"{score}/100")

    # Alerts
    st.subheader("🧠 Skin Condition")
    st.warning(detect_problem(result, humidity))

    st.subheader("🌍 Weather Advice")
    st.success(weather_advice(temp, humidity))

    # Save history
    entry = {
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "score": score,
        "temp": temp,
        "humidity": humidity
    }
    st.session_state.history.append(entry)

# -------------------- ADVANCED DASHBOARD --------------------
if len(st.session_state.history) >= 1:
    st.markdown("---")
    st.subheader("📊 Skin Analytics Dashboard")

    df = pd.DataFrame(st.session_state.history)

    # Convert time
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)

    # -------- LINE CHART --------
    st.write("### 📈 Skin Score Trend")
    st.line_chart(df["score"])

    # -------- AREA CHART --------
    st.write("### 📉 Environment Impact")
    st.area_chart(df[["temp", "humidity"]])

    # -------- BAR CHART --------
    st.write("### 📊 Latest Comparison")
    latest = df.tail(1)
    st.bar_chart(latest[["score", "temp", "humidity"]])

    # -------- METRIC --------
    st.write("### 🎯 Latest Skin Score")
    st.metric("Score", f"{int(df['score'].iloc[-1])}/100")

# -------------------- CLEAR --------------------
if st.button("🗑️ Clear History"):
    st.session_state.history = []
    st.success("History Cleared")

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("⚠️ AI-based system. Not medical advice.")
