import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import random

# Load API key
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_KEY")
gen_ai.configure(api_key=GEMINI_KEY)

# Page setup
st.set_page_config(page_title="Chat with EnergiBot", layout="centered")

# Initialize Gemini model
model = gen_ai.GenerativeModel("gemini-2.5-pro")

# Session state initialization
if "chat_stage" not in st.session_state:
    st.session_state.chat_stage = "collect_name"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_age" not in st.session_state:
    st.session_state.user_age = ""
if "education_level" not in st.session_state:
    st.session_state.education_level = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Greeting phrases
greetings = ["Hello", "Hi", "Welcome", "Hey there", "Nice to meet you"]

# Show chat history
for message in st.session_state.chat_history:
    with st.chat_message("user" if message["role"] == "user" else "assistant"):
        if message["role"] == "user":
            st.markdown(f"👤 **{st.session_state.user_name}**\n\n{message['message']}")
        else:
            st.markdown(f"🤖 **EnergiBot**\n\n{message['message']}")

# Stage 1: Collect Name
if st.session_state.chat_stage == "collect_name":
    with st.chat_message("assistant"):
        st.markdown("🤖 **EnergiBot**\n\nWhat is your name?")
    if name := st.chat_input("Enter your name"):
        st.session_state.user_name = name
        greet = random.choice(greetings)
        st.session_state.chat_history.append({"role": "user", "message": name})
        st.session_state.chat_history.append({"role": "assistant", "message": f"{greet}, {name}! How old are you?"})
        st.session_state.chat_stage = "collect_age"
        st.rerun()

# Stage 2: Collect Age
elif st.session_state.chat_stage == "collect_age":
    with st.chat_message("assistant"):
        st.markdown(f"🤖 **EnergiBot**\n\nHow old are you, {st.session_state.user_name}?")
    if age := st.chat_input("Enter your age"):
        st.session_state.user_age = age
        st.session_state.chat_history.append({"role": "user", "message": age})
        st.session_state.chat_stage = "collect_education"
        st.rerun()

# Stage 3: Collect Education Level
elif st.session_state.chat_stage == "collect_education":
    with st.chat_message("assistant"):
        st.markdown("🤖 **EnergiBot**\n\n📚 Please choose your class or education level:")

    levels = [
        "Class1", "Class2", "Class3", "Class4", "Class5",
        "JSS1", "JSS2", "JSS3", "SS1", "SS2", "SS3",
        "Undergraduate", "Masters", "PhD"
    ]
    level = st.selectbox("Select your level:", levels, key="education_selector")

    if st.button("✅ Continue"):
        st.session_state.education_level = level
        st.session_state.chat_history.append({
            "role": "assistant",
            "message": f"Awesome! You’re in **{level}**. Ask me a question!"
        })

        # Inject memory/personality into Gemini
        memory = (
            f"You are a friendly chatbot named EnergiBot. You teach energy topics to kids. "
            f"The user is named {st.session_state.user_name}, aged {st.session_state.user_age}, "
            f"and is in {level} level. Respond in a fun and understandable way for this audience."
        )
        st.session_state.chat_session.send_message(memory)
        st.session_state.chat_stage = "chatting"
        st.rerun()

# Stage 4: Chatting
elif st.session_state.chat_stage == "chatting":
    if prompt := st.chat_input(f"What would you like to know, {st.session_state.user_name}?"):

        # Show user message
        with st.chat_message("user"):
            st.markdown(f"👤 **{st.session_state.user_name}**\n\n{prompt}")
        st.session_state.chat_history.append({
            "role": "user",
            "message": prompt
        })

        # Stream assistant response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            for chunk in st.session_state.chat_session.send_message(prompt, stream=True):
                part = chunk.text if hasattr(chunk, "text") else ""
                full_response += part
                response_placeholder.markdown(f"🤖 **EnergiBot**\n\n{full_response}")

        st.session_state.chat_history.append({
            "role": "assistant",
            "message": full_response
        })

        st.rerun()
