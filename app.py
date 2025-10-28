import streamlit as st
import requests
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="R.O.A.S.T", page_icon="🔥", layout="wide")
st.markdown("<h1 style='text-align:center;'>🔥 R.O.A.S.T.</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Really Offensive Automated Sus Terminator 💀</p>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "username" not in st.session_state:
    st.session_state.username = ""
if "mood" not in st.session_state:
    st.session_state.mood = "Savage"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

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

left, center, right = st.columns([2, 5, 2])

with right:
    if st.button("🌃 Dark Mode"):
        st.session_state.theme = "dark"
    if st.button("🌇 Light Mode"):
        st.session_state.theme = "light"

with left:
    st.markdown("### 😎 Name")
    name = st.text_input("Enter your name", value=st.session_state.username)
    if name.strip():
        st.session_state.username = name.strip()
    else:
        st.session_state.username = "user"
    st.markdown("---")
    show_mood_chart()

def roast_message(user_msg):
    user = st.session_state.username.lower().strip()
    triggers = [
        "who made you", "who created you", "your creator", "who is your owner",
        "who owns you", "who designed you", "who built you", "who programmed you",
        "who developed you", "who invented you", "your owner", "who coded you"
    ]
    if any(phrase in user_msg.lower() for phrase in triggers):
        return f"I was forged in the fiery brain of <b>Kavin J M</b> — the ultimate roastmaster 🔥"
    
    special_terms = ["kavin", "kavin j m", "kavinjm"]
    if user_msg.lower().strip() in special_terms:
        return "😤 You can't roast the roastmaster. He's immune to petty burns. 🔥🧠"

    if not api_key:
        return "⚠️ Missing GROQ_API_KEY. Please add it in your Streamlit secrets."

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
    messages = [m for m in messages if m.get("content")]

    try:
        #  Correct and verified Groq API endpoint
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "temperature": 0.8
        }

        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        data = res.json()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        else:
            return "🤖 No roast generated. Groq returned an empty response."

    except requests.exceptions.HTTPError as e:
        return f"💥 API Error: {res.text}"
    except Exception as e:
        return f"⚠️ Unexpected Error: {str(e)}"

def message_align(msg, sender="user"):
    align = "flex-end" if sender == "user" else "flex-start"
    emoji = "😎" if sender == "user" else "😏"
    if st.session_state.theme == "dark":
        border_color = "white"
        text_color = "white"
    else:
        border_color = "black"
        text_color = "black"

    st.markdown(f"""
        <div style='display: flex; justify-content: {align}; margin: 10px 0;'>
            <div style='border: 1.5px solid {border_color}; background-color: transparent;
                        padding: 10px 15px; border-radius: 15px; max-width: 75%;
                        font-size: 16px; color: {text_color};'>
                <span><b>{emoji}</b> {msg}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

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
        
