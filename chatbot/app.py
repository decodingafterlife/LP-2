import streamlit as st
from chatbot import Chatbot

st.set_page_config(page_title="E-commerce Support Chatbot", layout="centered")

st.title("🛍️ E-commerce Support Chatbot")
st.write("Ask me anything about your orders, returns, or payments!")

bot = Chatbot()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box for user query
user_input = st.text_input("You:", key="input")

# Handle input
if user_input:
    response = bot.get_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display chat history
for sender, msg in reversed(st.session_state.chat_history):
    if sender == "You":
        st.markdown(f"**🧑‍💻 {sender}:** {msg}")
    else:
        st.markdown(f"**🤖 {sender}:** {msg}")
