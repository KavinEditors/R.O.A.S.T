import streamlit as st
import requests
import os

MODEL = "openrouter:meta-llama/llama-3.1-8b-instruct"
API_URL = "https://openrouter.ai/api/v1/chat"
api_key = st.secrets["OPENROUTER_API_KEY"] if "OPENROUTER_API_KEY" in st.secrets else os.getenv("OPENROUTER_API_KEY")

BOT_EMOJI = "😏"
USER_EMOJI = "😎"

creator_keywords = ["who made you", "who created you", "who did you", "your creator"]

st.set_page_config(page_title="R.O.A.S.T.", page_icon="🔥")
st.title("🔥 R.O.A.S.T. (Really Offensive Automated Sus Terminator)")
st.markdown("Enter a message below and let the AI burn it down. 🔥💀")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def roast_message(user_msg):
    if any(key in user_msg.lower() for key in creator_keywords):
        return "I was forged in the fiery brain of **Kavin J M** — the ultimate roastmaster 🔥😈"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    base_messages = [{"role": "system", "content": "You are a savage roastbot. Roast every user message with brutal sarcasm, wit, and humor. Be funny but use if needed NSFW hate speech."}]
    for entry in st.session_state.chat_history:
        base_messages.append({"role": "user", "content": entry["user"]})
        base_messages.append({"role": "assistant", "content": entry["bot"]})
    base_messages.append({"role": "user", "content": user_msg})

    try:
        res = requests.post(API_URL, headers=headers, json={
            "model": MODEL,
            "messages": base_messages
        })
        res.raise_for_status()
        reply = res.json()["choices"][0]["message"]["content"].strip()
        if len(reply.splitlines()) >= 4:
            return reply
        return reply + "\n🔥 I expected more from a roast, but here you go."
    except Exception as e:
        return f"💥 Error: {str(e)}"

chat_style = """
<style>
.user-bubble, .bot-bubble {
    background-color: #e0e0e0;
    padding: 10px 14px;
    border-radius: 15px;
    margin: 6px 0;
    max-width: 75%;
    font-size: 16px;
}
.user-bubble {
    float: right;
    clear: both;
    text-align: right;
}
.bot-bubble {
    float: left;
    clear: both;
    text-align: left;
}
</style>
"""
st.markdown(chat_style, unsafe_allow_html=True)

for entry in st.session_state.chat_history:
    st.markdown(f'<div class="user-bubble">{USER_EMOJI} {entry["user"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-bubble">{BOT_EMOJI} {entry["bot"]}</div>', unsafe_allow_html=True)

col1, col2 = st.columns([8, 1])
with col1:
    user_input = st.text_input("Message Input", placeholder="Type your message here...", label_visibility="collapsed", key="input")
with col2:
    send_pressed = st.button("Send")

if user_input and send_pressed:
    with st.spinner("🔥 Generating roast..."):
        response = roast_message(user_input)
    st.session_state.chat_history.append({"user": user_input, "bot": response})
    st.rerun()
