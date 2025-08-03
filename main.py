import os
import streamlit as st

from dotenv import load_dotenv
import google.generativeai as gen_ai

load_dotenv()

st.set_page_config(
    page_title="Chat with EnergiBot",
    layout="centered"
)

GEMINI_KEY = os.getenv("GEMINI_KEY")
gen_ai.configure(api_key=GEMINI_KEY)
model = gen_ai.GenerativeModel("gemini-2.5-pro")

#function translates roles between Gemini and Streamlit terminolgy

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


#Initializing chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

#Chatbot title
st.title("EnergiBot")

#Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.role[0])

#Input field for user's messsage
memory = f"""
You are a friendly energy teacher chatbot named EnergiBot, designed for kids"""
st.session_state.chat_session.send_message(memory)
user_prompt = st.chat_input("Ask EnergiBot ..........")
if user_prompt:
    st.markdown(user_prompt)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    #Display response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)


st.write(st.session_state)

#Initialize reset button
if st.button("Reset Chat"):
    st.rerun()