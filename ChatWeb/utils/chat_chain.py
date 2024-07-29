#utils/chat_chain.py

from . import ChatOllama, ConversationChain, ConversationBufferMemory, CallbackManager, StreamingStdOutCallbackHandler, OllamaEndpointNotFoundError

def initialize_chat_chain(model_choice):
    """
    Creates a new chat chain with memory.
    Args:
        model_choice (str): The model to be used for the chat chain.
    Returns:
        ConversationChain, str: The chat chain object and an error message if any.
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
    except OllamaEndpointNotFoundError:
        # Specific handling for model not found
        return None, f"Model '{model_choice}' not found. Please pull the model using the command\n `ollama pull {model_choice}`\n"
    except Exception as e:
        # General error handling
        return None, str(e)

