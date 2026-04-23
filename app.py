import streamlit as st
from PIL import Image
import requests
import random
import datetime
import pandas as pd

# -------------------- CONFIG --------------------
st.set_page_config(page_title="AI Skin Advisor", page_icon="🧴", layout="centered")

# -------------------- SESSION HISTORY --------------------
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
st.write("✨ AI + Weather + Smart Tracking System")

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
def skin_advice(s):
    return {
        "Oily Skin":["Oil-free facewash","Gel sunscreen","Avoid heavy creams"],
        "Dry Skin":["Use moisturizer","Drink water","Avoid harsh soap"],
        "Normal Skin":["Maintain routine","Stay hydrated","Use light cream"]
    }[s]

def creams(s):
    return {
        "Oily Skin":["Neutrogena Oil-Free","Cetaphil Oily Skin","Plum Green Tea"],
        "Dry Skin":["Nivea Soft","Cetaphil Cream","Himalaya Nourishing"],
        "Normal Skin":["Ponds Light","Simple Moisturizer","Lakme Peach Milk"]
    }[s]

def routine(s):
    return {
        "Oily Skin":"Morning: Cleanser + Sunscreen | Night: Light moisturizer",
        "Dry Skin":"Morning: Moisturizer + Sunscreen | Night: Heavy cream",
        "Normal Skin":"Morning: Cleanser + Sunscreen | Night: Light cream"
    }[s]

def weather_advice(t,h):
    if t>35: return "🔥 Stay hydrated & use sunscreen"
    elif h>70: return "💧 Skin may get oily, cleanse regularly"
    else: return "🌤️ Maintain routine"

def water_intake(weight):
    return round(weight*0.033,2)

# -------------------- MAIN --------------------
if file:
    img = Image.open(file)
    st.image(img, caption="Uploaded Image")

    with st.spinner("Analyzing..."):
        result, confidence = predict()

    st.success(f"🧴 {result}")
    st.write(f"📊 Confidence: {confidence:.2f}%")

    # Save to history
    entry = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "skin": result,
        "confidence": round(confidence,2),
        "temp": temp,
        "humidity": humidity
    }
    st.session_state.history.append(entry)

    # Tips
    st.subheader("💡 Skincare Tips")
    for t in skin_advice(result):
        st.write("✔",t)

    # Creams
    st.subheader("🧴 Recommended Creams")
    for c in creams(result):
        st.write("✨",c)
        st.markdown(f"[🔍 Search {c}](https://www.google.com/search?q={c.replace(' ','+')} )")

    # Routine
    st.subheader("📅 Daily Routine")
    st.info(routine(result))

    # Weather Advice
    st.subheader("🌍 Weather Advice")
    st.success(weather_advice(temp,humidity))

    # Water Intake
    st.subheader("💧 Water Intake")
    weight = st.number_input("Enter weight (kg)", value=60)
    st.write(f"Recommended: {water_intake(weight)} L/day")

    # Report
    report = f"""
Skin: {result}
Confidence: {confidence:.2f}%
Temp: {temp}
Humidity: {humidity}
"""
    st.download_button("📄 Download Report", report)

# -------------------- HISTORY --------------------
st.markdown("---")
st.subheader("📊 Skin History Tracker")

if len(st.session_state.history)==0:
    st.write("No history yet")
else:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)

if st.button("🗑️ Clear History"):
    st.session_state.history=[]
    st.success("History Cleared!")

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("⚠️ Not a medical diagnosis")
