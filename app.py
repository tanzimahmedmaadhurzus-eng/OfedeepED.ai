import streamlit as st
from groq import Groq

# --- UI & Branding ---
st.set_page_config(page_title="Ofedeep AI | 100% Student Solution", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-title { color: #1E3A8A; font-size: 35px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🛡️ Ofedeep AI: Digital Tutor</p>', unsafe_allow_html=True)
st.caption("বাংলাদেশের ১ম-১২তম শ্রেণীর সকল বই ও শিক্ষা সহায়তায় নিবেদিত নিজস্ব এআই।")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("🔑 Private Access")
    groq_api_key = st.text_input("Enter Groq API Key", type="password")
    st.divider()
    st.info("এটি Ofedeep AI-এর নিজস্ব সার্ভার ব্যবহার করে, যা ১০০% ফ্রি এবং দ্রুত।")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- AI Logic ---
if prompt := st.chat_input("বইয়ের যেকোনো প্রশ্ন এখানে লিখুন (যেমন: নবম শ্রেণীর গণিত)..."):
    if not groq_api_key:
        st.error("দয়া করে সাইডবারে আপনার Groq API Key-টি দিন।")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Groq Client Initialization
            client = Groq(api_key=groq_api_key)
            
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                
                # Ofedeep AI Custom Instructions
                completion = client.chat.completions.create(
                    model="llama3-8b-8192", # সুপার ফাস্ট ওপেন সোর্স মডেল
                    messages=[
                        {
                            "role": "system", 
                            "content": """Your name is Ofedeep AI. You are a private academic assistant for students in Bangladesh (Class 1-12).
                            1. You have 100% knowledge of NCTB (National Curriculum and Textbook Board) books.
                            2. You must answer in Bengali if the student asks in Bengali.
                            3. For Math and Science, provide step-by-step solutions with clear logic.
                            4. Be polite, professional, and act like a senior teacher from Bangladesh."""
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
            st.error(f"সার্ভার ত্রুটি: {str(e)}")
            
