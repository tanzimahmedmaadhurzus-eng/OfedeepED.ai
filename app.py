import streamlit as st
from groq import Groq
import os

# --- CLEAN PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ofedeeped",
    page_icon="✨",
    layout="centered"
)

# --- MINIMALIST STYLING ---
st.markdown("""
    <style>
    .brand-title {
        font-family: 'Inter', sans-serif;
        color: #000000;
        text-align: center;
        font-size: 60px;
        font-weight: 900;
        letter-spacing: -2px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #000000;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION MODULE ---
def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        # Show Only "Ofedeeped" Branding
        st.markdown('<p class="brand-title">Ofedeeped</p>', unsafe_allow_html=True)
        
        with st.container():
            st.subheader("Login to your account")
            username = st.text_input("Username", placeholder="tanzimahmedmaadhurzo")
            password = st.text_input("Password", type="password", placeholder="ofedeeped2026")
            
            if st.button("Enter Ofedeeped"):
                if username == "tanzimahmedmaadhurzo" and password == "ofedeeped2026":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try again.")
        return False
    return True

# --- MAIN APP LOGIC ---
if check_auth():
    # Sidebar Navigation
    st.sidebar.title("Ofedeeped")
    curriculum = st.sidebar.radio(
        "Select Framework",
        ["NCTB (Bangladesh)", "IB Diploma"]
    )
    
    api_key = st.sidebar.text_input("Groq API Key", type="password")
    
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

    # Minimalist Header
    st.markdown('<p style="font-size:32px; font-weight:bold;">Ofedeeped AI</p>', unsafe_allow_html=True)
    st.caption(f"Curriculum: {curriculum}")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # AI Process Flow
    if prompt := st.chat_input("Ask your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if not api_key:
            st.warning("Please provide your API Key in the sidebar.")
        else:
            try:
                client = Groq(api_key=api_key)
                
                # Instruction Engine
                system_instruction = (
                    f"You are the Ofedeeped AI specialized in {curriculum}. "
                    "1. Respond in both English and Bengali. "
                    "2. For Science/Math, provide a 3D structural analysis. "
                    "3. Keep the tone professional and helpful."
                )

                with st.chat_message("assistant"):
                    response_area = st.empty()
                    full_resp = ""
                    
                    stream = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": system_instruction}] + st.session_state.messages,
                        stream=True
                    )
                    
                    for chunk in stream:
                        text = chunk.choices[0].delta.content
                        if text:
                            full_resp += text
                            response_area.markdown(full_resp + "▌")
                    response_area.markdown(full_resp)
                
                st.session_state.messages.append({"role": "assistant", "content": full_resp})
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
            
