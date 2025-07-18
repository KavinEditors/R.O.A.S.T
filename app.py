import streamlit as st
import requests

# Get OpenRouter API key from Streamlit Secrets or local env
api_key = st.secrets["OPENROUTER_API_KEY"]

# OpenRouter endpoint
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Choose a model you have access to (gpt-3.5-turbo is safe)
MODEL = "openai/gpt-3.5-turbo"

# Streamlit page config
st.set_page_config(page_title="R.O.A.S.T.", page_icon="🔥")
st.title("🔥 R.O.A.S.T. (Really Offensive Automated Sus Terminator)")
st.markdown("Enter a message below and let the AI burn it down. 🔥💀")

# User input
msg = st.text_input("Type here:", placeholder="Write something sus or dumb...")

# Roast generator
def roast_message(message):
    if message.lower() in ["who made you", "who created you", "who's your creator", "who developed you"]:
        return "I was forged in the fiery brain of Kavin J M — the ultimate roastmaster 🔥😈"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a savage roastbot. Your job is to roast the user's message in a humorous, sarcastic, and brutal (but clean) way."},
            {"role": "user", "content": message}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        roast = response.json()["choices"][0]["message"]["content"].strip()
        return roast
    except Exception as e:
        return f"💥 Error: {str(e)}"

# Trigger roast
if msg:
    with st.spinner("🔥 Generating roast..."):
        roast = roast_message(msg)
        st.markdown("**💀 R.O.A.S.T. Response:**")
        st.success(roast)
