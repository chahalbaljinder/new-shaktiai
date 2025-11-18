import speech_recognition as sr
import re
import threading
import time
import streamlit as st

# Context-aware keywords for government policy terms and APEX agent names
GOVERNMENT_POLICY_TERMS = [
    # Leave Policies
    "maternity leave", "child care leave", "ccl", "paternity leave", "medical leave", 
    "study leave", "earned leave", "casual leave", "compassionate leave",
    
    # Transfer & Posting
    "transfer", "posting", "spouse ground transfer", "hardship posting", 
    "family station transfer", "mutual transfer", "compassionate transfer",
    
    # Legal Rights & Protection
    "posh act", "sexual harassment", "workplace harassment", "gender discrimination",
    "equal opportunity", "women's rights", "legal rights", "grievance", "complaint",
    
    # Career & Promotion
    "promotion", "career progression", "performance appraisal", "project allocation",
    "research opportunities", "leadership positions", "scientist grade",
    
    # Organizations
    "drdo", "isro", "csir", "government", "organization", "department",
    
    # Wellness & Support
    "stress", "anxiety", "burnout", "work life balance", "mental health",
    "counseling", "support", "confidential", "anonymous reporting",
    
    # Documentation & Procedures
    "application", "form", "documentation", "procedure", "workflow", "submission",
    "approval", "policy", "circular", "guidelines", "rules", "regulations"
]

APEX_AGENT_NAMES = [
    # Athena variations
    "athena", "atena", "athina", "policy agent", "procedure agent",
    
    # Asha variations  
    "asha", "asa", "wellness agent", "support agent", "counselor",
    
    # Scribe variations
    "scribe", "scryb", "documentation agent", "workflow agent", "document agent",
    
    # Project names
    "apex", "apeks", "project apex", "apex ai"
]

def get_voice_input():
    """
    Enhanced voice input with context awareness for government policy terms and agent names.
    Returns recognized speech as text with improved accuracy for domain-specific terms.
    """
    recognizer = sr.Recognizer()
    
    # Configure recognizer for better government policy term recognition
    recognizer.energy_threshold = 400
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 3  # Longer pause for policy consultations
    recognizer.phrase_threshold = 3
    
    try:
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1.0)
            print("🎧 Listening for voice input... (speak clearly)")
            
            # Listen with longer timeout for policy consultations
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
            
        try:
            # Try Google Speech Recognition first (better for policy terms)
            text = recognizer.recognize_google(audio)
            print(f"✅ Google Speech Recognition: {text}")
            
        except (sr.UnknownValueError, sr.RequestError):
            try:
                # Fallback to offline Sphinx
                text = recognizer.recognize_sphinx(audio)
                print(f"✅ Sphinx Recognition: {text}")
                
            except (sr.UnknownValueError, sr.RequestError):
                print("❌ Could not understand audio")
                return ""
        
        # Post-process for government context and APEX agent names
        enhanced_text = enhance_government_context(text)
        return enhanced_text.strip()
        
    except sr.WaitTimeoutError:
        print("⏰ No speech detected within timeout")
        return ""
    except Exception as e:
        print(f"❌ Error: {e}")
        return ""

def enhance_government_context(text):
    """
    Enhance recognized text with government policy term corrections and APEX agent name recognition.
    """
    if not text:
        return text
    
    text_lower = text.lower()
    enhanced = text
    
    # Fix common APEX agent name misrecognitions
    agent_corrections = {
        # Athena variations
        "atena": "Athena",
        "athina": "Athena", 
        "athena": "Athena",
        "policy agent": "Athena",
        "procedure agent": "Athena",
        
        # Asha variations
        "asa": "Asha",
        "asha": "Asha",
        "wellness agent": "Asha",
        "support agent": "Asha",
        "counselor": "Asha",
        
        # Scribe variations
        "scryb": "Scribe",
        "scribe": "Scribe", 
        "documentation agent": "Scribe",
        "workflow agent": "Scribe",
        "document agent": "Scribe",
        
        # Project names
        "apeks": "Apex",
        "apex": "Apex",
        "project apex": "Project Apex",
        "apex ai": "APEX-AI"
    }
    
    for incorrect, correct in agent_corrections.items():
        pattern = r'\b' + re.escape(incorrect) + r'\b'
        enhanced = re.sub(pattern, correct, enhanced, flags=re.IGNORECASE)
    
    # Fix common government policy term misrecognitions
    policy_corrections = {
        # Leave Policies
        "matarnity": "maternity",
        "maternaty": "maternity",
        "ccell": "CCL",
        "ccl": "CCL",
        "paternaty": "paternity",
        "medicol": "medical",
        "compassionet": "compassionate",
        
        # Transfer & Posting
        "transfere": "transfer",
        "posteng": "posting",
        "hardshep": "hardship",
        "mutal": "mutual",
        
        # Legal Rights & Protection
        "posh": "POSH",
        "harrasment": "harassment",
        "harrassment": "harassment",
        "discriminashun": "discrimination",
        "greevance": "grievance",
        "greevans": "grievance",
        "complent": "complaint",
        "complaing": "complaint",
        
        # Career & Promotion
        "promoshun": "promotion",
        "progreshun": "progression",
        "appraisel": "appraisal",
        "allocashun": "allocation",
        "oppertunity": "opportunity",
        "ledarship": "leadership",
        "scientest": "scientist",
        
        # Organizations
        "drdo": "DRDO",
        "isro": "ISRO",
        "csir": "CSIR",
        "goverment": "government",
        "govarnment": "government",
        "organistion": "organization",
        "departmant": "department",
        
        # Wellness & Support
        "anxiaty": "anxiety",
        "burnot": "burnout",
        "counsoling": "counseling",
        "counceling": "counseling",
        "confedential": "confidential",
        "anonimous": "anonymous",
        "mentol": "mental",
        
        # Documentation & Procedures
        "aplicashun": "application",
        "documantation": "documentation",
        "proceedure": "procedure",
        "workflo": "workflow",
        "submision": "submission",
        "aproval": "approval",
        "circuler": "circular",
        "gydelines": "guidelines",
        "regulashuns": "regulations",
        "statatory": "statutory",
        "complience": "compliance"
    }
    
    for incorrect, correct in policy_corrections.items():
        pattern = r'\b' + re.escape(incorrect) + r'\b'
        enhanced = re.sub(pattern, correct, enhanced, flags=re.IGNORECASE)
    
    return enhanced

def get_voice_input_interactive():
    """
    Interactive voice input with real-time transcription and auto-search.
    Updates text field in real-time as user speaks.
    """
    recognizer = sr.Recognizer()
    
    # Configure for real-time recognition
    recognizer.energy_threshold = 300  # Lower for responsiveness
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1.5   # Longer pause before considering speech done
    recognizer.phrase_threshold = 0.2  # Shorter for faster response
    
    # Initialize session state for real-time updates
    if 'voice_active' not in st.session_state:
        st.session_state['voice_active'] = False
    if 'current_transcript' not in st.session_state:
        st.session_state['current_transcript'] = ""
    if 'auto_submit' not in st.session_state:
        st.session_state['auto_submit'] = False
    
    try:
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("🎧 Starting interactive listening... (speak naturally)")
            
            st.session_state['voice_active'] = True
            st.session_state['current_transcript'] = ""
            
            # Real-time listening loop
            accumulated_text = ""
            silence_count = 0
            
            while st.session_state['voice_active'] and silence_count < 3:
                try:
                    # Listen for short phrases
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=4)
                    
                    # Try to recognize immediately
                    try:
                        # Quick recognition for real-time feedback
                        partial_text = recognizer.recognize_google(audio, language='en-IN')
                        
                        if partial_text.strip():
                            # Enhance the partial text
                            enhanced_partial = enhance_government_context(partial_text)
                            
                            # Accumulate text
                            if accumulated_text:
                                accumulated_text += " " + enhanced_partial
                            else:
                                accumulated_text = enhanced_partial
                            
                            # Update session state for real-time display
                            st.session_state['current_transcript'] = accumulated_text
                            print(f"📝 Real-time: {accumulated_text}")
                            
                            # Reset silence counter
                            silence_count = 0
                        
                    except (sr.UnknownValueError, sr.RequestError):
                        # No speech detected
                        silence_count += 1
                        print(f"🔇 Silence {silence_count}/3")
                
                except sr.WaitTimeoutError:
                    # Timeout - increment silence counter
                    silence_count += 1
                    print(f"⏰ Timeout {silence_count}/3")
            
            # Finalize the transcript
            final_text = accumulated_text.strip()
            if final_text:
                st.session_state['current_transcript'] = final_text
                st.session_state['auto_submit'] = True
                print(f"✅ Final transcript: {final_text}")
                return final_text
            else:
                print("❌ No speech detected")
                return ""
                
    except Exception as e:
        print(f"❌ Voice input error: {e}")
        return ""
    
    finally:
        st.session_state['voice_active'] = False
