import streamlit as st
from groq import Groq
import os

# --- পেজ কনফিগারেশন ---
st.set_page_config(page_title="Ofedeeped AI | 100% Solution", page_icon="🎓", layout="centered")

# --- লোগো ডিসপ্লে সেকশন ---
col1, col2, col3 = st.columns([1, 2, 1]) # লোগো মাঝখানে রাখার জন্য
with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.title("🎓 Ofedeeped AI")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.caption("<center>বাংলাদেশের ১-১২ শ্রেণীর সকল বই ও শিক্ষা সহায়তায় নিবেদিত নিজস্ব এআই।</center>", unsafe_allow_html=True)

# --- সাইডবার সেটিংস ---
with st.sidebar:
    st.header("⚙️ Settings")
    groq_api_key = st.text_input("আপনার Groq API Key দিন", type="password")
    st.divider()
    if st.button("নতুন চ্যাট শুরু করুন"):
        st.session_state.messages = []
        st.rerun()

# চ্যাট হিস্ট্রি শুরু করা
if "messages" not in st.session_state:
    st.session_state.messages = []

# আগের কথাগুলো দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- মূল চ্যাট লজিক ---
if prompt := st.chat_input("বইয়ের যেকোনো প্রশ্ন এখানে লিখুন..."):
    if not groq_api_key:
        st.error("দয়া করে সাইডবারে আপনার Groq API Key-টি দিন।")
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
                        {"role": "system", "content": "You are Ofedeeped AI. A senior expert teacher for Class 1-12 in Bangladesh. Answer clearly in Bengali."},
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
        
