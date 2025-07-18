import streamlit as st
import requests

# Config
st.set_page_config(page_title="R.O.A.S.T.", page_icon="🔥")
st.title("🔥 R.O.A.S.T. (Really Offensive Automated Sus Terminator)")
st.markdown("Talk to the savage AI and get roasted 💀. Ask anything dumb or sus and feel the burn.")

# API setup
api_key = st.secrets["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-3.5-turbo"

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

creator_keywords = ["who made", "who created", "who developed", "your creator", "who built", "who coded"]

# Roast generation
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

    for _ in range(3):  # Try 3 times to get 4+ lines
        try:
            res = requests.post(API_URL, headers=headers, json={
                "model": MODEL,
                "messages": base_messages
            })
            res.raise_for_status()
            reply = res.json()["choices"][0]["message"]["content"].strip()
            if len(reply.splitlines()) >= 4:
                return reply
        except Exception as e:
            return f"💥 Error: {str(e)}"

    return "🔥 Couldn't roast properly right now. Try again later."

# Display chat history
for entry in st.session_state.chat_history:
    st.markdown(f"**😎 You:** {entry['user']}")
    st.markdown(f"**😏 R.O.A.S.T. Bot:** {entry['bot']}")
    st.markdown("---")

# Chat input layout (input + button inline)
col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input("Type your message:", key="user_input", label_visibility="collapsed", placeholder="Say something dumb...")
with col2:
    send_clicked = st.button("Send")

# On send
if send_clicked and user_input.strip():
    with st.spinner("🔥 Roasting you..."):
        reply = roast_message(user_input)
        st.session_state.chat_history.append({"user": user_input, "bot": reply})
        st.query_params.update(dummy_reload=str(len(st.session_state.chat_history)))
