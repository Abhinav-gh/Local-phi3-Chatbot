# utils/response.py

import time

def generate_response_stream(response):
    """
    Streams a given chatbot response token by token.
    Args:
        response (str): The response text from the chatbot.
    Yields:
        str: Tokenized response text.
    """
    response_tokens = response.split()
    for token in response_tokens:
        yield token + ' '
        time.sleep(0.025)  # Adjust the delay between tokens to control the speed of the typewriter effect

