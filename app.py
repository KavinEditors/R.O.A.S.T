import streamlit as st
import requests
import os
import matplotlib.pyplot as plt
import random

api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="R.O.A.S.T.🔥", page_icon="🔥")

# Username input at the very top
username = st.text_input("Enter your name", key="username_input").strip() or "User"

st.markdown(f"<h1 style='text-align:center;'>🔥 R.O.A.S.T.</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>Really Offensive Automated Sus Terminator 💀</p>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def roast_message(user_msg):
    if any(x in user_msg.lower() for x in ["who made you", "who created you", "your creator"]):
        return f"I was forged in the fiery brain of <b>Kavin J M</b> — the ultimate roastmaster 🔥"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    messages = [{"role": "system", "content": "Roast all messages with dark humor, wit, sarcasm. No mercy."}]
    for chat in st.session_state.chat_history:
        messages.append({"role": "user", "content": chat["user"]})
        messages.append({"role": "assistant", "content": chat["bot"]})
    messages.append({"role": "user", "content": user_msg})
    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json={"model": "llama3-8b-8192", "messages": messages}
        )
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"😏 💥 Error: {str(e)}"

def message_align(msg, sender="user"):
    align = "right" if sender == "user" else "left"
    emoji = "😎" if sender == "user" else "😏"
    html = f"<div style='text-align:{align}; background-color:#f0f0f0; padding:10px; border-radius:10px; margin:8px 0; max-width:70%; display:inline-block;'><b>{emoji} {username if sender=='user' else 'R.O.A.S.T.'}</b><br>{msg}</div>"
    st.markdown(html, unsafe_allow_html=True)

# Show chat history
for chat in st.session_state.chat_history:
    message_align(chat["user"], "user")
    message_align(chat["bot"], "bot")

# Input
col1, col2 = st.columns([8, 1])
with col1:
    user_input = st.text_input(" ", placeholder="Type your message...", label_visibility="collapsed", key="input")
with col2:
    send = st.button("Send")

if user_input and send:
    with st.spinner("🔥 Cooking up a roast..."):
        response = roast_message(user_input)
    st.session_state.chat_history.append({"user": user_input, "bot": response})
    st.rerun()

# Random mood bar chart
st.markdown("---")
st.markdown("### 🤖 Bot Mood")
labels = ["SUS", "Savage", "Dark Humour"]
values = [random.randint(10, 100) for _ in labels]
colors = ["#F39C12", "#E74C3C", "#8E44AD"]

fig, ax = plt.subplots()
ax.bar(labels, values, color=colors)
ax.set_ylim(0, 100)
ax.set_ylabel("Intensity")
st.pyplot(fig)
