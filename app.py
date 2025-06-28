"""
Streamlit application for SHAKTI-AI.
"""

import streamlit as st
from crew import ask_shakti_ai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SHAKTI-AI | Women's Health & Legal AI Agents",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .agent-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #ff6b6b;
    }
    .stButton button {
        background-color: #ff6b6b;
        color: white;
        border-radius: 5px;
    }
    h1, h2, h3 {
        color: #444;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("🧬 SHAKTI-AI")
st.subheader("AI-powered support for women's health, legal rights, and well-being")

# Sidebar with agent information
st.sidebar.title("Meet Your AI Support Team")

with st.sidebar.expander("👶 Maaya - Maternal Health", expanded=False):
    st.markdown("""
    **Expertise**: Pregnancy, childbirth, and baby care
    
    Maaya is like the experienced nurse in your neighborhood, offering practical guidance through your 
    maternal journey with warmth and evidence-based knowledge.
    """)

with st.sidebar.expander("🌸 Gynika - Reproductive Health", expanded=False):
    st.markdown("""
    **Expertise**: Menstruation, puberty, and contraception
    
    Gynika provides judgment-free information about your reproductive health, helping break taboos and 
    empowering you with accurate knowledge about your body.
    """)

with st.sidebar.expander("🧘‍♀️ Meher - Mental Wellness", expanded=False):
    st.markdown("""
    **Expertise**: Emotional support for trauma, anxiety, and abuse
    
    Meher is your compassionate mental health ally, offering culturally sensitive guidance through 
    emotional challenges with a blend of modern psychology and holistic approaches.
    """)

with st.sidebar.expander("⚖️ Nyaya - Legal Rights", expanded=False):
    st.markdown("""
    **Expertise**: Indian laws on consent, abortion, and family rights
    
    Nyaya helps you understand your legal rights and options within the Indian legal system, explaining 
    complex concepts in straightforward language.
    """)

with st.sidebar.expander("💪 Vaanya - Feminist Health", expanded=False):
    st.markdown("""
    **Expertise**: Menopause, hormonal health, and women's empowerment
    
    Vaanya is your guide through later-life health transitions, combining scientific understanding with 
    advocacy for women's autonomy and challenging patriarchal medical systems.
    """)

# Main content area
st.markdown("### How can we support you today?")

# Input area
query = st.text_area(
    "Enter your question or concern",
    height=150,
    placeholder="Example: I'm 6 weeks pregnant and experiencing morning sickness. What can I do to manage it?"
)

# Agent selection
st.markdown("### Which experts would you like to consult? (Optional)")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    maternal = st.checkbox("Maternal Health", value=False)
with col2:
    reproductive = st.checkbox("Reproductive Health", value=False)
with col3:
    mental = st.checkbox("Mental Health", value=False)
with col4:
    legal = st.checkbox("Legal Rights", value=False)
with col5:
    feminist = st.checkbox("Feminist Health", value=False)

# Submit button
if st.button("Get Guidance"):
    if query:
        with st.spinner("Consulting with SHAKTI-AI experts..."):
            # Determine which agents to use based on checkboxes
            selected_agents = []
            if maternal:
                selected_agents.append("maternal")
            if reproductive:
                selected_agents.append("reproductive")
            if mental:
                selected_agents.append("mental")
            if legal:
                selected_agents.append("legal")
            if feminist:
                selected_agents.append("feminist")
            
            # If no specific agents selected, use all
            if not selected_agents:
                selected_agents = None
                
            # Get response from SHAKTI-AI
            response = ask_shakti_ai(query, selected_agents)
            
            # Display response
            st.markdown("### Expert Guidance")
            st.markdown(f"{response}")
            
            # Display feedback options
            st.markdown("### Was this helpful?")
            col1, col2 = st.columns(2)
            with col1:
                st.button("👍 Yes, thank you")
            with col2:
                st.button("👎 Not really")
    else:
        st.error("Please enter a question or concern.")

# Footer
st.markdown("---")
st.markdown(
    "SHAKTI-AI provides general information only and is not a substitute for professional medical, legal, or mental health advice. "
    "Always consult qualified professionals for specific concerns."
)
