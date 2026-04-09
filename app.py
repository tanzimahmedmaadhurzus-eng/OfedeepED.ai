import streamlit as st
from groq import Groq
import os
from PIL import Image
import streamlit_authenticator as stauth

# --- Page Config ---
st.set_page_config(page_title="Ofedeeped", page_icon="🎓", layout="centered")

# --- Authentication Logic (Simplified for Startup) ---
names = ['User']
usernames = ['user123']
passwords = ['ofedeeped2026'] # আপনি এটি পরিবর্তন করতে পারেন

hashed_passwords = stauth.Hasher(passwords).generate()
credentials = {"usernames":{usernames[0]:{"name":names[0],"password":hashed_passwords[0]}}}

authenticator = stauth.Authenticate(credentials, "ofedeeped_auth", "auth_key", cookie_expiry_days=30)

# --- Initial View: Logo & Login ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.title("🎓 Ofedeeped")
    except:
        st.title("🎓 Ofedeeped")

name, authentication_status, username = authenticator.login("Login / একাউন্ট খুলুন", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.info("Please login to access the AI Tutor / এগিয়ে যেতে লগইন করুন।")

# --- Main App (After Successfull Login) ---
if authentication_status:
    authenticator.logout("Logout", "sidebar")
    
    st.sidebar.title("⚙️ Curriculum Settings")
    curriculum = st.sidebar.selectbox(
        "Select Curriculum / কারিকুলাম বাছাই করুন",
        ["NCTB (Bangladesh)", "IB Diploma (International)"]
    )
    
    st.sidebar.info(f"Active: {curriculum}")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- AI Query Logic ---
    if prompt := st.chat_input("Ask anything (English/বাংলা)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
        
        if not groq_api_key:
            st.warning("Please enter your API Key in the sidebar to start.")
        else:
            try:
                client = Groq(api_key=groq_api_key)
                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    # Custom System Prompt for Curriculum
                    system_prompt = f"""
                    Your name is Ofedeeped AI. 
                    1. Provide answers strictly based on the {curriculum} curriculum.
                    2. If NCTB, focus on Bangladesh context and textbook standards.
                    3. If IB Diploma, focus on Theory of Knowledge (TOK) and deep conceptual understanding.
                    4. ALWAYS explain in both English and Bengali (Side-by-side or sectioned).
                    5. For Science/Math, include a '3D Perspective' section explaining the spatial structure.
                    """

                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                        stream=True
                    )
                    for chunk in completion:
                        content = chunk.choices[0].delta.content
                        if content:
                            full_response += content
                            response_placeholder.markdown(full_response + "█")
                    response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {str(e)}")
            
