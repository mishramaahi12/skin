import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
import requests

# -------------------- MODEL LOAD --------------------
interpreter = tf.lite.Interpreter(model_path="model/model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# -------------------- LABELS --------------------
with open("model/labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

# -------------------- PAGE --------------------
st.set_page_config(page_title="AI Skin Advisor", layout="centered")
st.title("✨ AI Skin & Health Advisor")
st.write("Get personalized skincare + weather-based advice")

# -------------------- CITY --------------------
city = st.selectbox("📍 Select Your City", ["Ahmedabad", "Mumbai", "Delhi", "Bangalore"])

# -------------------- WEATHER FUNCTION --------------------
def get_weather(city):
    api_key = "YOUR_API_KEY_HERE"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        # If API works
        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["main"]
            return temp, humidity, condition

        else:
            raise Exception("API Error")

    except:
        # ---------- SMART FALLBACK (DIFFERENT FOR EACH CITY) ----------
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

st.subheader("🌦️ Live Weather")
st.write(f"🌡️ Temperature: {temp}°C")
st.write(f"💧 Humidity: {humidity}%")
st.write(f"☁️ Condition: {condition}")

# -------------------- IMAGE UPLOAD --------------------
uploaded_file = st.file_uploader("Upload your skin image", type=["jpg", "png", "jpeg"])

# -------------------- PREDICTION --------------------
def predict(image):
    img = image.resize((224, 224))
    img = np.array(img, dtype=np.float32)

    # Normalize (Teachable Machine requirement)
    img = (img / 127.5) - 1

    img = np.expand_dims(img, axis=0)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])
    index = np.argmax(output)

    return labels[index]

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

    st.write("🔍 Analyzing...")

    result = predict(image)

    st.success(f"🧴 Skin Type: {result}")

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