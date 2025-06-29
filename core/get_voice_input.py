import speech_recognition as sr
import re
import threading
import time
import streamlit as st

# Context-aware keywords for medical terms and agent names
MEDICAL_TERMS = [
    "pregnancy", "pregnant", "menstruation", "periods", "contraception", "abortion",
    "menopause", "hormones", "bleeding", "pain", "cramps", "nausea", "dizzy", "fever",
    "delivery", "childbirth", "breastfeeding", "lactation", "ovulation", "fertility",
    "pcos", "endometriosis", "fibroids", "cysts", "infection", "discharge", "spotting",
    "mood", "depression", "anxiety", "stress", "trauma", "abuse", "violence",
    "legal", "rights", "consent", "marriage", "divorce", "domestic", "harassment"
]

AGENT_NAMES = [
    "maaya", "maya", "maa", "gynika", "gyneka", "meher", "mehir", 
    "nyaya", "nyya", "vaanya", "vanya", "shakti", "shakti ai"
]

def get_voice_input():
    """
    Enhanced voice input with context awareness for medical terms and agent names.
    Returns recognized speech as text with improved accuracy for domain-specific terms.
    """
    recognizer = sr.Recognizer()
    
    # Configure recognizer for better medical term recognition
    recognizer.energy_threshold = 400
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 3  # Longer pause for medical consultations
    recognizer.phrase_threshold = 3
    
    try:
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1.0)
            print("🎧 Listening for voice input... (speak clearly)")
            
            # Listen with longer timeout for medical consultations
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
            
        try:
            # Try Google Speech Recognition first (better for medical terms)
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
        
        # Post-process for medical context and agent names
        enhanced_text = enhance_medical_context(text)
        return enhanced_text.strip()
        
    except sr.WaitTimeoutError:
        print("⏰ No speech detected within timeout")
        return ""
    except Exception as e:
        print(f"❌ Error: {e}")
        return ""

def enhance_medical_context(text):
    """
    Enhance recognized text with medical term corrections and agent name recognition.
    """
    if not text:
        return text
    
    text_lower = text.lower()
    enhanced = text
    
    # Fix common agent name misrecognitions
    agent_corrections = {
        "maya": "Maaya",
        "maa": "Maaya", 
        "maia": "Maaya",
        "gyneka": "Gynika",
        "genika": "Gynika",
        "mehir": "Meher",
        "meer": "Meher",
        "nyya": "Nyaya",
        "naya": "Nyaya",
        "vanya": "Vaanya",
        "vania": "Vaanya",
        "shakti ai": "SHAKTI-AI",
        "shakthi": "SHAKTI"
    }
    
    for incorrect, correct in agent_corrections.items():
        pattern = r'\b' + re.escape(incorrect) + r'\b'
        enhanced = re.sub(pattern, correct, enhanced, flags=re.IGNORECASE)
    
    # Fix common medical term misrecognitions
    medical_corrections = {
        "pregency": "pregnancy",
        "pregant": "pregnant",
        "menstration": "menstruation",
        "periode": "periods",
        "contraceptive": "contraception",
        "menapose": "menopause",
        "hormons": "hormones",
        "bledding": "bleeding",
        "nausia": "nausea",
        "dizy": "dizzy",
        "breastfeding": "breastfeeding",
        "ovulaion": "ovulation",
        "fertillity": "fertility",
        "anxiaty": "anxiety",
        "harrasment": "harassment"
    }
    
    for incorrect, correct in medical_corrections.items():
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
                            enhanced_partial = enhance_medical_context(partial_text)
                            
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
