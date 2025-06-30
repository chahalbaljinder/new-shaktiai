"""
Simple test for voice input functionality.
"""

import streamlit as st
from get_voice_input import get_voice_input

st.title("🎤 Voice Input Test")

# Initialize session state
if 'voice_result' not in st.session_state:
    st.session_state['voice_result'] = ""

# Voice input button
if st.button("🎤 Test Voice Input"):
    with st.spinner("🎧 Listening..."):
        result = get_voice_input()
        if result:
            st.session_state['voice_result'] = result
            st.success(f"Voice input captured: {result}")
        else:
            st.error("No speech detected")

# Text area showing the result
query = st.text_area(
    "Voice input will appear here:",
    value=st.session_state['voice_result'],
    height=100
)

st.write(f"Current session state: {st.session_state.get('voice_result', 'None')}")
