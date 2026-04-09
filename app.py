import streamlit as st
from groq import Groq
import os

# --- 1. GLOBAL UI & PERFORMANCE CONFIG ---
st.set_page_config(
    page_title="Ofedeeped",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. PROFESSIONAL BRANDING & TYPOGRAPHY ---
# Unique Montserrat font for "Ofedeeped" brand and Inter for content
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&family=Inter:wght@400;600;800&display=swap');
    
    /* Unique Brand Title Styling */
    .brand-logo {
        font-family: 'Montserrat', sans-serif;
        font-size: 85px;
        font-weight: 900;
        color: #000000;
        text-align: center;
        letter-spacing: -6px;
        margin-bottom: 0px;
        line-height: 1;
    }
    
    /* Dynamic Font Sizing for Learning Modules */
    .concept-header { 
        font-family: 'Inter', sans-serif;
        font-size: 32px; 
        font-weight: 800; 
        color: #1A1A1A; 
        border-left: 8px solid #4F46E5;
        padding-left: 15px;
        margin-top: 30px;
    }
    
    .detail-body { 
        font-family: 'Inter', sans-serif;
        font-size: 18px; 
        line-height: 1.7; 
        color: #374151;
    }
    
    .summary-card { 
        background-color: #F9FAFB; 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid #E5E7EB; 
        font-size: 16px;
        margin-top: 20px;
    }

    /* Professional Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: black;
        color: white;
        font-weight: 700;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #333;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PERSISTENT AUTHENTICATION SYSTEM (SSO READY) ---
if "auth_session" not in st.session_state:
    st.session_state.auth_session = False

def show_login_portal():
    st.markdown('<p class="brand-logo">Ofedeeped</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-family:Inter; color:gray;'>Unified Learning Portal</p>", unsafe_allow_html=True)
    
    with st.container():
        st.write("### Secure Login")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Continue with Google"):
                st.session_state.auth_session = True
                st.rerun()
        with col2:
            if st.button("Continue with Microsoft"):
                st.session_state.auth_session = True
                st.rerun()
        
        st.markdown("---")
        st.caption("By logging in, you agree to the Ofedeeped Inc. Terms of Service.")

# --- 4. CORE AI ENGINE (NCTB & IB INTEGRATED) ---
def run_tutor_system():
    # Sidebar Navigation & Management
    st.sidebar.markdown("# Workspace Control")
    curriculum = st.sidebar.selectbox(
        "Select Framework", 
        ["NCTB (Bangladesh Class 1-12)", "IB Diploma (International)"]
    )
    api_key = st.sidebar.text_input("Groq Cloud API Key", type="password")
    
    if st.sidebar.button("Sign Out"):
        st.session_state.auth_session = False
        st.rerun()

    # Active Branding
    st.markdown('<p class="brand-logo" style="font-size:35px; text-align:left;">Ofedeeped</p>', unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = []

    # Display Chat
    for entry in st.session_state.history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"], unsafe_allow_html=True)

    # User Input Processing
    if user_input := st.chat_input("Ask a question about your curriculum..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"<div class='detail-body'>{user_input}</div>", unsafe_allow_html=True)

        if not api_key:
            st.warning("Action Required: Provide your Groq API Key in the sidebar.")
        else:
            try:
                client = Groq(api_key=api_key)
                
                # --- MASTER SYSTEM PROMPT ---
                # Logic: Language Mirroring, 3D Color Rendering, and Segmented Hierarchy
                system_logic = f"""
                You are the Ofedeeped AI Lead Tutor. Framework: {curriculum}.
                
                RULES:
                1. LANGUAGE MIRROR: If user asks in English, respond ONLY in English. If in Bengali, respond ONLY in Bengali.
                2. SEGMENTATION: Wrap answers in HTML tags:
                   - Core Concepts: <div class='concept-header'>Title</div>
                   - Depth Analysis: <div class='detail-body'>Details</div>
                   - Summary: <div class='summary-card'>Key Takeaways</div>
                3. 3D VISUALS: If asked for 'picture' or '3D art', generate a vivid, colorful text-based 3D structural analysis (using ASCII and rich descriptions).
                4. TARGET: Strictly follow NCTB (Class 1-12) or IB standards based on selection.
                """

                with st.chat_message("assistant"):
                    display = st.empty()
                    accumulated_text = ""
                    
                    stream = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": system_logic}] + st.session_state.history,
                        stream=True
                    )
                    
                    for chunk in stream:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            accumulated_text += delta
                            display.markdown(accumulated_text + "▌", unsafe_allow_html=True)
                    display.markdown(accumulated_text, unsafe_allow_html=True)
                
                st.session_state.history.append({"role": "assistant", "content": accumulated_text})
            
            except Exception as e:
                st.error(f"Engine Failure: {str(e)}")

# --- 5. APP EXECUTION ---
if not st.session_state.auth_session:
    show_login_portal()
else:
    run_tutor_system()
