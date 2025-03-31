import streamlit as st
import os
from drive_thru_ai.agent.ai_agent import DriveThruAgent


def show_drive_thru():
    st.set_page_config(page_title="AI Drive-Thru", layout="wide")

    # Initialize session state for the AI agent
    if 'agent' not in st.session_state:
        # Get API key from environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            st.error("Please set the OPENAI_API_KEY environment variable")
            return
        st.session_state.agent = DriveThruAgent()

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to order?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            response = st.session_state.agent.process_customer_input(prompt)
            st.write(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response})

    # Add a sidebar with order summary
    with st.sidebar:
        st.header("Order Summary")
        current_order = st.session_state.agent.get_current_order()
        if current_order:
            for item in current_order:
                st.write(
                    f"- {item.get_description()}: ${item.get_price():.2f}")
            st.write(
                f"**Total: ${st.session_state.agent.get_order_total(current_order):.2f}**")
        else:
            st.write("No items in order yet")


if __name__ == "__main__":
    show_drive_thru()
