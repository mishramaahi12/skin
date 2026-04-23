import streamlit as st
from PIL import Image
import numpy as np
import requests
import random

# -------------------- PAGE --------------------
st.set_page_config(page_title="AI Skin Advisor", layout="centered")

st.title("✨ AI Skin & Health Advisor")
st.markdown("## 🌟 Smart AI-Based Skin & Health Recommendation System")

# -------------------- CITY --------------------
city = st.selectbox("📍 Select Your City", ["Ahmedabad", "Mumbai", "Delhi", "Bangalore"])

# -------------------- WEATHER FUNCTION --------------------
def get_weather(city):
    api_key = "YOUR_API_KEY"  # optional

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["main"]
            return temp, humidity, condition
        else:
            raise Exception("API error")

    except:
        # fallback (works always)
        if city == "Mumbai":
            return 32, 80, "Humid"
        elif city == "Delhi":
            return 38, 40, "Hot"
        elif city == "Bangalore":
            return 28, 60, "Cloudy"
        else:
            return 35, 70, "Hot"

# -------------------- WEATHER DISPLAY --------------------
temp, humidity, condition = get_weather(city)

st.subheader("🌦️ Weather Report")
st.write(f"🌡️ Temperature: {temp}°C")
st.write(f"💧 Humidity: {humidity}%")
st.write(f"☁️ Condition: {condition}")

# -------------------- IMAGE UPLOAD --------------------
uploaded_file = st.file_uploader("Upload your skin image", type=["jpg", "png", "jpeg"])

# -------------------- MOCK AI PREDICTION --------------------
def predict(image):
    skin_types = ["Oily Skin", "Dry Skin", "Normal Skin"]
    result = random.choice(skin_types)
    confidence = random.uniform(85, 98)
    return result, confidence

# -------------------- SKIN ADVICE --------------------
def skin_advice(skin):
    if "Oily" in skin:
        return [
            "Use oil-free facewash",
            "Avoid heavy creams",
            "Use gel-based sunscreen",
            "Wash face twice daily"
        ]
    elif "Dry" in skin:
        return [
            "Use heavy moisturizer",
            "Drink more water",
            "Avoid harsh soaps",
            "Apply sunscreen daily"
        ]
    else:
        return [
            "Maintain balanced skincare",
            "Use light moisturizer",
            "Stay hydrated"
        ]

# -------------------- WEATHER ADVICE --------------------
def weather_advice(temp, humidity):
    if temp > 35:
        return "🔥 Hot weather: Use sunscreen, stay hydrated, avoid sun exposure."
    elif humidity > 70:
        return "💧 Humid weather: Skin may get oily, cleanse regularly."
    elif temp < 15:
        return "❄️ Cold weather: Use heavy moisturizer."
    else:
        return "🌤️ Moderate weather: Maintain regular routine."

# -------------------- MAIN --------------------
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Analyzing image..."):
        result, confidence = predict(image)

    st.success(f"🧴 Skin Type: {result}")
    st.write(f"📊 Confidence: {confidence:.2f}%")

    # Skin Advice
    st.subheader("💡 Skincare Tips")
    for tip in skin_advice(result):
        st.write("✔", tip)

    # Weather Advice
    st.subheader("🌍 Weather-Based Advice")
    st.info(weather_advice(temp, humidity))

    # Health Tips
    st.subheader("🥗 Health Tips")
    st.write("✔ Drink 2–3L water daily")
    st.write("✔ Eat fruits & vegetables")
    st.write("✔ Sleep 7–8 hours")

    # -------------------- DOWNLOAD REPORT --------------------
    report = f"""
Skin Type: {result}
Confidence: {confidence:.2f}%

Weather:
Temperature: {temp}°C
Humidity: {humidity}%

Advice:
{', '.join(skin_advice(result))}
"""
    st.download_button("📄 Download Report", report, file_name="skin_report.txt")

# -------------------- DISCLAIMER --------------------
st.warning("⚠️ This is an AI-based suggestion system and not a medical diagnosis.")
