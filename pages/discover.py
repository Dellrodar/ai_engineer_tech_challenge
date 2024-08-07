import streamlit as st
from utils import init, get_videos_and_urls
import os

init('Discovery Page')
main = st.container()
discovery_result_limit = os.environ.get('DISCOVERY_RESULT_LIMIT', 10)
urls, videos = get_videos_and_urls('Todays top stories', discovery_result_limit)
with main:
  top = st.container(height=800)
  with top:
    for url in urls:
      st.link_button(label=url, url=url, use_container_width=True)
