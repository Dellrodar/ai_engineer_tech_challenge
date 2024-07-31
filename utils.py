from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_community.llms import Llama
from langchain_ollama import ChatOllama
from bs4 import BeautifulSoup
from urllib.parse import unquote
import requests
import streamlit as st
import numpy as np

def init(title):
  st.logo('https://skywarditsolutions.com/skyward/wp-content/themes/skyward/assets/img/skyward-logo.svg', link='https://skywarditsolutions.com/')
  st.set_page_config(
    page_title=title,
  )

  st.sidebar.page_link("http://www.google.com", label="Google", icon="🌎")

def get_videos_and_urls(user_query, limit):
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
    if 'tiktok.com/' in url:
      videos.append(url)
    # malformed url, discard it
    if 'https://' not in url and 'http://' not in url:
     continue
    # add to urls list
    urls.append(url)

  # dedupe urls and videos after cleaning
  if limit is not None:
    urls = list(np.unique(urls))[0:limit]
    videos = list(np.unique(videos))[0:limit]
  else:
    urls = list(np.unique(urls))[0:5]
    videos = list(np.unique(videos))[0:5]

  return [
    urls,
    videos,
  ]

def get_response(user_query, chat_history):
  llm = ChatOllama(
    model = 'llama3.1',
    temperature=0.2,
    # base_url='http://host.docker.internal:11434'
    base_url='http://localhost:11434'
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

  urls, videos = get_videos_and_urls(user_query, 4)

  with st.container(height=300, border=True):
    st.text('Here are some helpful links:')
    for url in urls:
      st.link_button(label=url, url=url, use_container_width=True)
  if videos:
    with st.container(height=300, border=True):
      for video in videos:
        st.video(video)

  return chain.stream({
        'chat_history': chat_history,
        'user_question': user_query
      })
