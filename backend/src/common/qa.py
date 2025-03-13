import streamlit as st

from rag.rag_helper import RAGHelper

st.subheader('Q/A')

rag_helper = st.session_state.rag_helper
qa_chain = rag_helper.get_qa_chain()
query = st.text_input("Enter your questions:")
if query:
    response = qa_chain.invoke(query)
    st.write("💡 Answer:", response["result"])

