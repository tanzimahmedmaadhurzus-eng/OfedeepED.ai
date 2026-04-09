import streamlit as st
from groq import Groq
import os
from PIL import Image

# --- Page Config ---
st.set_page_config(page_title="Ofedeeped AI | Bilingual & 3D", page_icon="🎓", layout="centered")

# --- Logo handling with Error fix ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        if os.path.exists("logo.png"):
            img = Image.open("logo.png")
            st.image(img, use_container_width=True)
        else:
            st.title("🎓 Ofedeeped AI")
    except Exception:
        st.title("🎓 Ofedeeped AI") # লোগোতে এরর থাকলে নাম দেখাবে অ্যাপ ক্র্যাশ করবে না

st.markdown("<h4 style='text-align: center;'>Bilingual Learning & 3D Visualization</h4>", unsafe_allow_html=True)

# --- Sidebar ---
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

# --- AI Logic (Bilingual + 3D) ---
if prompt := st.chat_input("যেকোনো প্রশ্ন করুন (English/বাংলা)..."):
    if not groq_api_key:
        st.error("Please provide your Groq API Key.")
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
                            1. Answer ALWAYS in both English and Bengali.
                            2. For Science/Academic topics, include a section called '3D Perspective' where you explain the spatial structure or process (e.g., describing an atom or cells in 3D).
                            3. Style: Professional teacher."""
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
    
