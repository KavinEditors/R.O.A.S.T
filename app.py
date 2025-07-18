import streamlit as st
import os
import google.generativeai as genai

# Load Gemini API key securely
api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)

# Load model
model = genai.GenerativeModel("gemini-pro")

# Streamlit config
st.set_page_config(page_title="R.O.A.S.T.", page_icon="🔥")
st.title("🔥 R.O.A.S.T. (Really Offensive Automated Sus Terminator)")

st.markdown("Enter a message and let the bot burn it down brutally... 😈")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Check if the message is about creator
def is_creator_question(msg):
    triggers = ["who made", "who created", "your creator", "who did you", "developer"]
    return any(trigger in msg.lower() for trigger in triggers)

# Generate roast using Gemini
def get_roast(message):
    prompt = f"""
Roast this message brutally also NFSW. Be sarcastic, savage, and funny. 
Minimum 4 lines. Make it feel like a verbal burn. Message: "{message}"
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "😏 R.O.A.S.T. Bot: 🔥 Couldn't roast properly right now. Try again later."

# Display chat history
for entry in st.session_state.chat:
    if entry["sender"] == "user":
        st.markdown(f"😎 You: {entry['msg']}")
    else:
        st.markdown(f"😏 R.O.A.S.T. Bot: {entry['msg']}")

# Chat input with send button
col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input(" ", key="input", placeholder="Type your message here...", label_visibility="collapsed")
with col2:
    send = st.button("➡️")

# When message is sent
if send and user_input:
    st.session_state.chat.append({"sender": "user", "msg": user_input})

    # Creator response
    if is_creator_question(user_input):
        reply = "I was forged in the digital fires by **Kavin J M**, the ultimate brain behind my roasts. 🔥"
    else:
        reply = get_roast(user_input)

    st.session_state.chat.append({"sender": "bot", "msg": reply})
    st.experimental_rerun()
