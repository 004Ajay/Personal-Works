import streamlit as st
import ollama
import time

# Function to simulate streaming data
def stream_data(text, delay: float = 0.05):
    for word in text.split():
        yield word + " "
        time.sleep(delay)

# Function to get response from the Ollama API
def get_ollama_response(user_input):
    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": user_input}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

st.title("ChatGPT Clone")

# Resetting session_state 'chat_history' simulating "Clear Chat"
if st.button("Clear Chat"):
    st.session_state['chat_history'] = []

# Initializing chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.chat_input("Ask Me...") # Chat input box at bottom

# Display chat history
if st.session_state['chat_history']:
    for i, message in enumerate(st.session_state['chat_history']):
        if i % 2 == 0:
            st.markdown(f"**User**: {message}")
        else:
            st.markdown(f"**Bot**: {message}")

if user_input:
    # Append user input to chat history and immediately display it
    st.session_state['chat_history'].append(user_input)
    st.markdown(f"**User**: {user_input}")
    
    # Create a placeholder for the bot's response to simulate streaming
    bot_response_placeholder = st.empty()

    # Get model response from Ollama
    response = get_ollama_response(user_input)
    
    # Stream the bot's response word by word
    response_text = ""
    for word in stream_data(response):
        response_text += word
        bot_response_placeholder.markdown(f"**Bot**: {response_text}")
    
    # Append the final bot response to the chat history
    st.session_state['chat_history'].append(response_text)
