"""
Enhanced Wishes Vault with PostgreSQL Database Integration
This module provides a secure wishes vault using PostgreSQL database backend.
"""

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
from datetime import datetime, timedelta
import random
from .db_config import wishes_db

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format."""
    try:
        parsed = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed)
    except:
        return False

def send_email_share(wishes_text, recipient_email, sender_name="SHAKTI-AI User"):
    """Send wishes via email using Gmail SMTP."""
    try:
        # Create email content
        subject = f"Shared Wishes from {sender_name}"
        body = f"""
Dear Friend,

{sender_name} has shared their wishes with you through SHAKTI-AI:

---
{wishes_text}
---

This message was sent securely through SHAKTI-AI's Wishes Vault.

With warm regards,
SHAKTI-AI Team
        """.strip()

        # Try to use system's default email client
        mailto_url = f"mailto:{recipient_email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        
        st.markdown(f'<a href="{mailto_url}" target="_blank">Click here to open your email client</a>', unsafe_allow_html=True)
        return True
        
    except Exception as e:
        st.error(f"Email sharing error: {e}")
        return False

def send_whatsapp_share(wishes_text, phone_number, sender_name="SHAKTI-AI User"):
    """Send wishes via WhatsApp."""
    try:
        # Format phone number
        if not phone_number.startswith('+'):
            if phone_number.startswith('91') and len(phone_number) == 12:
                phone_number = '+' + phone_number
            elif len(phone_number) == 10:
                phone_number = '+91' + phone_number
            else:
                phone_number = '+' + phone_number

        # Create WhatsApp message
        message = f"""Hi! {sender_name} has shared their wishes with you through SHAKTI-AI:

---
{wishes_text}
---

Sent securely via SHAKTI-AI Wishes Vault 💜"""

        # Open WhatsApp Web with pre-filled message
        pywhatkit.sendwhatmsg_instantly(phone_number, message, wait_time=2, tab_close=False)
        return True
        
    except Exception as e:
        st.error(f"WhatsApp sharing error: {e}")
        return False

def get_user_id():
    """Get or create a user ID for the current session."""
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = f"user_{random.randint(1000, 9999)}_{datetime.now().strftime('%Y%m%d')}"
    return st.session_state['user_id']

def show_secure_wishes_vault(neutral_mode=False):
    """Enhanced wishes vault with PostgreSQL database backend."""
    
    # Initialize database
    if not wishes_db.init_database():
        st.error("⚠️ Database connection failed. Please check your PostgreSQL configuration.")
        return
    
    user_id = get_user_id()
    wishes_released = False
    safe_word_triggered = False

    # Check for safe word trigger
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

        # Get user's wishes from database
        user_wishes = wishes_db.get_wishes(user_id, limit=1)
        current_wish = user_wishes[0] if user_wishes else None
        
        # Initialize session state
        if 'show_wishes_form' not in st.session_state:
            st.session_state['show_wishes_form'] = current_wish is None
        
        # Initialize or refresh form fields with current wish data
        if current_wish:
            # Always update session state with current wish data when available
            st.session_state['wishes_input'] = current_wish['content'] or ""
            st.session_state['contact_name'] = current_wish['contact_name'] or ""
            st.session_state['contact_email'] = current_wish['contact_email'] or ""
            st.session_state['contact_phone'] = current_wish['contact_phone'] or ""
            st.session_state['contact_relationship'] = current_wish['contact_relationship'] or ""
        else:
            # Initialize with empty values if no current wish
            if 'wishes_input' not in st.session_state:
                st.session_state['wishes_input'] = ""
            if 'contact_name' not in st.session_state:
                st.session_state['contact_name'] = ""
            if 'contact_email' not in st.session_state:
                st.session_state['contact_email'] = ""
            if 'contact_phone' not in st.session_state:
                st.session_state['contact_phone'] = ""
            if 'contact_relationship' not in st.session_state:
                st.session_state['contact_relationship'] = ""

        show_form = st.session_state.get('show_wishes_form', False)
        
        if show_form:
            with st.form("wishes_form", clear_on_submit=False):
                wishes_input = st.text_area(
                    "Your wishes (kept private & secure)", 
                    value=st.session_state['wishes_input'], 
                    height=120,
                    placeholder="Write your deepest wishes, dreams, and thoughts here..."
                )
                
                st.markdown("##### 📱 Trusted Contact Information")
                
                col1, col2 = st.columns(2)
                with col1:
                    contact_name = st.text_input(
                        "Trusted contact name", 
                        value=st.session_state['contact_name'],
                        placeholder="e.g., Best Friend, Partner, Family"
                    )
                    contact_email = st.text_input(
                        "Contact email", 
                        value=st.session_state['contact_email'],
                        placeholder="contact@example.com"
                    )
                
                with col2:
                    contact_phone = st.text_input(
                        "Contact phone", 
                        value=st.session_state['contact_phone'],
                        placeholder="+91XXXXXXXXXX"
                    )
                    contact_relationship = st.text_input(
                        "Relationship", 
                        value=st.session_state['contact_relationship'],
                        placeholder="e.g., Sister, Best Friend, Partner"
                    )
                
                # Sharing preferences
                st.markdown("##### ⚙️ Sharing Preferences")
                auto_share = st.checkbox("Enable automatic sharing in emergency", value=False)
                share_method_pref = st.selectbox(
                    "Preferred sharing method",
                    ["Email", "WhatsApp", "Both"],
                    index=0
                )
                
                submitted = st.form_submit_button("💾 Save Wishes Securely", use_container_width=True)
                
                if submitted:
                    if not wishes_input.strip():
                        st.error("⚠️ Please enter your wishes before saving.")
                    else:
                        try:
                            sharing_preferences = {
                                "auto_share": auto_share,
                                "preferred_method": share_method_pref
                            }
                            
                            if current_wish:
                                # Update existing wish
                                success = wishes_db.update_wish(
                                    wish_id=current_wish['id'],
                                    user_id=user_id,
                                    content=wishes_input.strip(),
                                    contact_name=contact_name.strip() if contact_name else None,
                                    contact_email=contact_email.strip() if contact_email else None,
                                    contact_phone=contact_phone.strip() if contact_phone else None,
                                    contact_relationship=contact_relationship.strip() if contact_relationship else None,
                                    sharing_preferences=sharing_preferences
                                )
                                if success:
                                    st.success("✅ Wishes updated securely!")
                                else:
                                    st.error("❌ Failed to update wishes.")
                            else:
                                # Create new wish
                                wish_id = wishes_db.save_wish(
                                    user_id=user_id,
                                    content=wishes_input.strip(),
                                    contact_name=contact_name.strip() if contact_name else None,
                                    contact_email=contact_email.strip() if contact_email else None,
                                    contact_phone=contact_phone.strip() if contact_phone else None,
                                    contact_relationship=contact_relationship.strip() if contact_relationship else None,
                                    sharing_preferences=sharing_preferences
                                )
                                if wish_id:
                                    st.success("✅ Wishes saved securely!")
                                    current_wish = {"id": wish_id}
                                else:
                                    st.error("❌ Failed to save wishes.")
                            
                            if current_wish:
                                st.session_state['show_wishes_form'] = False
                                st.rerun()
                                
                        except Exception as e:
                            st.error(f"❌ Error saving wishes: {e}")
        
        else:
            # Display existing wishes
            if current_wish:
                st.markdown("**Your wishes:**")
                st.markdown(f"<div style='background:#f8f9fa;padding:1em;border-radius:8px;border-left:4px solid #007bff;'>{current_wish['content']}</div>", unsafe_allow_html=True)
                
                # Display contact information
                if current_wish.get('contact_name') or current_wish.get('contact_email') or current_wish.get('contact_phone'):
                    st.markdown("**Trusted Contact:**")
                    contact_info = []
                    if current_wish.get('contact_name'):
                        contact_info.append(f"👤 **{current_wish['contact_name']}**")
                    if current_wish.get('contact_relationship'):
                        contact_info.append(f"({current_wish['contact_relationship']})")
                    if current_wish.get('contact_email'):
                        contact_info.append(f"📧 {current_wish['contact_email']}")
                    if current_wish.get('contact_phone'):
                        contact_info.append(f"📱 {current_wish['contact_phone']}")
                    
                    st.markdown(" • ".join(contact_info))
                
                # Enhanced sharing functionality
                if current_wish.get('contact_email') or current_wish.get('contact_phone'):
                    st.markdown("---")
                    st.markdown("##### 📤 Share Wishes")
                    
                    # Sharing method selection
                    share_methods = []
                    if current_wish.get('contact_email'):
                        share_methods.append("📧 Email")
                    if current_wish.get('contact_phone'):
                        share_methods.append("📱 WhatsApp")
                    
                    if len(share_methods) > 1:
                        share_method = st.radio(
                            "Choose sharing method:",
                            share_methods,
                            horizontal=True,
                            key="share_method_radio"
                        )
                    else:
                        share_method = share_methods[0] if share_methods else None
                    
                    if share_method == "📧 Email" and current_wish.get('contact_email'):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.text_input("Recipient's Email", value=current_wish['contact_email'], disabled=True)
                        with col2:
                            if st.button("📧 Send Email", use_container_width=True):
                                sender_name = current_wish.get('contact_name', 'SHAKTI-AI User')
                                with st.spinner("📧 Preparing email..."):
                                    if send_email_share(current_wish['content'], current_wish['contact_email'], sender_name):
                                        # Log sharing activity
                                        wishes_db.log_sharing(
                                            wish_id=current_wish['id'],
                                            shared_with=current_wish['contact_email'],
                                            sharing_method='email',
                                            status='initiated'
                                        )
                                        st.success(f"✅ Email client opened for {current_wish['contact_email']}!")
                                        st.balloons()
                    
                    elif share_method == "📱 WhatsApp" and current_wish.get('contact_phone'):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.text_input("Recipient's Phone", value=current_wish['contact_phone'], disabled=True)
                        with col2:
                            if st.button("📱 Send WhatsApp", use_container_width=True):
                                sender_name = current_wish.get('contact_name', 'SHAKTI-AI User')
                                with st.spinner("📱 Opening WhatsApp..."):
                                    if send_whatsapp_share(current_wish['content'], current_wish['contact_phone'], sender_name):
                                        # Log sharing activity
                                        wishes_db.log_sharing(
                                            wish_id=current_wish['id'],
                                            shared_with=current_wish['contact_phone'],
                                            sharing_method='whatsapp',
                                            status='initiated'
                                        )
                                        st.success("✅ WhatsApp opened with your message!")
                                        st.info("💡 Complete the sending in the WhatsApp window that opened.")
                    
                    # Privacy notice
                    st.info("🔒 **Privacy**: Messages are shared directly. SHAKTI-AI doesn't store shared content.")
            
            # Action buttons
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("✏️ Edit Wishes", use_container_width=True):
                    st.session_state['show_wishes_form'] = True
                    st.rerun()
            
            with col2:
                if current_wish and st.button("📊 View History", use_container_width=True):
                    sharing_history = wishes_db.get_sharing_history(user_id)
                    if sharing_history:
                        st.markdown("**Sharing History:**")
                        for record in sharing_history[:5]:  # Show last 5 entries
                            st.caption(f"📤 {record['sharing_method'].title()} to {record['shared_with']} - {record['shared_at'].strftime('%Y-%m-%d %H:%M')}")
                    else:
                        st.info("No sharing history found.")
            
            with col3:
                if current_wish and st.button("🗑️ Delete Wishes", use_container_width=True, type="secondary"):
                    if wishes_db.delete_wish(current_wish['id'], user_id):
                        # Clear session state
                        for key in ['wishes_input', 'contact_name', 'contact_email', 'contact_phone', 'contact_relationship']:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.session_state['show_wishes_form'] = True
                        st.success("🗑️ Wishes deleted securely.")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete wishes.")
                    
        st.markdown("</div>", unsafe_allow_html=True)

def get_wishes_summary(user_id=None):
    """Get a summary of wishes for the user."""
    if not user_id:
        user_id = get_user_id()
    
    wishes = wishes_db.get_wishes(user_id, limit=5)
    return {
        'total_wishes': len(wishes),
        'latest_wish': wishes[0] if wishes else None,
        'has_contact_info': any(w.get('contact_email') or w.get('contact_phone') for w in wishes)
    }
