import os
from unittest.mock import call
from urllib import response
from huggingface_hub import Agent
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchResults
from langchain.agents import initialize_agent,AgentType
from langchain.callbacks import StreamlitCallbackHandler

from dotenv import load_dotenv
load_dotenv()

# Get API key from HF Secrets
api_key = os.getenv("GROQ_API_KEY")

# Ensure API key exists
if not api_key:
    st.error("🚨 Missing API key! Set GROQ_API_KEY in Hugging Face → Settings → Variables.")
    st.stop()

#used the inbuild tools of wikipedia,arxiv tools
api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=250)
wiki=WikipediaQueryRun(api_wrapper=api_wrapper)

api_wrapper_arxiv=ArxivAPIWrapper(top_k_result=1,doc_content_chars_max=250)
arxiv=ArxivQueryRun(api_wrapper_arxiv=api_wrapper_arxiv)

search=DuckDuckGoSearchResults(name='Search')

st.title("Langchain- Chat with search")
"""
In this example, we are using 'streamlitcallbackhandler to display the thoughts and actions'.
Try more langchain streamlit Agent examples at [github.com/langchain-ai/streamlit-agent]
"""
#sidebar for setting
st.sidebar.title("Setting")
api_key=st.sidebar.text_input("Enter your Groq API key:",type="password")

if "message" not in st.session_state:
    st.session_state["message"]=[
        {"role":"assisstant","content":"hii ,i am a chat bot which can search web.how can i help you"}
    ]

for msg in st.session_state.message:
    st.chat_message(msg['role']).write(msg['content'])

if prompt:=st.chat_input(placeholder="what is machine learing ?"):
    st.session_state.message.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

    llm=ChatGroq(groq_api_key=api_key,model="llama-3.3-70b-versatile",streaming=True)
    tools=[search,arxiv,wiki]

    search_agent=initialize_agent(tools,llm,agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)

    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        responses = search_agent.invoke({"input": st.session_state.message}, callbacks=[st_cb])
        st.session_state.message.append({'role':'assistant','content':responses})
        st.write(responses["output"])

