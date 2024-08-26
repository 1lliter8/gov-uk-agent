import streamlit as st
from langchain_core.messages import HumanMessage

from graph import build_graph

if 'graph' not in st.session_state:
    st.session_state.graph = build_graph()
    st.session_state.thread = 42

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        role = 'user'
    else:
        role = 'assistant'

    with st.chat_message(role):
        st.markdown(message.content)


if prompt := st.chat_input('What is up?'):
    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        response = st.session_state.graph.invoke(
            {'messages': [HumanMessage(content=prompt)]},
            config={'configurable': {'thread_id': st.session_state.thread}},
        )

        st.write(response['messages'][-1].content)

    st.session_state.messages = response['messages']
