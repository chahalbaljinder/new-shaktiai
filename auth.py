import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Utility Functions ---
def sign_up(username: str, email: str, password: str):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        # If signup is successful, insert username into profiles table
        if user and getattr(user, 'user', None) and hasattr(user.user, 'id'):
            user_id = user.user.id
            # Insert username and email into profiles table
            data, error = supabase.table("profiles").insert({"id": user_id, "username": username, "email": email}).execute()
            if error:
                st.warning(f"Profile creation warning: {error.message}")
        return user
    except Exception as e:
        st.error(f"Error signing up: {e}")
        return None

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.pop('user', None)
        st.success("Successfully signed out.")
        st.rerun()
    except Exception as e:
        st.error(f"Error signing out: {e}")

# --- Main App for Authenticated Users ---
def main_app(user_email: str):
    # Fetch username from profiles table using user_email
    username = None
    try:
        response = supabase.table("profiles").select("username").eq("email", user_email).single().execute()
        if response and hasattr(response, 'data') and response.data:
            username = response.data.get("username")
    except Exception as e:
        st.warning(f"Could not fetch username: {e}")
    display_name = username if username else user_email
    st.markdown(f"""
    <style>
    .main-app-container {{
        max-width: 500px;
        margin: 2em auto;
        background: linear-gradient(135deg, #ffe0ef 0%, #f8f9fa 100%);
        border-radius: 18px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.10);
        padding: 2.5em 2em 2em 2em;
        text-align: center;
    }}
    .main-app-container h2 {{
        color: #c9184a;
        margin-bottom: 0.5em;
    }}
    .main-app-container .user-email {{
        color: #6c757d;
        font-size: 1.1em;
        margin-bottom: 1.5em;
    }}
    .main-app-container .signout-btn button {{
        background: linear-gradient(45deg, #f783ac, #d6336c) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.5em 1.5em !important;
        margin-top: 1em;
        transition: all 0.3s ease !important;
    }}
    .main-app-container .signout-btn button:hover {{
        background: linear-gradient(45deg, #d6336c, #f783ac) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(247, 131, 172, 0.3) !important;
    }}
    </style>
    <div class="main-app-container">
        <h2>Welcome to SHAKTI-AI</h2>
        <div class="user-email">Hello, <b>{display_name}</b>!</div>
        <div>This is your secure, personalized area.<br>All your wishes and data will be stored privately.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Sign Out", key="signout_btn", help="Sign out and return to login."):
        sign_out()

# --- Auth UI ---
def auth_screen():
    st.set_page_config(
        page_title="SHAKTI-AI Login",
        page_icon="🧬",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    st.markdown("""
    <style>
    .auth-container {
        max-width: 420px;
        margin: 2em auto;
        background: linear-gradient(135deg, #ffe0ef 0%, #f8f9fa 100%);
        border-radius: 18px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.10);
        padding: 2.5em 2em 2em 2em;
    }
    .auth-title {
        color: #c9184a;
        font-size: 2em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1.2em;
    }
    .stTextInput > div > input, .stTextInput input {
        border: 2px solid #f783ac;
        border-radius: 8px;
    }
    .stButton > button {
        background: linear-gradient(45deg, #f783ac, #d6336c) !important;
        color: #fff !important;
        border-radius: 12px !important;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        margin-top: 0.5em;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #d6336c, #f783ac) !important;
        transform: translateY(-2px);
    }
    .switch-link {
        color: #d6336c;
        font-size: 0.98em;
        text-align: center;
        margin-top: 1.2em;
        cursor: pointer;
        text-decoration: underline;
    }
    </style>
    <div class="auth-container">
        <div class="auth-title">SHAKTI-AI Login</div>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.get('user')
    if user and getattr(user, 'user', None) and getattr(user, 'error', None) is None and hasattr(user.user, 'email'):
        # Supabase AuthResponse object: user.user is a User object, user.error is error
        email = user.user.email
        main_app(email)
        return

    # --- Login/Signup Tabs ---
    tabs = st.tabs(["Login", "Sign Up"])
    with tabs[0]:
        st.subheader(":lock: Login to your account")
        with st.form("login_form"):
            user_input = st.text_input("Username or Email", key="login_user_input", placeholder="Enter your username or email")
            password = st.text_input("Password", type="password", key="login_password")
            submit_button = st.form_submit_button("Login")
            if submit_button:
                try:
                    # Determine if input is email or username
                    if "@" in user_input and "." in user_input:
                        # Looks like an email
                        email = user_input.strip()
                    else:
                        # Looks like a username, look up email
                        response = supabase.table("profiles").select("email").eq("username", user_input.strip()).single().execute()
                        if not response or not hasattr(response, 'data') or not response.data or not response.data.get("email"):
                            st.warning("No account found with that username. Please check your username or sign up.")
                            return
                        email = response.data["email"]
                    # Try to sign in with email and password
                    user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    if getattr(user, 'error', None):
                        # Friendly error messages
                        msg = user.error.message.lower()
                        if "invalid login credentials" in msg or "invalid password" in msg:
                            st.warning("Incorrect password. Please try again or reset your password if you've forgotten it.")
                        elif "email not confirmed" in msg:
                            st.warning("Please confirm your email before logging in. Check your inbox for a confirmation link.")
                        else:
                            st.warning("Login failed. Please check your credentials and try again.")
                    elif user and getattr(user, 'user', None) and hasattr(user.user, 'email'):
                        st.session_state['user'] = user
                        st.success("Login successful! Reloading...")
                        st.rerun()
                    else:
                        st.warning("Login failed. Please check your credentials and try again.")
                except Exception as e:
                    st.warning("Unable to log in. Please check your credentials and try again.")

    with tabs[1]:
        st.subheader(":sparkles: Create a new account")
        with st.form("signup_form"):
            signup_username = st.text_input("Username", key="signup_username")
            signup_email = st.text_input("Email", key="signup_email")
            signup_password = st.text_input("Password", type="password", key="signup_password")
            signup_button = st.form_submit_button("Sign Up")
            if signup_button:
                if not signup_username:
                    st.error("Username is required.")
                else:
                    try:
                        # Check if username already exists (use maybe_single to avoid error)
                        response = supabase.table("profiles").select("id").eq("username", signup_username).maybe_single().execute()
                        if response and hasattr(response, 'data') and response.data:
                            st.warning("That username is already taken. Please choose another username.")
                        else:
                            user = sign_up(signup_username, signup_email, signup_password)
                            if user and getattr(user, 'user', None):
                                st.success("Sign up successful! Please check your email and confirm your account before logging in.")
                            elif getattr(user, 'error', None):
                                st.warning(user.error.message)
                            else:
                                st.warning("Sign up failed. Please try again.")
                    except Exception as e:
                        st.warning("Unable to sign up. Please try again or contact support if the problem persists.")

if __name__ == "__main__":
    auth_screen()