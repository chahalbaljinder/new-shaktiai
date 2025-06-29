"""
Enhanced SHAKTI-AI Streamlit application with voice input and sharing features.
"""

import streamlit as st
from core.crew import ask_shakti_ai
from dotenv import load_dotenv
import os
from core.get_voice_input import get_voice_input, get_voice_input_interactive
from streamlit.components.v1 import html
import random
from datetime import datetime, timedelta
from database.wishes_vault_db import show_secure_wishes_vault

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
    /* Hide sidebar and set full width */
    [data-testid="stSidebar"], .block-container .sidebar-content { display: none !important; }
    
    /* Hide ALL Streamlit header and toolbar elements */
    header[data-testid="stHeader"] { display: none !important; }
    .stApp > header { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    [data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
    .stApp { margin-top: 0 !important; padding-top: 0 !important; }
    .main { margin-top: 0 !important; padding-top: 0 !important; }
    
    /* Remove any top spacing from containers */
    .element-container { margin-top: 0 !important; padding-top: 0 !important; }
    .stMarkdown { margin-top: 0 !important; padding-top: 0 !important; }
    .block-container { padding-top: 0 !important; margin-top: 0 !important; }
    
    /* Force full height and remove any gaps */
    html, body, #root, .stApp { 
        margin: 0 !important; 
        padding: 0 !important; 
        height: 100% !important; 
    }
    
    /* Main container styling */
    .main .block-container {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%) !important;
        min-height: 100vh !important;
        position: relative !important;
        top: 0 !important;
    }
    
    /* Weather app container */
    .weather-app-container {
        max-width: 800px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin-top: 2rem;
        position: relative;
        z-index: 1;
    }
    
    /* Search bar styling - Improved */
    .fake-search-bar {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 25px;
        padding: 1em 1.5em;
        display: flex;
        align-items: center;
        max-width: 450px;
        margin: 0 auto 2em auto;
        border: 2px solid #e3f2fd;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .fake-search-bar:hover {
        border-color: #74b9ff;
        box-shadow: 0 6px 20px rgba(116, 185, 255, 0.15);
    }
    
    .fake-search-bar input {
        border: none;
        background: transparent;
        outline: none;
        width: 100%;
        font-size: 1.1em;
        color: #495057;
        font-weight: 500;
    }
    
    .fake-search-bar input::placeholder {
        color: #6c757d;
        font-style: italic;
    }
    
    .search-icon {
        color: #74b9ff !important;
        margin-right: 1em;
        font-size: 1.3em;
    }
    
    .location-icon {
        color: #fd79a8 !important;
        margin-left: 1em;
        font-size: 1.3em;
        cursor: pointer;
        transition: transform 0.2s ease;
    }
    
    .location-icon:hover {
        transform: scale(1.1);
    }
    
    /* Navigation tabs */
    .nav-tabs {
        text-align: center;
        margin: 1em 0 2em 0;
    }
    
    .nav-tab {
        background: linear-gradient(45deg, #74b9ff, #0984e3);
        color: white;
        padding: 0.5em 1.2em;
        border-radius: 20px;
        font-size: 0.9em;
        margin: 0.2em;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        font-weight: 600;
    }
    
    /* Main weather display */
    .weather-main {
        text-align: center;
        margin-bottom: 2em;
        padding: 1.5em;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        color: white;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    .weather-main h3 {
        margin: 0.3em 0;
        color: #ffffff !important;
        font-size: 1.2em;
        opacity: 0.9;
    }
    
    .weather-main h1 {
        margin: 0.2em 0;
        color: #ffffff !important;
        font-size: 3em;
        font-weight: 300;
    }
    
    .weather-main p {
        margin: 0.3em 0;
        color: #ffffff !important;
        font-size: 1.1em;
        opacity: 0.9;
    }
    
    /* Forecast cards - Force Horizontal Layout */
    .compact-forecast {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: stretch !important;
        gap: 1em !important;
        margin: 1.5em 0 !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        padding: 0.5em !important;
        width: 100% !important;
    }
    
    .forecast-card {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%) !important;
        border-radius: 16px !important;
        padding: 1.2em 0.8em !important;
        min-width: 110px !important;
        flex: 1 1 0px !important;
        max-width: 150px !important;
        text-align: center !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1) !important;
        font-size: 0.9em !important;
        color: #495057 !important;
        transition: all 0.3s ease !important;
        border: 2px solid transparent !important;
        display: inline-block !important;
        vertical-align: top !important;
    }
    
    .forecast-card:hover {
        transform: translateY(-4px);
        border-color: #74b9ff;
        box-shadow: 0 8px 25px rgba(116, 185, 255, 0.2);
    }
    
    .forecast-day {
        font-weight: 700;
        color: #2d3436 !important;
        font-size: 0.9em;
        margin-bottom: 0.5em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .forecast-icon {
        font-size: 2.2em;
        margin: 0.4em 0;
        display: block;
    }
    
    .forecast-temp {
        font-weight: 700;
        color: #2d3436 !important;
        font-size: 1.2em;
        margin: 0.3em 0;
    }
    
    .forecast-rain {
        color: #74b9ff !important;
        font-size: 0.85em;
        font-weight: 600;
    }
    
    /* Badges and metrics */
    .aqi-badge {
        background: linear-gradient(45deg, #ffeaa7, #fdcb6e);
        color: #2d3436;
        padding: 0.4em 0.8em;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9em;
        display: inline-block;
        margin-top: 0.5em;
    }
    
    .small-metric {
        display: inline-block;
        margin: 0.3em;
        padding: 0.5em 0.8em;
        background: linear-gradient(45deg, #74b9ff, #0984e3);
        color: white;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: 500;
    }
    
    /* Info sections */
    .compact-section {
        margin: 1em 0;
        padding: 1.2em;
        background: #ffffff;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .compact-section h5 {
        margin: 0 0 0.8em 0;
        color: #495057 !important;
        font-size: 1em;
        font-weight: 600;
    }
    
    .compact-section div {
        color: #6c757d !important;
        font-size: 0.9em;
    }
    
    /* Time display */
    .time-display {
        text-align: center;
        margin: 1.5em 0;
        padding: 1em;
        background: linear-gradient(45deg, #a29bfe, #6c5ce7);
        border-radius: 12px;
        color: white !important;
    }
    
    .time-display span {
        color: white !important;
        font-weight: 600;
    }
    
    /* Emergency services */
    .emergency-card {
        background: linear-gradient(135deg, #fd79a8, #e84393);
        padding: 0.8em;
        margin: 0.3em 0;
        border-radius: 8px;
        border-left: 4px solid #d63031;
        color: white !important;
    }
    
    .emergency-card div {
        color: white !important;
    }
    
    .emergency-card a {
        color: #ffffff !important;
        text-decoration: none;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #00b894, #00a085) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.5em 1.5em !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #00a085, #00b894) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 184, 148, 0.3) !important;
    }
    
    /* Responsive design for mobile */
    @media (max-width: 768px) {
        .weather-app-container {
            padding: 1.5rem;
            margin: 0.5rem;
        }
        
        .fake-search-bar {
            max-width: 100%;
            margin: 0 0 1.5em 0;
        }
        
        .compact-forecast {
            gap: 0.5em;
            overflow-x: scroll;
            padding-bottom: 1em;
        }
        
        .forecast-card {
            min-width: 80px;
            max-width: 90px;
            padding: 1em 0.6em;
        }
        
        .weather-main h1 {
            font-size: 2.5em !important;
        }
        
        .nav-tab {
            padding: 0.4em 0.8em;
            font-size: 0.8em;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    
    # Main weather app container
    st.markdown('<div class="weather-app-container">', unsafe_allow_html=True)
    
    # Improved search bar and tabs
    st.markdown("""
    <div class='fake-search-bar'>
        <span class='search-icon'>🔍</span>
        <input type='text' placeholder='Search for a city...' disabled>
        <span class='location-icon'>📍</span>
    </div>
    <div class='nav-tabs'>
        <span class='nav-tab'>☀️ Today</span>
        <span class='nav-tab'>📅 Week</span>
        <span class='nav-tab'>🌍 Maps</span>
    </div>
    """, unsafe_allow_html=True)
    
    now = datetime.now()
    cities = ["New Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad"]
    current_city = random.choice(cities)
    temp = random.randint(24, 36)
    humidity = random.randint(40, 80)
    wind = random.randint(5, 20)
    aqi = random.randint(40, 120)
    
    conditions = [
        ("Sunny", "☀️"), ("Cloudy", "⛅"), ("Rainy", "🌦️"), ("Stormy", "⛈️"), ("Hazy", "🌫️")
    ]
    condition, icon = random.choice(conditions)
    feels_like = temp + random.randint(-3, 5)
    
    # Main weather display
    st.markdown(f"""
    <div class='weather-main'>
        <h3>📍 {current_city}</h3>
        <h1>{icon} {temp}°C</h1>
        <p>{condition} • Feels like {feels_like}°C</p>
        <span class='aqi-badge'>AQI {aqi}</span>
        <div style='margin-top:1em;'>
            <span class='small-metric'>💧 {humidity}%</span>
            <span class='small-metric'>💨 {wind} km/h</span>
            <span class='small-metric'>👁️ {random.randint(8,15)} km</span>
            <span class='small-metric'>🌡️ {random.randint(1010,1025)} mb</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 5-day forecast with horizontal cards
    st.markdown("<h4 style='text-align:center;margin:2em 0 1em 0;color:#2d3436;font-size:1.4em;font-weight:700;'>📅 5-Day Forecast</h4>", unsafe_allow_html=True)
    
    # Generate all forecast cards in a single HTML string
    forecast_html = "<div class='compact-forecast'>"
    
    for i in range(1, 6):
        future_date = now + timedelta(days=i)
        day_temp = random.randint(22, 38)
        day_condition, day_icon = random.choice(conditions)
        rain_chance = random.randint(0, 80)
        
        forecast_html += f"""
        <div class='forecast-card'>
            <div class='forecast-day'>{future_date.strftime('%a')}</div>
            <div class='forecast-icon'>{day_icon}</div>
            <div class='forecast-temp'>{day_temp}°</div>
            <div class='forecast-rain'>💧 {rain_chance}%</div>
        </div>"""
    
    forecast_html += "</div>"
    st.markdown(forecast_html, unsafe_allow_html=True)
    
    # Compact grid layout for additional info
    col1, col2 = st.columns(2)
    
    with col1:
        # Air Quality
        st.markdown(f"""
        <div class='compact-section'>
            <h5>🌬️ Air Quality</h5>
            <div style='display:flex;justify-content:space-between;'>
                <span><strong>PM2.5:</strong> {random.randint(25, 85)}</span>
                <span><strong>PM10:</strong> {random.randint(40, 120)}</span>
                <span><strong>O₃:</strong> {random.randint(30, 80)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sun times
        sunrise_hour = random.randint(5, 7)
        sunset_hour = random.randint(17, 19)
        st.markdown(f"""
        <div class='compact-section'>
            <h5 style='margin:0.2em 0;color:#555;font-size:0.9em;'>🌅 Sun Times</h5>
            <div style='display:flex;justify-content:space-between;font-size:0.8em;'>
                <span>🌅 {sunrise_hour:02d}:{random.randint(0,59):02d} AM</span>
                <span>🌇 {sunset_hour:02d}:{random.randint(0,59):02d} PM</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Weather alerts (compact)
        alert_tips = [
            "🌡️ High temp today - stay hydrated",
            "🌧️ Monsoon active - carry umbrella",
            "💨 Strong winds - secure items",
            "🌫️ Poor air quality - wear mask"
        ]
        selected_tip = random.choice(alert_tips)
        
        st.markdown(f"""
        <div class='compact-section'>
            <h5 style='margin:0.2em 0;color:#555;font-size:0.9em;'>⚠️ Weather Alert</h5>
            <div style='font-size:0.8em;color:#856404;'>{selected_tip}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Traffic update (compact)
        traffic_updates = [
            "� Normal traffic flow",
            "🟡 Moderate congestion",
            "� Heavy traffic reported",
            "🚌 Metro running on time"
        ]
        selected_traffic = random.choice(traffic_updates)
        
        st.markdown(f"""
        <div class='compact-section'>
            <h5 style='margin:0.2em 0;color:#555;font-size:0.9em;'>🚗 Traffic Status</h5>
            <div style='font-size:0.8em;'>{selected_traffic}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Current time display
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%A, %B %d")
    
    st.markdown(f"""
    <div class='time-display'>
        <span style='font-size:1.2em;font-weight:bold;'>🕒 {current_time}</span>
        <span style='margin-left:2em;font-size:1em;opacity:0.9;'>{current_date}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Emergency services buttons
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🆘 Emergency Services", use_container_width=True):
            st.session_state['show_helplines'] = not st.session_state.get('show_helplines', False)
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.session_state['panic_mode'] = False
            st.session_state['show_helplines'] = False
            st.rerun()

    if st.session_state.get('show_helplines', False):
        st.markdown("""
        <div class='compact-section'>
            <h5 style='color:#d32f2f;text-align:center;margin-bottom:1em;'>🆘 Emergency Contacts</h5>
        </div>
        """, unsafe_allow_html=True)
        
        helplines = [
            ("Women Helpline", "1091"),
            ("Mental Health", "7827170170"),
            ("Police", "100"),
            ("Child Helpline", "1098"),
        ]
        
        col1, col2 = st.columns(2)
        for i, (label, number) in enumerate(helplines):
            wa_msg = "Hello, I need help urgently. Please assist."
            wa_url = f"https://wa.me/91{number}?text={wa_msg.replace(' ', '%20')}"
            
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"""
                <div class='emergency-card'>
                    <div style='font-weight:bold;'>{label}</div>
                    <div style='font-size:1.1em;'>{number} 
                        <a href='{wa_url}' style='margin-left:0.5em;text-decoration:none;'>📲</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if st.button("❌ Close Helplines"):
            st.session_state['show_helplines'] = False
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

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

# Add wishes vault to sidebar
st.sidebar.markdown("---")
with st.sidebar.expander("🔐 Secure Wishes Vault", expanded=False):
    st.markdown("*Your private space for sensitive notes and wishes*")
    show_secure_wishes_vault()

# Main content area
st.markdown("### Your space, your questions — we're listening")

# --- Enhanced Interactive Voice Input UI ---
st.markdown("#### 🎤 Voice Input")

col_voice, col_status = st.columns([2, 8])

with col_voice:
    # Voice input button logic
    voice_button_clicked = False
    
    if st.session_state.get('voice_active', False):
        if st.button('⏹️ Stop Listening', key="stop_voice_btn", use_container_width=True):
            st.session_state['voice_active'] = False
            st.rerun()
    else:
        voice_button_clicked = st.button(
            '🎤 Start Voice Input', 
            help='Click to start voice input with medical term recognition',
            use_container_width=True,
            key="voice_input_btn"
        )

with col_status:
    # Voice input status display
    if st.session_state.get('voice_active', False):
        st.info("🎙️ **LISTENING...** Speak naturally about your health concerns")
    elif st.session_state.get('current_transcript', ''):
        display_text = st.session_state['current_transcript']
        if len(display_text) > 100:
            display_text = display_text[:100] + "..."
        st.success(f"✅ **Voice Input Ready:** \"{display_text}\"")

# Handle voice input
if voice_button_clicked and not st.session_state.get('voice_active', False):
    st.session_state['voice_active'] = True
    st.session_state['current_transcript'] = ""
    st.rerun()

# Voice input processing (when active)
if st.session_state.get('voice_active', False):
    # Show that we're listening
    st.info("🎙️ **LISTENING...** Speak clearly about your health concerns")
    
    # Use interactive voice input for real-time transcription
    with st.spinner('🎧 Processing voice input...'):
        try:
            # Use the interactive voice input function
            spoken_text = get_voice_input_interactive()
            if spoken_text and spoken_text.strip():
                st.session_state['current_transcript'] = spoken_text
                st.session_state['query_text'] = spoken_text
                st.session_state['voice_active'] = False
                st.session_state['auto_submit'] = True
                st.success(f"✅ Voice input complete: \"{spoken_text}\"")
                st.balloons()
                st.rerun()
            else:
                st.session_state['voice_active'] = False
                st.warning("⚠️ No speech detected. Please try again.")
                st.rerun()
        except Exception as e:
            st.session_state['voice_active'] = False
            st.error(f"❌ Voice input error: {str(e)}")
            st.rerun()

# Auto-submit when voice input is complete
if st.session_state.get('auto_submit', False):
    st.session_state['auto_submit'] = False
    final_query = st.session_state.get('current_transcript', '')
    if final_query:
        st.session_state['query_text'] = final_query
        st.success("🎯 Voice input complete! Processing your query...")
        st.balloons()
        # Auto-trigger the AI response
        st.session_state['auto_process'] = True
        st.rerun()

# --- Text Input with Voice Integration ---
st.markdown("#### ✍️ Text Input")

# Create a placeholder for real-time updates
text_placeholder = st.empty()

# Update text area value from voice input
current_text = st.session_state.get('current_transcript', '') or st.session_state.get('query_text', '')

# If voice is active, show live transcript
if st.session_state.get('voice_active', False):
    live_text = st.session_state.get('current_transcript', '')
    query = text_placeholder.text_area(
        "Tell us what's on your mind… (🎙️ Live Voice Input)",
        height=150,
        value=live_text,
        key=f'query_text_area_live_{len(live_text)}',  # Unique key for updates
        help="Voice input is being transcribed here in real-time!"
    )
else:
    query = text_placeholder.text_area(
        "Tell us what's on your mind…",
        height=150,
        placeholder="Example: I'm 8 weeks pregnant and keep feeling dizzy, is this normal?",
        value=current_text,
        key='query_text_area',
        help="You can type here or use voice input above. Voice input will appear here in real-time."
    )

# Age input
age = st.text_input("Your Age (optional)", placeholder="e.g., 25")
if age:
    try:
        age = int(age)
    except:
        st.warning("Please enter age as a number.")
        age = None

# Get the final query text (from voice or manual input)
final_query_text = query or st.session_state.get('current_transcript', '')

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

# Submit button and auto-processing
if st.button("Get Guidance", use_container_width=True) or st.session_state.get('auto_process', False):
    # Reset auto_process flag
    if st.session_state.get('auto_process', False):
        st.session_state['auto_process'] = False
    
    # Use the final query from voice or text input
    final_query = final_query_text
    
    if final_query:
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
            response = ask_shakti_ai(final_query, selected_agents, age)
            
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

# Footer
st.markdown("---")
st.markdown("✨ *SHAKTI-AI: For every woman, every phase, every fight.* ✨")
st.markdown(
    "**Disclaimer:** SHAKTI-AI provides general information only and is not a substitute for professional medical, legal, or mental health advice. "
    "Always consult qualified professionals for specific concerns."
)
