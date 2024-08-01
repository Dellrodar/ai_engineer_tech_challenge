from langchain_core.messages import AIMessage, HumanMessage
from streamlit_chat import message
import streamlit as st
from utils import init, get_response

init('Skyward Chat Bot')
# Check for empty chat history
if "chat_history" not in st.session_state:
  st.session_state.chat_history = [AIMessage(content='Hello! Welcome to the chat! Do you have a question?')]

st.header('My Perplexity-like clone')

messages = st.session_state.get('chat_history', [])
for i, msg in enumerate(messages):
  if i % 2 != 0:
    message(msg.content, is_user=True, key=str(i) + '_user')
  else:
    message(msg.content, is_user=False, key=str(i) + '_ai')

user_input = st.chat_input('Your message: ', key='user_input')

if user_input:
  st.session_state.chat_history.append(HumanMessage(content=user_input))

  with st.spinner('Generating response...'):
    response = st.write_stream(get_response(user_input, st.session_state.chat_history))
  st.session_state.chat_history.append(AIMessage(content=response))
