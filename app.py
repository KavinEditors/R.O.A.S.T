import streamlit as st
import requests
import os

# Set page
st.set_page_config(page_title="R.O.A.S.T.", page_icon="🔥")
st.title("🔥 R.O.A.S.T. (Really Offensive Automated Sus Terminator)")
st.markdown("Enter a message and let the bot burn it down brutally... 😈")

# OpenRouter API Key
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"] if "OPENROUTER_API_KEY" in st.secrets else os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mixtral-8x7b"  # Or use "openai/gpt-3.5-turbo", etc.

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Detect creator questions
def is_creator_question(msg):
    triggers = ["who made", "who created", "your creator", "who did you", "developer"]
    return any(trigger in msg.lower() for trigger in triggers)

# Roast using OpenRouter
def get_roast(message):
    prompt = f"""
Roast this message in a clever, brutal, and sarcastic way. Keep it clean (no NSFW/hate).
Make sure it's at least 4 lines long.

Message to roast: "{message}"
"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://roast-app.streamlit.app",  # Replace with your app URL
        "X-Title": "ROAST App",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a savage roast bot. You destroy egos with humor."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        return reply.strip()
    except Exception as e:
        return "😏 R.O.A.S.T. Bot: 🔥 Couldn't roast properly right now. Try again later."

# Display chat
for entry in st.session_state.chat:
    if entry["sender"] == "user":
        st.markdown(f"😎 You: {entry['msg']}")
    else:
        st.markdown(f"😏 R.O.A.S.T. Bot: {entry['msg']}")

# Input box
col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input(" ", key="input", placeholder="Type your message here...", label_visibility="collapsed")
with col2:
    send = st.button("➡️")

# On Send
if send and user_input:
    st.session_state.chat.append({"sender": "user", "msg": user_input})

    if is_creator_question(user_input):
        reply = "I was created by the legendary **Kavin J M**, the roastmaster general. 🔥"
    else:
        reply = get_roast(user_input)

    st.session_state.chat.append({"sender": "bot", "msg": reply})
    st.experimental_rerun()
