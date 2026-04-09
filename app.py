import streamlit as st
from groq import Groq
import os

# --- ADVANCED PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ofedeeped",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR BRANDING ---
st.markdown("""
    <style>
    .main-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1E1E1E;
        text-align: center;
        font-size: 50px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #4F46E5;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION MODULE ---
def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        # Display Branding before Login
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if os.path.exists("logo.png"):
                st.image("logo.png")
            else:
                st.markdown('<p class="main-title">Ofedeeped</p>', unsafe_allow_html=True)
        
        with st.container():
            st.subheader("Secure Access / একাউন্ট লগইন")
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            if st.button("Access Dashboard"):
                if username == "tanzimahmedmaadhurzo" and password == "ofedeeped2026":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
        return False
    return True

# --- CORE APPLICATION LOGIC ---
if check_auth():
    # Sidebar Setup
    st.sidebar.title("Ofedeeped Control Panel")
    st.sidebar.markdown("---")
    
    # Curriculum Logic Integration
    curriculum = st.sidebar.selectbox(
        "Academic Framework",
        ["NCTB (Bangladesh National Curriculum)", "IB Diploma Program (International)"]
    )
    
    api_key = st.sidebar.text_input("Groq API Key", type="password", help="Enter your Groq cloud API key here.")
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    # Chat Interface
    st.markdown(f'<p style="font-size:24px; font-weight:bold;">Ofedeeped AI Tutor ({curriculum})</p>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # AI Process Flow
    if prompt := st.chat_input("Ask a concept (e.g., Quantum Mechanics or Newton's Law)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if not api_key:
            st.warning("Action Required: Please enter your Groq API Key in the sidebar.")
        else:
            try:
                client = Groq(api_key=api_key)
                
                # HIGH-LEVEL SYSTEM PROMPTING
                system_instruction = (
                    f"You are the lead AI Tutor at Ofedeeped Inc. "
                    f"Strictly adhere to the {curriculum} framework. "
                    "RESPONSE GUIDELINES: "
                    "1. Dual-Language Output: Provide every explanation in both English and Bengali. "
                    "2. 3D Perspective: For Science/Math, describe the object in 3D coordinate space (X, Y, Z). "
                    "3. Pedagogy: If IB, use inquiry-based learning. If NCTB, follow the latest curriculum standards."
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
                st.error(f"System Error: {str(e)}")
        
