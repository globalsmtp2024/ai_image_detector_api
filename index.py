import streamlit as st
import requests
import json
from PIL import Image
import os
import time

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

API_USER = "1370547004"
API_SECRET = "zXbNU7cRCArtdRkXuGU4Kw9arzz8fb7B"

def detect_ai_image_with_api(image_path):
    params = {
        'models': 'genai',
        'api_user': API_USER,
        'api_secret': API_SECRET
    }
    with open(image_path, 'rb') as img_file:
        files = {'media': img_file}
        response = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

    if response.status_code == 200:
        output = json.loads(response.text)
        score = output.get("type", {}).get("ai_generated", None)
        if score is not None:
            if score >= 0.7:
                return "AI-Generated", score
            elif score <= 0.3:
                return "Real", score
            else:
                return "Uncertain", score
        else:
            return "Invalid Response", None
    else:
        return "Error", None

st.set_page_config(page_title="Centum Logics - AI Image Detection Tool", page_icon="🤖", layout="centered")

st.title('AI Image Detection Tool by Centum Logics')
st.markdown('### Welcome to the AI Image Detection Tool by Centum Logics!')
st.markdown('Upload an image to detect if it is **Real**, **AI-Generated**, or **Uncertain**.')

file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if file:
    st.image(file, caption="Uploaded Image", use_column_width=True)
    # st.write("Sending image to API for analysis...")
    file_path = os.path.join(UPLOAD_FOLDER, f"uploaded_{int(time.time())}.jpg")
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    prediction, confidence = detect_ai_image_with_api(file_path)

    if prediction == "Error":
        st.error("Something went wrong while calling the API.")
    elif prediction == "Invalid Response":
        st.error("The API did not return a valid prediction.")
    else:
        st.success(f"Prediction: **{prediction}**")
        # st.info(f"AI-Generated Confidence Score: `{confidence}`")
else:
    st.warning("Please upload an image to proceed.")
