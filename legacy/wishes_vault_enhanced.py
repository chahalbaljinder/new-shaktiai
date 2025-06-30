from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import streamlit as st
import os
import urllib.parse
import yagmail
import pywhatkit
import phonenumbers
import re
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import random

_VAULT_DIR = os.path.dirname(os.path.abspath(__file__))
WISHES_FILE = os.path.join(_VAULT_DIR, "wishes.enc")
KEY_FILE = os.path.join(_VAULT_DIR, "wishes.key")

def _get_fernet():
    if 'wishes_key' not in st.session_state:
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(KEY_FILE, 'wb') as f:
                f.write(key)
        st.session_state['wishes_key'] = key
    return Fernet(st.session_state['wishes_key'])

def _load_encrypted():
    if os.path.exists(WISHES_FILE):
        with open(WISHES_FILE, 'rb') as f:
            return f.read()
    return None

def _save_encrypted(data):
    with open(WISHES_FILE, 'wb') as f:
        f.write(data)

def _delete_encrypted():
    if os.path.exists(WISHES_FILE):
        os.remove(WISHES_FILE)

def _decrypt_wishes():
    f = _get_fernet()
    enc = _load_encrypted()
    if enc:
        try:
            return f.decrypt(enc).decode('utf-8')
        except Exception:
            return None
    return None

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone, country_code='IN'):
    """Validate phone number format."""
    try:
        parsed = phonenumbers.parse(phone, country_code)
        return phonenumbers.is_valid_number(parsed)
    except:
        return False

def format_phone_for_whatsapp(phone, country_code='IN'):
    """Format phone number for WhatsApp."""
    try:
        parsed = phonenumbers.parse(phone, country_code)
        return f"+{parsed.country_code}{parsed.national_number}"
    except:
        return None

def send_email_share(wishes_text, recipient_email, sender_name="SHAKTI-AI User"):
    """Send wishes via email using yagmail."""
    try:
        # Note: Configure with actual email credentials
        yag = yagmail.SMTP('your_email@gmail.com', 'your_app_password')
        
        subject = f"Shared Message from {sender_name} via SHAKTI-AI"
        body = f"""Hello,

Someone has shared a message with you through SHAKTI-AI's secure sharing feature:

---
{wishes_text}
---

Shared on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

SHAKTI-AI - Women's Health & Rights Support
"""
        
        yag.send(recipient_email, subject, body)
        return True
        
    except Exception as e:
        st.error(f"Email failed: {e}")
        return False

def send_whatsapp_share(wishes_text, phone_number, sender_name="SHAKTI-AI User"):
    """Send wishes via WhatsApp using pywhatkit."""
    try:
        formatted_phone = format_phone_for_whatsapp(phone_number)
        if not formatted_phone:
            return False
        
        message = f"""*Message from {sender_name} via SHAKTI-AI*

{wishes_text}

_Shared on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}_

*SHAKTI-AI* - Women's Health & Rights Support"""
        
        pywhatkit.sendwhatmsg_instantly(formatted_phone, message, wait_time=10, tab_close=True)
        return True
        
    except Exception as e:
        st.error(f"WhatsApp failed: {e}")
        return False

def share_via_email(wishes_text, contact_email, sender_email=None, sender_password=None):
    """Share wishes via email."""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email or "shakti.ai.wishes@gmail.com"
        msg['To'] = contact_email
        msg['Subject'] = "🌟 Important Message from SHAKTI-AI Wishes Vault"
        
        # Email body
        body = f"""
Dear Friend,

I wanted to share something important with you through SHAKTI-AI's secure wishes vault.

My wishes and thoughts:
{wishes_text}

This message was sent securely through SHAKTI-AI, a platform that supports women's health and well-being.

With care,
Your trusted contact

---
SHAKTI-AI: For every woman, every phase, every fight.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Gmail SMTP configuration (you can make this configurable)
        if sender_email and sender_password:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, contact_email, text)
            server.quit()
            return True
        else:
            # For demo purposes, just show the email content
            st.info("Email sharing configured. Message ready to send.")
            return True
            
    except Exception as e:
        st.error(f"Email sending failed: {e}")
        return False

def share_via_whatsapp(wishes_text, contact_phone):
    """Generate WhatsApp sharing link."""
    message = f"""🌟 Important Message from SHAKTI-AI Wishes Vault

My wishes and thoughts:
{wishes_text}

This message was sent securely through SHAKTI-AI, a platform that supports women's health and well-being.

With care ❤️"""
    
    # Format phone number (remove spaces, dashes)
    phone = ''.join(filter(str.isdigit, contact_phone))
    if not phone.startswith('91') and len(phone) == 10:
        phone = '91' + phone  # Add India country code
    
    # URL encode the message
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/{phone}?text={encoded_message}"
    
    return whatsapp_url

def show_secure_wishes_vault(neutral_mode=False):
    wishes_released = False
    safe_word_triggered = False

    for v in st.session_state.values():
        if isinstance(v, str) and "SAFE RELEASE" in v.upper():
            wishes_released = True
            safe_word_triggered = True
            break

    box_style = "background:#f8f9fa;padding:1em;border-radius:8px;margin:1em 0;" if not neutral_mode else "background:#f3f3f3;padding:0.7em 0.7em 0.2em 0.7em;border-radius:8px;margin:1em 0;box-shadow:0 1px 4px #0001;"
    with st.container():
        st.markdown(f"<div style='{box_style}'>", unsafe_allow_html=True)
        st.markdown("#### 🔒 Wishes Vault" if not neutral_mode else "<span style='color:#888;font-size:1.1em;'>🔒 Safe Wishes Box</span>", unsafe_allow_html=True)
        st.caption("Write your wishes, save, and they will stay hidden until released.")

        enc = _load_encrypted()
        wishes = None
        contact = None
        if enc:
            try:
                dec = _get_fernet().decrypt(enc).decode('utf-8')
                wishes_data = dec.split('\n---CONTACT---\n')
                wishes = wishes_data[0]
                contact = wishes_data[1] if len(wishes_data) > 1 else ""
            except Exception as e:
                wishes = None
                contact = None
                st.error(f"Decryption error: {e}")

        # Use session_state for form fields
        if 'wishes_input' not in st.session_state:
            st.session_state['wishes_input'] = wishes or ""
        if 'contact_name' not in st.session_state:
            st.session_state['contact_name'] = "" if not contact else contact.split('|')[0]
        if 'contact_info' not in st.session_state:
            st.session_state['contact_info'] = "" if not contact else (contact.split('|')[1] if '|' in contact else "")

        show_form = not enc or st.session_state.get('show_wishes_form', False)
        if show_form:
            with st.form("wishes_form", clear_on_submit=True):
                wishes_input = st.text_area("Your wishes (kept private & secure)", value=st.session_state['wishes_input'], key='wishes_input', height=120)
                
                st.markdown("##### 📱 Trusted Contact Information")
                contact_name = st.text_input("Trusted contact name (optional)", value=st.session_state['contact_name'], key='contact_name')
                contact_info = st.text_input("Contact email or phone (for sharing)", value=st.session_state['contact_info'], key='contact_info', 
                                           help="Enter email address or phone number for sharing wishes")
                
                submitted = st.form_submit_button("Save Wishes Securely")
                if submitted:
                    try:
                        f = _get_fernet()
                        contact_str = f"{contact_name}|{contact_info}" if contact_name or contact_info else ""
                        data = wishes_input.strip() + "\n---CONTACT---\n" + contact_str
                        enc = f.encrypt(data.encode('utf-8'))
                        _save_encrypted(enc)
                        st.session_state['show_wishes_form'] = False
                        st.success("✅ Wishes saved securely!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Encryption error: {e}")
        else:
            if wishes:
                st.markdown(f"**Your wishes:**<br><span style='color:#444'>{wishes}</span>", unsafe_allow_html=True)
            if contact:
                contact_parts = contact.split('|')
                contact_name = contact_parts[0] if len(contact_parts) > 0 else ""
                contact_info = contact_parts[1] if len(contact_parts) > 1 else ""
                st.caption(f"Trusted contact: {contact_name} ({contact_info})")
                
                # Enhanced sharing functionality with Email and WhatsApp
                if wishes and contact_info:
                    st.markdown("##### 📤 Share Wishes")
                    
                    # Sharing method selection
                    share_method = st.radio(
                        "Choose sharing method:",
                        ["📧 Email", "📱 WhatsApp"],
                        horizontal=True,
                        key="share_method_radio"
                    )
                    
                    if share_method == "📧 Email":
                        st.markdown("**Email Sharing**")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            recipient_email = st.text_input("Recipient's Email", 
                                                          value=contact_info if '@' in contact_info else "",
                                                          placeholder="friend@example.com")
                        with col2:
                            sender_name = st.text_input("Your Name (optional)", 
                                                       value=st.session_state.get('contact_name', ''),
                                                       placeholder="Your Name")
                        
                        if st.button("📧 Send Email", use_container_width=True):
                            if not recipient_email:
                                st.error("❌ Please enter recipient's email")
                            elif not validate_email(recipient_email):
                                st.error("❌ Please enter a valid email address")
                            else:
                                sender = sender_name if sender_name else "SHAKTI-AI User"
                                with st.spinner("📧 Sending email..."):
                                    if send_email_share(wishes, recipient_email, sender):
                                        st.success(f"✅ Email sent to {recipient_email}!")
                                        st.balloons()
                                    else:
                                        st.error("❌ Email configuration needed. Please set up email credentials.")
                    
                    elif share_method == "📱 WhatsApp":
                        st.markdown("**WhatsApp Sharing**")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            recipient_phone = st.text_input("Recipient's Phone", 
                                                          value=contact_info if contact_info.replace('+', '').replace('-', '').replace(' ', '').isdigit() else "",
                                                          placeholder="+91XXXXXXXXXX")
                        with col2:
                            sender_name = st.text_input("Your Name (optional)", 
                                                       value=st.session_state.get('contact_name', ''),
                                                       placeholder="Your Name",
                                                       key="wa_sender_name")
                        
                        if st.button("� Send WhatsApp", use_container_width=True):
                            if not recipient_phone:
                                st.error("❌ Please enter recipient's phone number")
                            elif not validate_phone(recipient_phone):
                                st.error("❌ Please enter a valid phone number")
                            else:
                                sender = sender_name if sender_name else "SHAKTI-AI User"
                                with st.spinner("� Opening WhatsApp..."):
                                    if send_whatsapp_share(wishes, recipient_phone, sender):
                                        st.success("✅ WhatsApp opened with your message!")
                                        st.info("💡 Complete the sending in the WhatsApp window that opened.")
                                    else:
                                        st.error("❌ WhatsApp sharing failed. Check phone number format.")
                    
                    # Privacy notice
                    st.info("� **Privacy**: Messages are shared directly. SHAKTI-AI doesn't store shared content.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Edit Wishes", key="edit_wishes_btn"):
                    st.session_state['show_wishes_form'] = True
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete Wishes", key="delete_wishes_btn"):
                    _delete_encrypted()
                    st.session_state['wishes_input'] = ""
                    st.session_state['contact_name'] = ""
                    st.session_state['contact_info'] = ""
                    st.session_state['show_wishes_form'] = True
                    st.success("🗑️ Wishes deleted.")
                    st.rerun()
                    
        st.markdown("</div>", unsafe_allow_html=True)
