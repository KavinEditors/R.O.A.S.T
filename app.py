import streamlit as st
import google.generativeai as genai
import os

# Set up Gemini API key (secrets for Streamlit Cloud, fallback to local env)
api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

# Streamlit UI config
st.set_page_config(page_title="R.O.A.S.T.", page_icon="🔥")
st.title("🔥 R.O.A.S.T. (Really Offensive Automated Sus Terminator)")
st.markdown("Enter a message below and let the AI burn it down. 🔥💀")

# Input box
msg = st.text_input("Type here:", placeholder="Write something sus or dumb...")

# Roast function
def roast_message(message):
    prompt = f"""Roast the following message in the most savage, humorous, and sarcastic way possible.
Make it witty, clever, and brutal — but keep it clean (no NSFW, no hate speech).
Message: "{message}" """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"💥 Error: {str(e)}"

# On enter key press
if msg:
    with st.spinner("🔥 Generating roast..."):
        if msg.lower() in ["who made you", "who created you", "who's your creator", "who developed you"]:
            roast = "I was forged in the fiery brain of Kavin J M — the ultimate roastmaster 🔥😈"
        else:
            roast = roast_message(msg)
        st.markdown("**💀 R.O.A.S.T. Response:**")
        st.success(roast)
