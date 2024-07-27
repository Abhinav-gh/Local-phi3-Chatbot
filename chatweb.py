from langchain.chat_models import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms.ollama import OllamaEndpointNotFoundError
import streamlit as st
import time

# 1. Utility functions

def initialize_chat_chain(model_choice):
    """
    Creates a new chat chain with memory
    """
    try:
        chat = ChatOllama(
            model=model_choice,
            streaming=True,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature=0.7
        )
        chat_chain = ConversationChain(
            llm=chat,
            memory=ConversationBufferMemory(),
        )
        return chat_chain, None
    except OllamaEndpointNotFoundError as e:
        # Specific handling for model not found
        return None, f"Model '{model_choice}' not found. Please pull the model using the command\n `ollama pull {model_choice}`\n"
    except Exception as e:
        # General error handling
        return None, str(e)

def generate_response_stream(response):
    """
    Streams a given chatbot response token by token
    """
    response_tokens = response.split()
    for token in response_tokens:
        yield token + ' '
        time.sleep(0.025)  # Adjust the delay between tokens to control the speed of the typewriter effect

# 2. Main program

st.set_page_config(page_title="My Local Chatbot",
                   page_icon=":robot_face:")

# Personality and objective of your assistant
default_model_choice = "phi3"
persona = "You are a helpful assistant. Your role is to provide information, answer questions, and engage in productive conversations."

# Input for model choice
model_choice = st.text_input("Enter the model name \t(e.g. ' phi3 '  ,  ' llama3 '  ,  ' gemma '):", value=default_model_choice)

# Initialize the chat chain if it is not present or model choice has changed
if "chat_chain" not in st.session_state or st.session_state.get("model_choice") != model_choice:
    chat_chain, error = initialize_chat_chain(model_choice)
    if error:
        st.error(error)
        chat_chain, error = initialize_chat_chain(default_model_choice)
        if error:
            st.error(f"Error initializing default model '{default_model_choice}': {error}")
            st.stop()  # Stop execution if both models fail
    st.session_state["chat_chain"] = chat_chain
    st.session_state["model_choice"] = model_choice
    st.session_state["conversation_history"] = [SystemMessage(content=persona),
                                                AIMessage(content=f"Hello! I'm your local chatbot assistant. I am currently using model: **{model_choice}**. How can I help you today?")]

# Sidebar with a button to start a new chat
with st.sidebar:
    st.subheader("Settings")
    st.write("Create a new chat if you want to clear the history and restart the conversation.")

    # For a new conversation, initialize the chat chain and conversation history
    if st.button("New chat"):
        chat_chain, error = initialize_chat_chain(model_choice)
        if error:
            st.error(error)
            chat_chain, error = initialize_chat_chain(default_model_choice)
            if error:
                st.error(f"Error initializing default model '{default_model_choice}': {error}")
                st.stop()  # Stop execution if both models fail
        st.session_state["chat_chain"] = chat_chain
        st.session_state["conversation_history"] = [SystemMessage(content=persona),
                                                    AIMessage(content=f"Hello! I'm your local chatbot assistant with the model: {model_choice}. How can I help you today?")]
        st.success("New chat created!")

# Initialize the conversation history (for the GUI)
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = [SystemMessage(content=persona),
                                                AIMessage(content=f"Hello! I'm your local chatbot assistant with the model: {model_choice}. How can I help you today?")]
conversation_history = st.session_state["conversation_history"]

# Display conversation history in the page
for message in st.session_state.conversation_history:
    if isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)

user_input = st.chat_input("Type your message here...")
if user_input:    
    # Add the user input in the history
    st.session_state.conversation_history.append(HumanMessage(content=user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            # Call the language model in the chat chain to generate a response from the user input
            try:
                response = st.session_state.chat_chain.predict(input=user_input)
                # Get the response stream and display it to the user with the typewriter effect
                response_stream = generate_response_stream(response)
                placeholder = st.empty()
                placeholder.write_stream(response_stream)
                # Remove the "ugly" stream from the UI and pretty print the response with Markdown formatting
                placeholder.empty()
                st.markdown(response)
                # Add the chatbot response to the history
                st.session_state.conversation_history.append(AIMessage(content=response))
            except OllamaEndpointNotFoundError as e:
                st.error(f"Model error: {e}. Switching to default model: {default_model_choice}.")
                chat_chain, error = initialize_chat_chain(default_model_choice)
                if error:
                    st.error(f"Error initializing default model '{default_model_choice}': {error}")
                else:
                    st.session_state["chat_chain"] = chat_chain
                    # Retry user input
                    response = st.session_state.chat_chain.predict(input=user_input)
                    response_stream = generate_response_stream(response)
                    placeholder = st.empty()
                    placeholder.write_stream(response_stream)
                    placeholder.empty()
                    st.markdown(response)
                    st.session_state.conversation_history.append(AIMessage(content=response))
