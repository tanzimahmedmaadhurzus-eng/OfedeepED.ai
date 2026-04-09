import streamlit as st
import openai
import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# --- SECURE VAULT ENGINE ---
class AfedipVault:
    def __init__(self, password: str):
        # Fixed the salt value error here
        self.salt = b"afedip_secure_salt_2026" 
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=self.salt, iterations=100000)
        self.key = kdf.derive(password.encode())

    def encrypt(self, text: str) -> str:
        aes = AESGCM(self.key)
        nonce = os.urandom(12)
        encrypted = aes.encrypt(nonce, text.encode(), None)
        return base64.b64encode(nonce + encrypted).decode()

    def decrypt(self, encrypted_text: str) -> str:
        data = base64.b64decode(encrypted_text)
        aes = AESGCM(self.key)
        return aes.decrypt(data[:12], data[12:], None).decode()

# --- INTERFACE ---
st.set_page_config(page_title="AFEDIP: Advanced AI", page_icon="🛡️")
st.title("🛡️ AFEDIP SECURE AI SYSTEM")

if "messages" not in st.session_state: st.session_state.messages = []
if "vault" not in st.session_state: st.session_state.vault = None

with st.sidebar:
    st.header("SECURITY PANEL")
    master_pass = st.text_input("Master Password", type="password")
    api_key = st.text_input("OpenAI API Key", type="password")
    if st.button("INITIALIZE"):
        if master_pass and api_key:
            try:
                st.session_state.vault = AfedipVault(master_pass)
                st.session_state.enc_key = st.session_state.vault.encrypt(api_key)
                st.success("AES-256 VAULT ACTIVE")
            except Exception as e:
                st.error(f"Initialization Failed: {str(e)}")

# --- CHAT LOGIC ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Enter your query..."):
    if not st.session_state.vault:
        st.error("INITIALIZE SECURITY FIRST")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        try:
            openai.api_key = st.session_state.vault.decrypt(st.session_state.enc_key)
            with st.chat_message("assistant"):
                full_res = ""
                res_box = st.empty()
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "You are AFEDIP AI. Expert academic tutor for Bangladesh curriculum. Use professional English."}, 
                              *st.session_state.messages],
                    stream=True
                )
                for chunk in response:
                    content = chunk.choices[0].delta.get("content", "")
                    full_res += content
                    res_box.markdown(full_res + "█")
                res_box.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e: 
            st.error(f"ERROR: {str(e)}")
