import streamlit as st
from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key = os.environ["OPENAI_API_KEY"]
)

st.title("My Own ChatGPT!🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# initialize model
if "model" not in st.session_state:
    st.session_state.model = "gpt-4-turbo-preview"
# for gpt-3.5-turbo:  gpt-3.5-turbo
# for gpt4-turbo:  gpt-4-turbo-preview    

# user input
if user_prompt := st.chat_input("Your prompt"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # generate responses
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for response in client.chat.completions.create(
            model=st.session_state.model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
