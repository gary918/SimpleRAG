import streamlit as st
from rag.rag_helper import RAGHelper

def init():
    rag_helper = RAGHelper()
    st.session_state.rag_helper = rag_helper

init()

qa_page = st.Page(
    "common/qa.py",
    title="Q/A",
    icon=":material/help:",
)

docs_page = st.Page(
    "common/docs.py",
    title="Documents",
    icon=":material/help:",
)

common_pages = [qa_page, docs_page]

st.title("Simple RAG")
page_dict = {}
page_dict["Common"] = common_pages

if len(page_dict) > 0:
    pg = st.navigation({"Common": common_pages} | page_dict)

pg.run()