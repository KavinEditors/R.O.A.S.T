import streamlit as st
import requests
import os

# Set page config
st.set_page_config(page_title="R.O.A.S.T.", page_icon="🔥")

# Title and subtitle
st.title("🔥 R.O.A.S.T. (Really Offensive Automated Sus Terminator)")
st.markdown("Let the AI roast your message like a pro. Enter anything dumb or sus below...")

# Load API key securely
api_key = st.secrets["OPENROUTER_API_KEY"] if "OPENROUTER_API_KEY" in st.secrets else os.getenv("OPENROUTER_API_KEY")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Detect if user is asking about the bot's creator
def is_creator_question(msg):
    msg = msg.lower()
    return any(q in msg for q in ["who made you", "who created you", "who built you", "your creator", "who did you"])

# Function to get roast reply from OpenRouter
def get_roast(user_msg):
    prompt = f"""
Roast the following message with brutal wit and sarcasm. Be hilarious and clever — make the roast at least 4 lines long. Keep it clean (no NSFW or hate speech).

Message: "{user_msg}"
"""
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral/mistral-7b-instruct",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 1
            }
        )

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "😏 R.O.A.S.T. Bot: 🔥 Couldn't roast properly right now. Try again later."

# Display chat history
for msg in st.session_state.chat:
    if msg["sender"] == "user":
        st.markdown(f"😎 **You:** {msg['msg']}")
    else:
        st.markdown(f"😏 **R.O.A.S.T. Bot:** {msg['msg']}")

# Input box and send button
col1, col2 = st.columns([8, 1])
with col1:
    user_input = st.text_input(" ", key="input", placeholder="Type your dumb message...", label_visibility="collapsed")
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
    st.session_state.input = ""  # clear input
