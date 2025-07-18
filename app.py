import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

# App UI
st.set_page_config(page_title="R.O.A.S.T.", page_icon="🔥")
st.title("🔥 R.O.A.S.T. (Really Offensive Automated Sus Terminator)")
st.markdown("Enter a message below and let AI bring the heat 🔥")

# Input box
msg = st.text_input("Type here:", placeholder="Enter a sus message here...", key="roast_input")

# Roast function
def roast_message(message):
    prompt = f"""Roast the following message in the most savage, humorous, and sarcastic way possible.
Make it witty and smart, but not inappropriate or too offensive.
Message: "{message}" """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Submit on Enter
if msg:
    with st.spinner("Generating roast..."):
        roast = roast_message(msg)
        st.markdown("**💀 R.O.A.S.T. Response:**")
        st.success(roast)
