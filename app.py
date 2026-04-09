import streamlit as st
from groq import Groq
import os

# --- Page Config ---
st.set_page_config(page_title="Ofedeeped AI | Bilingual & 3D", page_icon="🎓", layout="centered")

# --- Logo Display ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.title("🎓 Ofedeeped AI")

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .bilingual-box { border-left: 5px solid #1E3A8A; padding-left: 15px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- Settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    groq_api_key = st.text_input("Enter Groq API Key", type="password")
    if st.button("New Chat / নতুন চ্যাট"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- AI Logic ---
if prompt := st.chat_input("Ask anything... / যেকোনো প্রশ্ন করুন..."):
    if not groq_api_key:
        st.error("Please provide API Key in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            client = Groq(api_key=groq_api_key)
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=[
                        {
                            "role": "system", 
                            "content": """Your name is Ofedeeped AI. 
                            RULES:
                            1. Answer EVERY query in both Bengali and English.
                            2. For Science/Math topics, always provide a '3D Visualization' section where you describe the object or process in a 3D perspective (X, Y, Z axis) to help the student imagine it.
                            3. Structure: 
                               - [English Version]
                               - [Bengali Version]
                               - [3D Visualization / ৩ডি কল্পনা]"""
                        },
                        *st.session_state.messages
                    ],
                    stream=True
                )
                for chunk in completion:
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        full_response += content
                        response_placeholder.markdown(full_response + "█")
                response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
