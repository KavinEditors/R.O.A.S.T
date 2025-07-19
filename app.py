import streamlit as st
import requests
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Get API Key securely
api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")

# Page Setup
st.set_page_config(page_title="R.O.A.S.T.🔥", page_icon="🔥", layout="wide")
st.markdown("<h1 style='text-align:center;'>🔥 R.O.A.S.T.</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Really Offensive Automated Sus Terminator 💀</p>", unsafe_allow_html=True)

# Session States
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "username" not in st.session_state:
    st.session_state.username = ""

if "mood" not in st.session_state:
    st.session_state.mood = "Savage"

# Mood Colors
mood_colors = {
    "SUS": "orange",
    "Savage": "red",
    "Dark Humour": "purple",
    "Wholesome": "green"
}

# Mood Bar Chart
def show_mood_chart():
    st.markdown("### 😎 Roast Bot Mood")
    mood_labels = ["Savage 🔥", "SUS 🕵️", "Dark Humour 🖤", "Wholesome 😊"]
    raw = np.random.rand(4)
    percentages = (raw / raw.sum() * 100).round().astype(int)
    mood_df = pd.DataFrame({
        "Mood": mood_labels,
        "Percentage": percentages
    })
    st.bar_chart(mood_df.set_index("Mood"), use_container_width=True)

# Sidebar
left, center, right = st.columns([2, 5, 2])

with left:
    st.markdown("### 😎 Name")
    name = st.text_input("Enter your name", value=st.session_state.username)
    st.session_state.username = name.strip() or "user"

    st.markdown("---")
    st.markdown("### 📊 Bot Mood")
    mood = st.session_state.mood
    color = mood_colors[mood]
    fig, ax = plt.subplots(figsize=(3.5, 1.5))
    ax.barh([mood], [100], color=color)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Mood Intensity (%)")
    ax.set_yticks([])
    ax.set_title(mood)
    st.pyplot(fig)

    show_mood_chart()

# Roast Message Generator
def roast_message(user_msg):
    if any(x in user_msg.lower() for x in ["who made you", "who created you", "your creator"]):
        return f"I was forged in the fiery brain of <b>Kavin J M</b> — the ultimate roastmaster 🔥"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    persona = f"Roast {st.session_state.username} with hard roast. In 2 lines. Roast every single msg like hi, how are u. No mercy. Push to peak of stress. If name given, roast the name too."
    messages = [{"role": "system", "content": persona}]
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

# Message Renderer
def message_align(msg, sender="user"):
    align = "right" if sender == "user" else "left"
    emoji = "😎" if sender == "user" else "😏"
    html = f"<div style='text-align:{align}; margin:8px 0;'><b>{emoji}</b> {msg}</div>"
    st.markdown(html, unsafe_allow_html=True)

# Main Chat UI
with center:
    for chat in st.session_state.chat_history:
        message_align(chat["user"], "user")
        message_align(chat["bot"], "bot")

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
