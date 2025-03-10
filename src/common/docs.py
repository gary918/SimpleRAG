import streamlit as st
import pandas as pd
import tempfile
import os
import uuid

from rag.rag_helper import RAGHelper

st.subheader("Add a new document")
# Initialize session state for the uploaded file
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
uploaded_file = st.file_uploader("Upload a new PDF file", type=["pdf"], key=f"uploader_{st.session_state.uploader_key}")

st.subheader("Existing documents")
rag_helper = st.session_state.rag_helper
sources_df = rag_helper.get_source_list()

sources_tb = st.dataframe(sources_df, on_select="rerun", selection_mode=["single-row","multi-column"])

if st.button("Delete"):
    selected_row = sources_tb.selection
    print("~~~~~~~~~~",selected_row)
    if selected_row is not None:
        selected_source = [item.strip() for sublist in sources_df.iloc[selected_row["rows"]]["ids"].str.split(",").tolist() for item in sublist]
        print("xxxxxxxxxx",selected_source)
        rag_helper.delete_source(selected_source)
        st.rerun()
    

# for source in sources:
#     print("---------------source:", source)
#     df = pd.DataFrame({"Source": [source[0]] * len(source[1]), "Document ID": source[1]})
#     edited_df = st.data_editor(df)
#     if st.button("Delete", key=f"del_{source[0]}"):
#         rag_helper.delete_source(edited_df[edited_df["Source"] == source[0]]["Document ID"].tolist())
#         st.rerun()

if uploaded_file is not None:
    temp_file_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())
    uploaded_file = temp_file_path

    rag_helper = st.session_state.rag_helper
    documents = rag_helper.load_documents(uploaded_file)
    retriever = rag_helper.add_docs_to_vector_db(documents)
    
    st.session_state.uploader_key += 1
    st.rerun()
    