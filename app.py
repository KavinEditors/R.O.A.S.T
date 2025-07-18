import streamlit as st
import requests
import os

# Constants
MODEL = "openrouter:meta-llama/llama-3.1-8b-instruct"
API_URL = "https://openrouter.ai/api/v1/chat"
api_key = st.secrets["OPENROUTER_API_KEY"] if "OPENROUTER_API_KEY" in st.secrets else os.getenv("OPENROUTER_API_KEY")

# Emojis
BOT_EMOJI = "😏"
USER_EMOJI = "😎"

# Creator trigger
creator_keywords = ["who made you", "who created you", "who did you", "your creator"]

# Streamlit page setup
st.set_page_config(page_title="R.O.A.S.T.", page_icon="🔥")
st.title("🔥 R.O.A.S.T. (Really Offensive Automated Sus Terminator)")
st.markdown("Enter a message below and let the AI burn it down. 🔥💀")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Roast function
def roast_message(user_msg):
    if any(key in user_msg.lower() for key in creator_keywords):
        return "I was forged in the fiery brain of **Kavin J M** — the ultimate roastmaster 🔥😈"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    base_messages = [{"role": "system", "content": "You are a savage roastbot. Roast every user message with brutal sarcasm, wit, and humor. No NSFW. Minimum 4 lines."}]
    for entry in st.session_state.chat_history:
        base_messages.append({"role": "user", "content": entry["user"]})
        base_messages.append({"role": "assistant", "content": entry["bot"]})
    base_messages.append({"role": "user", "content": user_msg})

    last_working = ""
    for _ in range(3):
        try:
            res = requests.post(API_URL, headers=headers, json={
                "model": MODEL,
                "messages": base_messages
            })
            res.raise_for_status()
            reply = res.json()["choices"][0]["message"]["content"].strip()
            last_working = reply
            if len(reply.splitlines()) >= 4:
                return reply
        except Exception as e:
            return f"💥 Error: {str(e)}"

    return last_working or "🔥 Still too stunned to roast you. Try again soon."

# Display chat history
for entry in st.session_state.chat_history:
    st.markdown(f"{USER_EMOJI} **You:** {entry['user']}")
    st.markdown(f"{BOT_EMOJI} **R.O.A.S.T. Bot:** {entry['bot']}")

# Input area with aligned send button
col1, col2 = st.columns([8, 1])
with col1:
    user_input = st.text_input("", placeholder="Type your message here...", label_visibility="collapsed", key="input")
with col2:
    send_pressed = st.button("📩")

# Handle input
if user_input and send_pressed:
    with st.spinner("🔥 Generating roast..."):
        response = roast_message(user_input)
    st.session_state.chat_history.append({"user": user_input, "bot": response})
    st.rerun()
