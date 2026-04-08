import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from groq import Groq

# Configure the Groq API
API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

# Configure Streamlit page
st.set_page_config(page_title="Finance Helper Chatbot", layout="centered")
st.title("💰 Finance Helper Chatbot")
st.subheader("Your AI assistant for budgeting, saving, investing, and personal finance")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I'm your finance assistant. Ask me anything about budgeting, saving money, investing, or managing expenses. How can I help you today?"
        }
    ]

def display_messages():
    """Display all messages in the chat history"""
    for msg in st.session_state.messages:
        author = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(author):
            st.write(msg["content"])

def friendly_wrap(raw_text):
    """Add a friendly finance tone to AI responses"""
    return (
        "Great question! 💰\n\n"
        f"{raw_text.strip()}\n\n"
        "Would you like help creating a budget, saving plan, or investment strategy?"
    )

# Display existing messages
display_messages()

# Handle new user input
prompt = st.chat_input("Ask me about budgeting, saving, investments, loans...")

if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show user message
    with st.chat_message("user"):
        st.write(prompt)

    # Show thinking indicator while processing
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("🤔 Thinking...")

        # Call Groq API
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=1024,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful financial assistant. "
                            "Provide clear, practical advice on budgeting, saving money, "
                            "debt management, and basic investing. "
                            "Keep explanations simple and beginner-friendly. "
                            "Avoid giving risky or overly specific financial predictions."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract response text
            answer = response.choices[0].message.content
            friendly_answer = friendly_wrap(answer)

        except Exception as e:
            friendly_answer = f"I'm sorry, I encountered an error: {e}. Please try asking your question again."

        # Replace thinking indicator with actual response
        placeholder.write(friendly_answer)

        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": friendly_answer})

    # Refresh the page to show updated chat
    st.rerun()