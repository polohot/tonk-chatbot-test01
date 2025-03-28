from openai import OpenAI
import streamlit as st

from dotenv import load_dotenv
load_dotenv()
###############################################################################

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

###############################################################################
st.title("ChatGPT-like clone")

with st.expander('debug'):
    st.json(st.session_state.messages)
###############################################################################
client = OpenAI()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()


# ADD CLEAR CHAT BUTTON
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.messageslog = []
    st.rerun()

