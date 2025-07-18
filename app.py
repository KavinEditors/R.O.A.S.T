import streamlit as st
import requests

# Set up OpenRouter API key
api_key = st.secrets["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-3.5-turbo"

# Page config
st.set_page_config(page_title="R.O.A.S.T.", page_icon="🔥")
st.title("🔥 R.O.A.S.T. (Really Offensive Automated Sus Terminator)")
st.markdown("Talk to the savage AI and get roasted 💀. Ask anything dumb or sus and feel the burn.")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Trigger words to detect creator question
creator_keywords = ["who made", "who created", "who developed", "your creator", "who built", "who coded"]

# Roast generation function
def roast_message(user_msg):
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

# Display chat above input
for entry in st.session_state.chat_history:
    st.markdown(f"**🧍 You:** {entry['user']}")
    st.markdown(f"**🤖 R.O.A.S.T. Bot:** {entry['bot']}")
    st.markdown("---")

# User input
user_input = st.text_input("Type your message:", placeholder="Say something dumb...")

# Submit button
if st.button("Send") and user_input:
    with st.spinner("🔥 Generating roast..."):
        reply = roast_message(user_input)
        st.session_state.chat_history.append({"user": user_input, "bot": reply})
        st.experimental_set_query_params(dummy_reload=st.session_state.get("reload", 0) + 1)  # quick dummy refresh
        st.session_state.reload = st.session_state.get("reload", 0) + 1
