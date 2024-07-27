from langchain.chat_models import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import streamlit as st
import time
 
 
# 1. Utility functions
 
def initialize_chat_chain():
    """
    Creates a new chat chain with memory
    """
    # Ollama should be up and running on your local system
    # print("\033[H\033[J")
    # print("Please enter the model that you want to use for the chatbot.")
    # print("You can choose from the following models (in descending order of response time and ascending order of power):")
    # print("1. gemma:2b\n2. phi3\n3. llama3")
    # global modelChoice
    # modelChoice = input("Enter the model name: ")
    # if(modelChoice not in ['gemma:2b', 'phi3', 'llama3']):
    #     print("Invalid model name. Defaulting to gemma:2b")
    #     modelChoice = "gemma:2b"
    modelChoice = "phi3"
    chat = ChatOllama(
        model=modelChoice,  # change the model as per your requirements
        streaming=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        temperature=0.7  # Tweak the value to find what works best for your requirements
    )
 
    chat_chain = ConversationChain(
        llm=chat,
        memory=ConversationBufferMemory(),  # change the memory type as per your requirements
    )
 
    return chat_chain
 
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
                   page_icon=":robot_face:")  # more icons at https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
 
# Personality and objective of your assistant
modelChoice = "phi3"
persona = "You are a helpful assistant. Your role is to provide information, answer questions, and engage in productive conversations."
 
 
# Initialize the chat chain
if "chat_chain" not in st.session_state:
    st.session_state["chat_chain"] = initialize_chat_chain()
ai_welcome_message = f"Hello! I'm your local chatbot assistant with the model: {modelChoice}. How can I help you today?"
 
# Set page title
st.title("Chat with your Awesome Local Bot")
 
# Sidebar with a button to start a new chat
with st.sidebar:
    st.subheader("Settings")
    st.write("Create a new chat if you want to clear the history and restart the conversation.")
 
    # For a new conversation, initialize the chat chain and conversation history
    if st.button("New chat"):
        st.session_state["chat_chain"] = initialize_chat_chain()
        st.session_state["conversation_history"] = [SystemMessage(content=persona),
                                                    AIMessage(content=ai_welcome_message)]
        st.success("New chat created!")
 
# Initialize the conversation history (for the GUI)
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = [SystemMessage(content=persona), AIMessage(content=ai_welcome_message)]
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
            response = st.session_state.chat_chain.predict(input=user_input)
            # get the response stream and display it to the user with the typewriter effect
            response_stream = generate_response_stream(response)
            placeholder = st.empty()
            placeholder.write_stream(response_stream)
            # Remove the "ugly" stream from the UI and pretty print the response with Markdown formatting
            placeholder.empty()
            st.markdown(response)
            # Add the chatbot response to the history
            st.session_state.conversation_history.append(AIMessage(content=response))