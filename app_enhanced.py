"""
Enhanced SHAKTI-AI Streamlit application with voice input and sharing features.
"""

import streamlit as st
from crew import ask_shakti_ai
from dotenv import load_dotenv
import os
from get_voice_input import get_voice_input
from streamlit.components.v1 import html
import random
from datetime import datetime, timedelta
from wishes_vault_enhanced import show_secure_wishes_vault

# Load environment variables
load_dotenv()

# --- Utility: Safe word detection ---
def safe_word_detected():
    for v in st.session_state.values():
        if isinstance(v, str) and ("SAFE RELEASE" in v.upper() or v.upper().strip() == "SAFE"):
            return True
    return False

# --- Fake Weather UI (Panic Mode) ---
def show_fake_weather():
    st.markdown("""
    <style>
    [data-testid="stSidebar"], .block-container .sidebar-content { display: none !important; }
    .fake-search-bar {background:#f3f3f3;border-radius:8px;padding:0.5em 1em;display:flex;align-items:center;max-width:350px;margin:0 auto 1em auto;border:1px solid #ddd;}
    .fake-search-bar input {border:none;background:transparent;outline:none;width:100%;font-size:1em;}
    .weather-main {text-align:center;}
    .weather-forecast {display:flex;justify-content:center;gap:1.5em;margin-top:1em;}
    .weather-forecast-day {background:#f8f9fa;border-radius:8px;padding:0.7em 1em;min-width:90px;box-shadow:0 1px 4px #0001;}
    .aqi-badge {background:#ffe066;color:#444;padding:0.2em 0.7em;border-radius:1em;font-weight:bold;}
    .travel-ad {background:#fff3cd;color:#856404;padding:0.7em 1em;border-radius:8px;margin:1em auto;max-width:400px;text-align:center;font-size:1.1em;box-shadow:0 2px 8px #0001;}
    .helpline-item {margin-bottom:0.5em;display:flex;align-items:center;}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='fake-search-bar'>
        <span style='color:#888;margin-right:0.5em;'>🔍</span>
        <input type='text' value='Search City' disabled style='color:#aaa;'>
    </div>
    """, unsafe_allow_html=True)
    
    now = datetime.now()
    temp = random.randint(24, 36)
    humidity = random.randint(40, 80)
    wind = random.randint(5, 20)
    aqi = random.randint(40, 120)
    
    conditions = [
        ("Sunny", "☀️"),
        ("Partly Cloudy", "⛅"),
        ("Overcast", "☁️"),
        ("Light Rain", "🌦️")
    ]
    condition, icon = random.choice(conditions)
    
    st.markdown(f"""
    <div class='weather-main'>
        <h1>{icon} {temp}°C</h1>
        <h3>{condition}</h3>
        <p>Humidity: {humidity}% | Wind: {wind} km/h</p>
        <span class='aqi-badge'>AQI {aqi}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Forecast
    st.markdown("<div class='weather-forecast'>", unsafe_allow_html=True)
    for i in range(1, 6):
        day_temp = random.randint(22, 35)
        day_condition, day_icon = random.choice(conditions)
        st.markdown(
            f"<div class='weather-forecast-day'><div style='font-weight:bold;'>{(now + timedelta(days=i)).strftime('%a')}</div>"
            f"<div style='font-size:1.5em;margin:0.3em 0;'>{day_icon}</div><div>{day_temp}°C</div></div>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Helplines button
    if st.button("🆘 Emergency Services"):
        st.session_state['show_helplines'] = not st.session_state.get('show_helplines', False)

    if st.session_state.get('show_helplines', False):
        st.info("Stay safe during monsoon — here's some emergency contacts:")
        helplines = [
            ("Women Helpline", "1091"),
            ("Mental Health Helpline", "7827170170"),
            ("Police", "100"),
            ("Child Helpline", "1098"),
        ]
        for label, number in helplines:
            wa_msg = "Hello, I need help urgently. Please assist."
            wa_url = f"https://wa.me/91{number}?text={wa_msg.replace(' ', '%20')}"
            col1, col2, col3 = st.columns([4,1,1])
            with col1:
                st.write(f"**{label}:** {number}")
            with col2:
                if st.button(f"📋", key=f"copy_{number}"):
                    st.success(f"Copied: {number}")
            with col3:
                st.markdown(f"[📲]({wa_url})", unsafe_allow_html=True)

        if st.button("❌ Close Helplines"):
            st.session_state['show_helplines'] = False

    # Exit panic mode
    if st.button("🔄 Refresh Weather Feed"):
        st.session_state['panic_mode'] = False
        st.session_state['show_helplines'] = False
        st.rerun()

# --- PANIC BUTTON ---
def show_panic_button():
    if 'panic_mode' not in st.session_state:
        st.session_state['panic_mode'] = False
    if 'show_helplines' not in st.session_state:
        st.session_state['show_helplines'] = False
    
    if not st.session_state['panic_mode']:
        with st.sidebar:
            if st.button("🚨 Panic", help="Quickly hide this app and show neutral content", key="sidebar_panic_btn"):
                st.session_state['panic_mode'] = True
                st.rerun()

# Always show panic button
show_panic_button()

# --- PANIC MODE LOGIC ---
if st.session_state.get('panic_mode', False):
    # Clear all session state except panic/helplines/vault keys
    preserve_keys = {'panic_mode', 'show_helplines', 'wishes_key', 'wishes_input', 'contact_name', 'contact_info', 'show_wishes_form'}
    for k in list(st.session_state.keys()):
        if k not in preserve_keys:
            del st.session_state[k]
    
    show_fake_weather()
    
    if safe_word_detected():
        show_secure_wishes_vault(neutral_mode=True)
    st.stop()

# --- MAIN APPLICATION ---
# Page configuration
st.set_page_config(
    page_title="SHAKTI-AI | Women's Health & Legal AI Agents",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Styling
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom right, #fff0f6, #ffe0ef);
}
.main {
    padding: 2rem;
}
h1, h2, h3, h4, h5, h6 {
    color: #c9184a;
    font-family: 'Arial', sans-serif;
}
.stTextInput > div > input,
.stNumberInput input {
    border: 2px solid #f783ac;
    border-radius: 8px;
}
.stButton > button {
    background-color: #f783ac !important;
    color: #fff !important;
    border-radius: 20px;
    font-weight: bold;
    border: none;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    background-color: #d6336c !important;
    transform: translateY(-2px);
}
.stTextArea textarea {
    border: 2px solid #f783ac;
    border-radius: 8px;
}
.voice-button {
    background: linear-gradient(45deg, #f783ac, #d6336c) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 10px 20px !important;
    font-weight: bold !important;
    box-shadow: 0 4px 15px rgba(247, 131, 172, 0.4) !important;
    transition: all 0.3s ease !important;
}
.voice-button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 6px 20px rgba(247, 131, 172, 0.6) !important;
}
.agent-card {
    background-color: #ffe0ef;
    border-left: 5px solid #f783ac;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("🧬 SHAKTI-AI")
st.subheader("AI-powered support for women's health, legal rights, and well-being")

# Sidebar with agent information
st.sidebar.title("Meet Your AI Support Team")

with st.sidebar.expander("👶 Maaya - For Moms, By Heart", expanded=False):
    st.markdown("""
    **Expertise**: Pregnancy, childbirth, and baby care
    
    Maaya is your comforting pregnancy guide — here to cut through myths, answer every "is this normal?", 
    and keep you calm from bump to baby, with advice that actually makes sense for you.
    """)

with st.sidebar.expander("🌸 Gynika - Flow Friend", expanded=False):
    st.markdown("""
    **Expertise**: Menstruation, puberty, and contraception
    
    Gynika is your real talk reproductive guide — ditching the whispers and giving you straight-up truth on 
    your cycle, contraception, and more.
    """)

with st.sidebar.expander("🧘‍♀️ Meher - Gentle Guide", expanded=False):
    st.markdown("""
    **Expertise**: Emotional support for trauma, anxiety, and abuse
    
    Meher is your gentle guide — here to listen without judging, name what hurts, and remind you you're never 
    too much, even on your hardest days.
    """)

with st.sidebar.expander("⚖️ Nyaya - Rights Ally", expanded=False):
    st.markdown("""
    **Expertise**: Indian laws on consent, abortion, and family rights
    
    Nyaya is your rights ally — here to break down India's messy laws, decode your choices, and make sure
    you know exactly what's yours to fight for.
    """)

with st.sidebar.expander("💪 Vaanya - Age Rebel", expanded=False):
    st.markdown("""
    **Expertise**: Menopause, hormonal health, and women's empowerment
    
    Vaanya is your health rebel — here to smash taboos, keep you clued up on your body, and
    remind you that ageing strong is your superpower.
    """)

# Main content area
st.markdown("### Your space, your questions — we're listening")

# --- Enhanced Voice Input UI ---
st.markdown("#### 🎤 Voice Input")

col_voice, col_status = st.columns([2, 8])

with col_voice:
    # Enhanced microphone button with icon and text
    voice_button_clicked = st.button(
        '🎤 Speak Now', 
        help='Click to start voice input with medical term recognition',
        use_container_width=True,
        key="voice_input_btn"
    )
    
    if voice_button_clicked:
        with st.spinner('🎧 Listening... Please speak clearly about your health concerns'):
            spoken_text = get_voice_input()
            st.session_state['spoken_text'] = spoken_text
            
            if spoken_text:
                st.session_state['query_text'] = spoken_text
                st.success(f"✅ Recognized: \"{spoken_text}\"")
                st.balloons()
            else:
                st.warning("⚠️ No speech detected. Please try again and speak clearly.")

with col_status:
    # Show current voice input status
    if 'spoken_text' in st.session_state and st.session_state['spoken_text']:
        display_text = st.session_state['spoken_text']
        if len(display_text) > 100:
            display_text = display_text[:100] + "..."
        st.info(f"🗣️ Voice input ready: \"{display_text}\"")

# --- Text Input ---
st.markdown("#### ✍️ Text Input")
query = st.text_area(
    "Tell us what's on your mind…",
    height=150,
    placeholder="Example: I'm 8 weeks pregnant and keep feeling dizzy, is this normal?",
    key='query_text',
    help="You can type here or use voice input above"
)

# Age input
age = st.text_input("Your Age (optional)", placeholder="e.g., 25")
if age:
    try:
        age = int(age)
    except:
        st.warning("Please enter age as a number.")
        age = None

# Use spoken_text if available, otherwise use typed text
if 'spoken_text' in st.session_state and st.session_state['spoken_text']:
    query = st.session_state['spoken_text']
else:
    query = st.session_state.get('query_text', '')

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
    feminist = st.checkbox("Hormonal Health", value=False)

# Submit button
if st.button("Get Guidance", use_container_width=True):
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
            response = ask_shakti_ai(query, selected_agents, age)
            
            # Display response
            st.markdown("### Expert Guidance")
            st.markdown(f"{response}")
            
            # Display feedback options
            st.markdown("### Was this helpful?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Yes, thank you"):
                    st.success("Thank you for your feedback!")
            with col2:
                if st.button("👎 Not really"):
                    st.info("We'll work on improving our responses. Thank you for letting us know.")
    else:
        st.error("Please enter a question or concern.")

# Enhanced Wishes Vault
st.markdown("---")
show_secure_wishes_vault()

# Footer
st.markdown("---")
st.markdown("✨ *SHAKTI-AI: For every woman, every phase, every fight.* ✨")
st.markdown(
    "**Disclaimer:** SHAKTI-AI provides general information only and is not a substitute for professional medical, legal, or mental health advice. "
    "Always consult qualified professionals for specific concerns."
)
