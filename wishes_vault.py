import streamlit as st
import os
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
                contact_name = st.text_input("Trusted contact name (optional)", value=st.session_state['contact_name'], key='contact_name')
                contact_info = st.text_input("Trusted contact email/phone (optional)", value=st.session_state['contact_info'], key='contact_info')
                submitted = st.form_submit_button("Save Wishes Securely")
                if submitted:
                    try:
                        f = _get_fernet()
                        contact_str = f"{contact_name}|{contact_info}" if contact_name or contact_info else ""
                        data = wishes_input.strip() + "\n---CONTACT---\n" + contact_str
                        enc = f.encrypt(data.encode('utf-8'))
                        _save_encrypted(enc)
                        # Do not update st.session_state for widget keys after instantiation
                        st.session_state['show_wishes_form'] = False
                        st.success("Wishes saved securely!")
                        try:
                            if hasattr(st, 'experimental_rerun'):
                                st.experimental_rerun()
                            else:
                                st.experimental_user()
                        except Exception:
                            pass
                    except Exception as e:
                        st.error(f"Encryption error: {e}")
        else:
            if wishes:
                st.markdown(f"**Your wishes:**<br><span style='color:#444'>{wishes}</span>", unsafe_allow_html=True)
            if contact:
                st.caption(f"Trusted contact: {contact}")
            if st.button("Edit Wishes", key="edit_wishes_btn"):
                st.session_state['show_wishes_form'] = True
                try:
                    if hasattr(st, 'experimental_rerun'):
                        st.experimental_rerun()
                    else:
                        st.experimental_user()
                except Exception:
                    pass
            if st.button("Delete Wishes", key="delete_wishes_btn"):
                _delete_encrypted()
                st.session_state['wishes_input'] = ""
                st.session_state['contact_name'] = ""
                st.session_state['contact_info'] = ""
                st.session_state['show_wishes_form'] = True
                st.success("Wishes deleted.")
                try:
                    if hasattr(st, 'experimental_rerun'):
                        st.experimental_rerun()
                    else:
                        st.experimental_user()
                except Exception:
                    pass
        st.markdown("</div>", unsafe_allow_html=True)
