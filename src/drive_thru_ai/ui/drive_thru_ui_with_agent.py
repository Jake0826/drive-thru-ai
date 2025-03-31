import streamlit as st
import os
from drive_thru_ai.agent.simple_agent import SimpleDriveThruAgent
from collections import Counter


def show_drive_thru():
    st.set_page_config(page_title="AI Drive-Thru", layout="wide")

    # Initialize session state for the AI agent
    if 'agent' not in st.session_state:
        # Get API key from environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            st.error("Please set the OPENAI_API_KEY environment variable")
            return
        st.session_state.agent = SimpleDriveThruAgent()

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
            # Create a counter for item descriptions
            item_counts = Counter(item.get_description()
                                  for item in current_order)

            # Display items with their quantities
            for description, count in item_counts.items():
                item_price = next(item.get_price(
                ) for item in current_order if item.get_description() == description)
                if count > 1:
                    st.write(
                        f"- {count}x {description}: ${item_price * count:.2f}")
                else:
                    st.write(f"- {description}: ${item_price:.2f}")

            st.write(
                f"**Total: ${st.session_state.agent.get_order_total():.2f}**")
        else:
            st.write("No items in order yet")


if __name__ == "__main__":
    show_drive_thru()
