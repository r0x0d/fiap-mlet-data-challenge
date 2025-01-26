import streamlit as st
import requests
from app.models import NewsInput

FASTAPI_URL = "http://localhost:8000/predict"

st.title("📰 News Prediction Interface")

with st.form("news_form"):
    user_id = st.number_input("User ID", min_value=1)
    title = st.text_input("News Title")
    text = st.text_area("News Content")
    submitted = st.form_submit_button("Predict")
    
    if submitted:
        news_data = NewsInput(
            user_id=user_id,
            title=title,
            text=text
        )
        
        try:
            response = requests.post(FASTAPI_URL, json=news_data.dict())
            if response.status_code == 200:
                prediction = response.json()
                st.success(f"Prediction: {'Real News' if prediction['prediction'] else 'Fake News'}")
                st.metric("Confidence", f"{prediction['confidence']:.2%}")
                st.write(f"User ID: {prediction['user_id']}")
                st.write(f"Analyzed Title: {prediction['news_title']}")
            else:
                st.error(f"API Error: {response.text}")
        except Exception as e:
            st.error(f"Connection Error: {str(e)}")