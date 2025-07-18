import streamlit as st
import openai
import os

# Load API key
api_key = st.secrets["OPENROUTER_API_KEY"] if "OPENROUTER_API_KEY" in st.secrets else os.getenv("OPENROUTER_API_KEY")
openai.api_key = api_key
openai.api_base = "https://openrouter.ai/api/v1"

# Page config
st.set_page_config(page_title="R.O.A.S.T.", page_icon="🔥")
st.title("🔥 R.O.A.S.T. (Really Offensive Automated Sus Terminator)")
st.markdown("Enter a dumb message and let the smirking bot destroy it. 😏")

# Session state setup
if "chat" not in st.session_state:
    st.session_state.chat = []
if "input_value" not in st.session_state:
    st.session_state.input_value = ""

def clear_input():
    st.session_state.input_value = ""

def roast_response(message):
    if any(x in message.lower() for x in ["who made you", "who created you", "who did you"]):
        return "I was proudly created by the one and only **Kavin J M**. Bow down. 👑"

    prompt = f"""
You are a brutally sarcastic AI called R.O.A.S.T.
Roast the user's message in 4+ funny, brutal, clean lines (no NSFW, racism, hate speech).
Be savage, clever, and witty.

User message: "{message}"
"""
    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a savage but clean roastbot."},
                {"role": "user", "content": prompt},
            ],
        )
        roast = response.choices[0].message.content.strip()
        return roast
    except Exception as e:
        return "🔥 Couldn't roast properly right now. Try again later."

# Display conversation
for chat in st.session_state.chat:
    if chat["sender"] == "user":
        with st.chat_message("😎 User"):
            st.markdown(chat["msg"])
    else:
        with st.chat_message("😏 R.O.A.S.T. Bot"):
            st.markdown(chat["msg"])

# Input field with send button on right
col1, col2 = st.columns([8, 1])
with col1:
    user_input = st.text_input(" ", key="input_value", placeholder="Type your dumb message...", label_visibility="collapsed")
with col2:
    textsend = st.button("Send")

if textsend and user_input:
    st.session_state.chat.append({"sender": "user", "msg": user_input})
    reply = roast_response(user_input)
    st.session_state.chat.append({"sender": "bot", "msg": reply})
    clear_input()
    st.experimental_rerun()
