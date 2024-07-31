import streamlit as st
from utils import init, get_videos_and_urls

init('Discovery Page')
main = st.container()
urls, videos = get_videos_and_urls('Todays top stories', 10)
with main:
  top = st.container(height=800)
  with top:
    for url in urls:
      st.link_button(label=url, url=url, use_container_width=True)
