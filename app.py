import streamlit as st
import requests

# Set up OpenRouter API
api_key = st.secrets["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-3.5-turbo"

# Page Config
st.set_page_config(page_title="R.O.A.S.T.", page_icon="🔥")
st.title("🔥 R.O.A.S.T. (Really Offensive Automated Sus Terminator)")
st.markdown("Talk to the savage AI and get roasted 💀. Ask anything dumb or sus and feel the burn.")

# Session state to track conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Keywords that trigger creator identity
creator_keywords = ["who made", "who created", "who developed", "your creator", "who built", "who coded"]

# Roast Function
def roast_message(user_msg):
    # Check if the message is about creator
    if any(key in user_msg.lower() for key in creator_keywords):
        return "I was forged in the fiery brain of **Kavin J M** — the ultimate roastmaster 🔥😈"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": "You are a savage roastbot. Roast every user message with brutal sarcasm, but keep it clean (no NSFW)."}]
    for entry in st.session_state.chat_history:
        messages.append({"role": "user", "content": entry["user"]})
        messages.append({"role": "assistant", "content": entry["bot"]})
    messages.append({"role": "user", "content": user_msg})

    try:
        res = requests.post(API_URL, headers=headers, json={
            "model": MODEL,
            "messages": messages
        })
        res.raise_for_status()
        reply = res.json()["choices"][0]["message"]["content"].strip()
        return reply
    except Exception as e:
        return f"💥 Error: {str(e)}"

# --- Show Chat Above Input ---
for entry in st.session_state.chat_history:
    st.markdown(f"** 😎 You:** {entry['user']}")
    st.markdown(f"**😏 R.O.A.S.T. Bot:** {entry['bot']}")
    st.markdown("---")

# --- Input Form ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", placeholder="Type something dumb to get roasted...")
    submitted = st.form_submit_button("Send")

# --- Process Input ---
if submitted and user_input:
    with st.spinner("🔥 Generating roast..."):
        bot_reply = roast_message(user_input)
        st.session_state.chat_history.append({
            "user": user_input,
            "bot": bot_reply
        })
    st.experimental_rerun()
