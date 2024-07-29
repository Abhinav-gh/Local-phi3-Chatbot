try:
    from langchain.chat_models import ChatOllama
    from langchain.chains import ConversationChain
    from langchain.memory import ConversationBufferMemory
    from langchain.schema import AIMessage, HumanMessage, SystemMessage
    from langchain.callbacks.manager import CallbackManager
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
    from langchain_community.llms.ollama import OllamaEndpointNotFoundError
    import streamlit as st
except ImportError as e:
    # Capture any import errors and display them in the web app
    missing_module = str(e).split(" ")[-1]
    raise ImportError(f"Missing module: {missing_module}. Please ensure all required packages are installed.")

__all__ = [
    "ChatOllama",
    "ConversationChain",
    "ConversationBufferMemory",
    "AIMessage",
    "HumanMessage",
    "SystemMessage",
    "CallbackManager",
    "StreamingStdOutCallbackHandler",
    "OllamaEndpointNotFoundError",
    "st"
]
# Importing utility functions
from .chat_chain import initialize_chat_chain
from .response import generate_response_stream
