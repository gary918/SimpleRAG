import streamlit as st
from st_pages import Page
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
import os
import tempfile
from langchain_community.vectorstores.chroma import Chroma
import pandas as pd

VECTORDB_PERSIST_DIRCTORY = "../vectordb"
LLM_MODEL_NAME = "deepseek-r1:1.5b"
LLM_MODEL_NAME = "phi3.5"

def init():
    st.title("🔍 Simple RAG")

def load_retriever():
    embedder = HuggingFaceEmbeddings()
    vector_db = Chroma(persist_directory=VECTORDB_PERSIST_DIRCTORY, 
                       embedding_function=embedder)
    if vector_db is None:
        return None
    else:
        return vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

def get_source_list():
    embedder = HuggingFaceEmbeddings()
    vector_db = Chroma(persist_directory=VECTORDB_PERSIST_DIRCTORY, 
                       embedding_function=embedder)
    if vector_db is None:
        return None
    
    db = vector_db
    print(db.get().keys())
    print(len(db.get()["ids"]))
    print(db.get()["ids"])
    ids = db.get()["ids"]

    # Print the list of source files
    sources_dict = {}
    for x in range(len(db.get()["ids"])):
        doc = db.get()["metadatas"][x]
        source = doc["source"]
        if source not in sources_dict:
            sources_dict[source] = []
        sources_dict[source].append(ids[x])
    
    sources = [[source, ids] for source, ids in sources_dict.items()]
    
    return sources

def load_documents(file):
    loader = PDFPlumberLoader(file)
    documents = loader.load()
    return documents

def create_retriever(documents):
    text_splitter = SemanticChunker(HuggingFaceEmbeddings())
    documents = text_splitter.split_documents(documents)
    print("****************** documents:", documents)
    embedder = HuggingFaceEmbeddings()
    vector = Chroma.from_documents(documents, embedder, persist_directory=VECTORDB_PERSIST_DIRCTORY)
    retriever = vector.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    return retriever

def initialize_qa_chain(retriever, model_name=LLM_MODEL_NAME):
    llm = Ollama(model=model_name)
    return RetrievalQA.from_chain_type(llm, retriever=retriever)

def delete_source(selected_ids):
    embedder = HuggingFaceEmbeddings()
    vector_db = Chroma(persist_directory=VECTORDB_PERSIST_DIRCTORY, 
                       embedding_function=embedder)
    vector_db.delete(selected_ids)

def df_on_change():
    pass
    
def main():
    init()
    
    with st.sidebar:
        st.header("Actions")
        
        if st.button("Q/A"):
            st.session_state.show_qa = True
            st.session_state.show_documents = False
        
        if st.button("Documents"):
            st.session_state.show_qa = False
            st.session_state.show_documents = True

    retriever = load_retriever()

    if "show_documents" in st.session_state and st.session_state.show_documents:
        st.subheader("Add a new document")
        uploaded_file = st.file_uploader("Upload a new PDF file", type=["pdf"])
        
        st.subheader("Existing documents")
        sources = get_source_list()
        for source in sources:
            print("---------------source:", source)
            df = pd.DataFrame({"Source": [source[0]] * len(source[1]), "Document ID": source[1]})
            edited_df = st.data_editor(df, on_change=df_on_change)
            if st.button(f"Update {source[0]}"):
                # Handle update logic here
                st.write(f"Updated {source[0]}")

            if st.button(f"Delete {source[0]}"):
                st.error("Do you want to delete this document?")
                st.button("Yes", on_click= delete_source(edited_df[edited_df["Source"] == source[0]]["Document ID"].tolist()))
                st.button("No", on_click= st.write("Cancelled"))
            #st.write(source[0]+" : "+source[1])

        if uploaded_file is not None:
            temp_file_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(uploaded_file.read())
            uploaded_file = temp_file_path
        
            documents = load_documents(uploaded_file)
            retriever = create_retriever(documents)
            
            uploaded_file = None
    
    if retriever is not None:
        qa_chain = initialize_qa_chain(retriever)
        if "show_qa" in st.session_state and st.session_state.show_qa:
            query = st.text_input("Enter your questions:")
            if query:
                response = qa_chain.run(query)
                st.write("💡 Answer:", response)

if __name__ == "__main__":
    main()