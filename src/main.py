import os
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchResults
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler

load_dotenv()

# Get API key from Hugging Face Secrets
api_key = os.getenv("GROQ_API_KEY")

# Stop app if no key
if not api_key:
    st.error("🚨 Missing API key! Add GROQ_API_KEY in: Space → Settings → Variables")
    st.stop()

st.title("🔎 LangChain - Chat With Web Search")
"""
In this example, we are using 'streamlitcallbackhandler to display the thoughts and actions'.
Try more langchain streamlit Agent examples at [github.com/langchain-ai/streamlit-agent]
"""

# Tools
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=250)
wiki = WikipediaQueryRun(name="wikipedia", api_wrapper=api_wrapper)

api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=250)
arxiv = ArxivQueryRun(name="arxiv", api_wrapper=api_wrapper_arxiv)
search = DuckDuckGoSearchResults(name="search")

# Message log
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I can search the web. How may I help you?"}
    ]

# Display conversation history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    llm = ChatGroq(groq_api_key=api_key, model="llama-3.3-70b-versatile", streaming=True)
    tools = [search, arxiv, wiki]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        max_iterations=15,
        verbose=True
    )

    with st.chat_message("assistant"):
        cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = agent.invoke({"input": prompt}, callbacks=[cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response["output"])
        

