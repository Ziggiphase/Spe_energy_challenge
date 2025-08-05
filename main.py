import streamlit as st
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="EnergiBot Chat", page_icon="⚡")
st.title("⚡ EnergiBot - AI Assistant for Energy Learners")

# Session initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
if "level_selected" not in st.session_state:
    st.session_state.level_selected = False

# Education Level Selection
if not st.session_state.level_selected:
    st.markdown("### What is your level of education?")
    level = st.radio(
        "Choose your level:",
        ["Primary", "Secondary", "Tertiary", "Others"],
        index=None,
        key="level_radio"
    )

    if level:
        if st.button("Continue"):
            st.session_state.level_selected = True
            st.session_state.chat_session.send_message(
                f"My education level is {level}. You are EnergiBot. Please reply accordingly."
            )
            st.session_state.chat_history.append(
                {"role": "user", "message": f"🧑 {level}"}
            )
            st.session_state.chat_history.append(
                {"role": "assistant", "message": "🤖 EnergiBot: Great! Ask me a question to begin."}
            )
            st.experimental_rerun()

else:
    # Chat interface
    for msg in st.session_state.chat_history:
        st.markdown(f"**{msg['message']}**")

    prompt = st.chat_input("Ask me anything about energy...")

    if prompt:
        trimmed_prompt = prompt.strip()[:500]  # avoid timeout

        # Add user message
        st.session_state.chat_history.append({"role": "user", "message": f"🧑 {trimmed_prompt}"})

        try:
            response = st.session_state.chat_session.send_message(trimmed_prompt)
            reply_text = response.text.strip()
        except Exception as e:
            reply_text = "🤖 EnergiBot: Sorry, something went wrong. Please try again."

        # Add assistant response
        st.session_state.chat_history.append(
            {"role": "assistant", "message": f"🤖 EnergiBot: {reply_text}"}
        )
        st.rerun()
