from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from streamlit_chat import message
from bs4 import BeautifulSoup
import requests
import streamlit as st
from urllib.parse import unquote
import numpy as np

def init():
  st.set_page_config(
    page_title='Skyward Chat Bot'
  )

  # Check for empty chat history
  if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content='Hello! Welcome to the chat! Do you have a question?')]

  if 'messages' not in st.session_state:
    st.session_state.messages = [
      SystemMessage(content='You are a helpful assistant'),
    ]

  st.header('My Perplexity-like clone')
  with st.sidebar:
    st.link_button(label='Home', url='http://localhost:8501/', use_container_width=True)

def get_response(user_query, chat_history):
  llm = ChatOllama(
    model = 'llama3.1',
    temperature=0.2,
  )

  # Making a template for opening the page
  template = """
    Chat history: {chat_history}
    User question: {user_question}
    """

  # Creating the user input prompt
  prompt = ChatPromptTemplate.from_template(template)

  # Making the chain to stream from to output to the page
  chain = prompt | llm |  StrOutputParser()

  response = requests.get(f'https://google.com/search?q={user_query}')
  soup = BeautifulSoup(response.text, 'html.parser')
  links = soup.find_all('a')

  urls = []
  videos = []
  for li in [link for link in links if link['href'].startswith('/url?q=')]:
    url = li['href']
    url = url.replace('/url?q=', '')
    url = unquote(url.split('&sa=')[0])

    # Removing google sources, pdfs, and anchors
    # fixing some search urls
    if '//search?q=' in url:
      url = url.replace('//search?q=', '')
    if '/search?q=' in url:
      url = url.replace('/search?q=', '')
    if 'google.com/' in url:
      continue
    if url.endswith('.pdf'):
      continue
    if '#' in url:
      url = url.split('#')[0]
    if 'youtube.com/' in url or 'youtu.be/' in url:
      videos.append(url)
    # malformed url, discard it
    if 'https://' not in url and 'http://' not in url:
     continue
    # add to urls list
    urls.append(url)

  # dedupe urls and videos after cleaning
  urls = list(np.unique(urls))[0:4]
  videos = list(np.unique(videos))[0:4]

  with st.container(height=300, border=True):
    st.text('Here are some helpful links:')
    for url in urls:
      st.link_button(label=url, url=url, use_container_width=True)
  with st.container(height=300, border=True):
    for video in videos:
      st.video(video)

  return chain.stream({
        'chat_history': chat_history,
        'user_question': user_query
      })

# Init streamlit resources
init()

messages = st.session_state.get('chat_history', [])
for i, msg in enumerate(messages):
  if i % 2 == 0:
    message(msg.content, is_user=True, key=str(i) + '_user')
  else:
    message(msg.content, is_user=False, key=str(i) + '_ai')

user_input = st.chat_input('Your message: ', key='user_input')

if user_input:
  st.session_state.chat_history.append(HumanMessage(content=user_input))

  with st.spinner('Generating response...'):
    response = st.write_stream(get_response(user_input, st.session_state.chat_history))
  st.session_state.chat_history.append(AIMessage(content=response))
