import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    },
)

# Initialize session state
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "education_selected" not in st.session_state:
    st.session_state.education_selected = False

# Title
st.title("🔋 EnergiBot — Ask Me Anything About Energy!")

# Step 1: Get name
if not st.session_state.user_name:
    st.session_state.user_name = st.text_input("👤 Please enter your name to begin:")
    st.stop()

# Step 2: Select education level
if not st.session_state.education_selected:
    level = st.selectbox("🎓 Select your education level:", ["Primary", "Secondary", "Tertiary"])
    if st.button("Continue"):
        st.session_state.education_selected = True
        st.session_state.chat_session.send_message(
            f"My name is {st.session_state.user_name} and my education level is {level}."
        )
        st.rerun()
    st.stop()

# Chat area
st.write("💬 **Ask me a question about energy:**")

# Chat input
prompt = st.chat_input("Type your question...")

# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**{st.session_state.user_name}**: {chat['message']}")
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(f"**EnergiBot**: {chat['message']}")

# Handle new prompt
if prompt:
    # Display user message
    st.session_state.chat_history.append({"role": "user", "message": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"**{st.session_state.user_name}**: {prompt}")

    # Stream EnergiBot's reply
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("**EnergiBot**: ", unsafe_allow_html=True)
        response_placeholder = st.empty()
        full_response = ""

        for chunk in st.session_state.chat_session.send_message(prompt, stream=True):
            if chunk.text:
                full_response += chunk.text
                response_placeholder.markdown(f"**EnergiBot**: {full_response}")

    # Save assistant reply to chat history
    st.session_state.chat_history.append({"role": "assistant", "message": full_response})
