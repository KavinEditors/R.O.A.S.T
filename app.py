import streamlit as st
import requests

BOT_EMOJI = "😏"
USER_EMOJI = "😎"

MODEL = "mixtral-8x7b-32768"
API_URL = "https://api.groq.com/openai/v1/chat/completions"
api_key = st.secrets["GROQ_API_KEY"]

creator_keywords = ["who made you", "who created you", "your creator", "who did you"]

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
    messages = [{"role": "system", "content": "You are a savage roastbot. Roast every user message with brutal sarcasm, wit, and humor. use NSFW"}]
    for entry in st.session_state.chat_history:
        messages.append({"role": "user", "content": entry["user"]})
        messages.append({"role": "assistant", "content": entry["bot"]})
    messages.append({"role": "user", "content": user_msg})
    response = requests.post(API_URL, headers=headers, json={
        "model": MODEL,
        "messages": messages
    })
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()

for entry in st.session_state.chat_history:
    with st.container():
        col1, col2 = st.columns([7, 5])
        with col1:
            st.markdown(f'<div style="background-color:#e0e0e0; padding:10px; border-radius:10px; text-align:left">{BOT_EMOJI} <b>ROAST:</b> {entry["bot"]}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="background-color:#d9d9d9; padding:10px; border-radius:10px; text-align:right">{USER_EMOJI} <b>You:</b> {entry["user"]}</div>', unsafe_allow_html=True)

col1, col2 = st.columns([8, 1])
with col1:
    user_input = st.text_input("", placeholder="Type your message here...", label_visibility="collapsed", key="input")
with col2:
    send_pressed = st.button("Send")

if user_input and send_pressed:
    with st.spinner("🔥 Generating roast..."):
        response = roast_message(user_input)
    st.session_state.chat_history.append({"user": user_input, "bot": response})
    st.session_state.input = ""
    st.rerun()
