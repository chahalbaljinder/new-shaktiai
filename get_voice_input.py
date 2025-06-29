import speech_recognition as sr

def get_voice_input():
    """
    Listens to the user's microphone and returns recognized speech as text using pocketsphinx (offline).
    Returns an empty string if no speech is detected or audio is unintelligible.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            # Optionally, adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening for voice input...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        try:
            text = recognizer.recognize_sphinx(audio)
            return text.strip()
        except sr.UnknownValueError:
            # Speech was unintelligible
            return ""
        except sr.RequestError:
            # Sphinx is not available or another error
            return ""
    except Exception:
        # Microphone not available or no speech detected in time
        return ""
