# Env variables
| name | type | example |
| --- | --- | --- |
| 'OLLAMA_URL' | string | 'http://ollama-container' |
| 'OLLAMA_PORT' | number | 11434 |
| 'MODEL' | 'string' | 'llama3.1' |
| 'TEMPERATURE' | float | 0.2 |
| 'SEARCH_URL' | string | 'http://www.google.com' |
| 'VIDEO_URL_RESULT_LIMIT' | number | 4 |
| 'DISCOVERY_RESULT_LIMIT' | number | 10 |

## Process
This task was to create a production ready replica of [Perplexity.ai](https://www.perplexity.ai/). The first thing I wanted to plan for is what features I could replicate at a glance. I identified five features and they are as follows: The sidebar, the discovery page, the chat function on the main page, suggested urls based on the return, and suggested videos based on the return.

This first thing I focused on was the chat capability. I started by choosing my model(llama 3.1) and a framework to run the model(Ollama) and Langchain. From there, I started with streamlit for the front end, creating the container and user input for the LLM prompt. I connected the LLM via an Langchain Ollama connector with my local ollama container as the host. My inital stream gave a response, but did not remember the history of the chat.

The next task involved getting ollama to remember this chat history. I created a prompt template using langchain's ChatPromptTemplate. This template was as follows:

```
template = """
    You are a helpful assistant.
    Answer the following questions considering the history of the conversation:
    Chat history: {chat_history}
    User question: {user_query}
    """
```

This template includes the current user question, the previous chat history, and two static prompts. The result of this stream is then returned to the user on the screen. For sample in put on this, I introduce myself and a prompt of, "Hello, my name is Emilio". I then continued on with different prompts about fishing, cars, and various hobbies. I then prompted, "Can you remember what my name is?" and it gave the output of my name, meaning the test was a success and it was now reading history.

Once the chat was complete, I worked getting urls and videos based on the user search. for this, I sent a request to google with the users prompt as the search query and returned the results. I took those results and parsed all of the urls from the html returned using BeautifulSoup.

From this list of links, I wanted to filter and separate links from specific sites like google and remove them. I also wanted to remove pdf files and links with anchors. And finally, I wanted to separate links that contained videos. I used popular video sharing sites like youtube and tik tok to separate the videos from the urls and added them to a separate list. I returned both lists of separated links and videos and returned them, where the top four(controlled by VIDEO_URL_RESULT_LIMIT env variable) will be returned in a container with the stream.

Next I worked on the sidebar and discovery page. I started by creating a sidebar on the main page. then adding some simple links. The first one is to google's search page. Seeing that this worked and not wanting to duplicate this in the discovery page, I moved this sidebar init function to a utility. Also not wanting to duplicate the search logic for the discovery page, I moved that into a utility function as well.In case I would want to use the chatbot in other parts of this replica, I moved the get_response function to a utility as well.

Starting on discovery page I had it do one thing and that is return links of todays top stories using the get_video_and_urls function I made previously.

Trying to make this more configurable was a little bit of a challenge. I wanted to take into effect those who may or may not have internet access, as well as those whose infrastructures only run local hosting. I created environmental variables that can be fed into this program. I have the option of running it locally via a dockerized container with an ollama server, or running it independently and having a hosted ollama server elsewhere.

To handle scaling for this, we can host an ollama server via AWS and have an EFS with all downloaded models attached to /root/.ollama. This ensure that the ollama server can be scaled to meet the needs of multiple users and needs of quick scaling.
This also gives expanded flexibility to use any llama models moving forward.
