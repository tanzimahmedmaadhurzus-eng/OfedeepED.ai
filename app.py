import streamlit as st
from groq import Groq
import os

# --- 1. GLOBAL UI CONFIGURATION ---
st.set_page_config(
    page_title="Ofedeeped",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. PROFESSIONAL STYLING (UNIQUE FONTS) ---
# Using 'Montserrat' for the brand and 'Inter' for readability
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&family=Inter:wght@400;600&display=swap');
    
    .main-brand {
        font-family: 'Montserrat', sans-serif;
        font-size: 80px;
        font-weight: 900;
        color: #000000;
        text-align: center;
        letter-spacing: -5px;
        margin-bottom: 0px;
        transition: 0.5s;
    }
    .main-brand:hover {
        color: #4F46E5;
    }
    .login-box {
        background-color: #F9FAFB;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #E5E7EB;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION & AUTHENTICATION (SSO READY) ---
if "auth_status" not in st.session_state:
    st.session_state.auth_status = False

def render_login():
    st.markdown('<p class="main-brand">Ofedeeped</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.write("### Single Sign-On (SSO) Portal")
        
        # Google/Microsoft Simulation (Ready for OAuth2 Integration)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌐 Google Login"):
                st.session_state.auth_status = True
                st.rerun()
        with col2:
            if st.button("🪟 Microsoft Login"):
                st.session_state.auth_status = True
                st.rerun()
        
        st.markdown("---")
        st.caption("Once logged in, your session remains active on this device.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. CORE ENGINE (NCTB & IB INTEGRATION) ---
def start_ofedeeped():
    # Sidebar Controls
    st.sidebar.title("Ofedeeped Control")
    curriculum = st.sidebar.selectbox(
        "Framework", 
        ["NCTB (Class 1-12 Bangladesh)", "IB Diploma (International)"]
    )
    api_key = st.sidebar.text_input("Groq Cloud API Key", type="password")
    
    if st.sidebar.button("Log Out"):
        st.session_status.auth_status = False
        st.rerun()

    # Chat Header
    st.markdown('<p style="font-size:35px; font-weight:900; font-family:Montserrat;">Ofedeeped AI</p>', unsafe_allow_html=True)
    st.info(f"Currently Optimized for: {curriculum}")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # USER INTERACTION LOGIC
    if user_query := st.chat_input("Ask about Math, Science, or Literature..."):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        if not api_key:
            st.error("Missing API Key in Sidebar.")
        else:
            try:
                client = Groq(api_key=api_key)
                
                # --- STRONG SYSTEM PROMPT ---
                # Logic: Dynamic Language, Segmented Structure, and Conditional Visuals
                system_logic = f"""
                You are the Ofedeeped AI Master Tutor. Framework: {curriculum}.
                1. LANGUAGE: If query is in English, reply in English. If Bengali, reply in Bengali.
                2. STRUCTURE: Break the answer into:
                   - Conceptual Overview
                   - Segmented Detailed Analysis (Step-by-step)
                   - Key Topics Summary (Most important points)
                3. VISUALS: If the user specifically asks for a 'picture', 'diagram', or 'visual', provide a detailed ASCII or Markdown description of the diagram. Do NOT provide images if not requested.
                4. TARGET: Accurate to Bangladesh NCTB Standards (1-12) or IB Global Criteria.
                """

                with st.chat_message("assistant"):
                    response_box = st.empty()
                    final_text = ""
                    
                    stream = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": system_logic}] + st.session_state.chat_history,
                        stream=True
                    )
                    
                    for chunk in stream:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            final_text += delta
                            response_box.markdown(final_text + "▌")
                    response_box.markdown(final_text)
                
                st.session_state.chat_history.append({"role": "assistant", "content": final_text})
            
            except Exception as e:
                st.error(f"Engine Error: {str(e)}")

# --- 5. EXECUTION ---
if not st.session_state.auth_status:
    render_login()
else:
    start_ofedeeped()
        
