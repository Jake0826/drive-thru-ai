import streamlit as st
import os
import time
import threading
from collections import Counter
from drive_thru_ai.agent.simple_agent import SimpleDriveThruAgent
from drive_thru_ai.agent.audio_recorder import AudioRecorder


def show_drive_thru():
    st.set_page_config(page_title="AI Drive-Thru", layout="wide")
    
    # Debug container at the top
    debug_container = st.container()
    with debug_container:
        st.subheader("Debug Information")
        debug_info = st.empty()
    
    # Initialize debug messages list
    if 'debug_messages' not in st.session_state:
        st.session_state.debug_messages = []
    
    def add_debug(message):
        """Add a debug message with timestamp"""
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        st.session_state.debug_messages.append(f"[{timestamp}] {message}")
        # Keep only last 10 messages
        if len(st.session_state.debug_messages) > 10:
            st.session_state.debug_messages = st.session_state.debug_messages[-10:]
        # Update debug display
        debug_info.markdown("\n".join(st.session_state.debug_messages))

    # Auto-refresh the app at regular intervals
    auto_refresh = st.empty()
    
    # Initialize agent if not already done
    if 'agent' not in st.session_state:
        add_debug("Initializing agent...")
        try:
            st.session_state.agent = SimpleDriveThruAgent()
            add_debug("Agent initialized successfully")
        except Exception as e:
            add_debug(f"Error initializing agent: {str(e)}")
    
    # Initialize recorder if not already done
    if 'recorder' not in st.session_state:
        add_debug("Initializing audio recorder...")
        try:
            st.session_state.recorder = AudioRecorder(
                st.session_state.agent.elevenlabs_client)
            add_debug("Audio recorder initialized")
        except Exception as e:
            add_debug(f"Error initializing audio recorder: {str(e)}")

    # Initialize chat history
    if 'messages' not in st.session_state:
        add_debug("Initializing chat history...")
        st.session_state.messages = []
        
        # Add welcome message to chat history
        welcome_message = "Welcome to McDonald's, how can I help you today?"
        st.session_state.messages.append(
            {"role": "assistant", "content": welcome_message})
        add_debug(f"Added welcome message: {welcome_message}")
        
        # Play welcome message
        add_debug("Converting welcome message to speech...")
        try:
            audio_stream = st.session_state.agent.text_to_speech_stream(
                welcome_message)
            if audio_stream:
                add_debug("Playing welcome audio...")
                st.session_state.agent.play_audio(audio_stream, st.session_state.recorder)
                add_debug("Welcome audio played")
            else:
                add_debug("Failed to generate welcome audio")
        except Exception as e:
            add_debug(f"Error in welcome audio: {str(e)}")
    
    # Initialize processing states
    if 'is_processing' not in st.session_state:
        st.session_state.is_processing = False
    
    if 'last_processed_transcription' not in st.session_state:
        st.session_state.last_processed_transcription = ""
    
    # Start recording if not already started
    if not getattr(st.session_state.recorder, 'is_recording', False):
        add_debug("Starting recording...")
        try:
            st.session_state.recorder.start_recording()
            add_debug("Recording started")
        except Exception as e:
            add_debug(f"Error starting recording: {str(e)}")

    # Display the chat messages
    st.subheader("Drive-Thru Conversation")
    chat_container = st.container(height=400)
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Status indicator
    status_container = st.empty()
    recorder_status = getattr(st.session_state.recorder, 'get_status', lambda: "unknown")()
    status_container.write(f"Status: {recorder_status}")
    
    # Check for new transcriptions
    add_debug("Checking for new transcriptions...")
    transcription = None
    try:
        transcription = st.session_state.recorder.get_transcription()
        if transcription:
            add_debug(f"New transcription detected: '{transcription}'")
            # Display raw transcription for debugging
            st.write(f"Raw transcription: '{transcription}'")
        else:
            add_debug("No new transcription detected")
    except Exception as e:
        add_debug(f"Error getting transcription: {str(e)}")
    
    # Process transcription if new and not already processing
    if (transcription and 
        transcription != st.session_state.last_processed_transcription and 
        not st.session_state.is_processing):
        
        add_debug(f"Processing new transcription: '{transcription}'")
        st.session_state.is_processing = True
        add_debug("Set is_processing = True")
        
        # Update status
        status_container.write(f"Status: Processing user input: '{transcription}'")
        
        # Add user message to chat history
        user_message = transcription
        st.session_state.messages.append(
            {"role": "user", "content": user_message})
        add_debug(f"Added user message to history: '{user_message}'")
        
        # Display user message in chat
        with chat_container:
            with st.chat_message("user"):
                st.write(user_message)
                add_debug("Displayed user message in chat")
        
        # Get AI response
        with chat_container:
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                response_placeholder.write("Thinking...")
                add_debug("Getting AI response...")
                
                try:
                    # Process user input and get response
                    response = st.session_state.agent.process_customer_input(
                        user_message, st.session_state.recorder)
                    add_debug(f"AI response received: '{response}'")
                    response_placeholder.write(response)
                    
                    # Add response to chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response})
                    add_debug("Added AI response to chat history")
                    
                    # Play audio response
                    add_debug("Converting AI response to speech...")
                    audio_stream = st.session_state.agent.text_to_speech_stream(response)
                    if audio_stream:
                        add_debug("Playing AI response audio...")
                        # Pass the recorder to the play_audio method
                        st.session_state.agent.play_audio(audio_stream, st.session_state.recorder)
                        add_debug("AI response audio played")
                    else:
                        add_debug("Failed to generate response audio")
                except Exception as e:
                    add_debug(f"Error in AI response processing: {str(e)}")
                    response_placeholder.write("I'm sorry, I couldn't process that. Could you please repeat?")
        
        # Update processing state
        st.session_state.last_processed_transcription = transcription
        st.session_state.is_processing = False
        add_debug("Set is_processing = False")
        add_debug("Finished processing transcription")
        
        # Force a rerun to update the UI
        st.rerun()
    
    # Show order summary in sidebar
    with st.sidebar:
        st.header("Order Summary")
        try:
            current_order = st.session_state.agent.get_current_order()
            if current_order:
                add_debug(f"Retrieved current order with {len(current_order)} items")
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
                add_debug("No items in current order")
                st.write("No items in order yet")
        except Exception as e:
            add_debug(f"Error displaying order summary: {str(e)}")
            st.write("Error displaying order")
    
    # Add manual controls
    col1, col2 = st.columns(2)
    
    # Refresh button
    if col1.button("Refresh UI"):
        add_debug("Manual refresh requested")
        st.rerun()
    
    # Reset button
    if col2.button("Reset Conversation"):
        add_debug("Resetting conversation")
        st.session_state.messages = []
        st.session_state.agent.clear_order()
        st.session_state.last_processed_transcription = ""
        st.session_state.is_processing = False
        
        # Add welcome message
        welcome_message = "Welcome back to McDonald's, how can I help you today?"
        st.session_state.messages.append(
            {"role": "assistant", "content": welcome_message})
        
        # Generate speech
        audio_stream = st.session_state.agent.text_to_speech_stream(welcome_message)
        if audio_stream:
            st.session_state.agent.play_audio(audio_stream)
        
        st.rerun()
    
    # Add auto refresh every 2 seconds (unless already processing)
    if not st.session_state.is_processing:
        auto_refresh.empty()  # Clear previous timer
        time.sleep(0.5)  # Wait a bit before next check
        st.rerun()


if __name__ == "__main__":
    show_drive_thru()