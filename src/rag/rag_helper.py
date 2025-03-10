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


from dotenv import load_dotenv
import os
import pandas as pd

class RAGHelper:
    def __init__(self):
        load_dotenv()

        self.llm_model_name = os.getenv("LLM_MODEL_NAME")
        self.vector_db_persist_directory = os.getenv("VECTORDB_PERSIST_DIRCTORY")
        self.embedder = HuggingFaceEmbeddings()
        self.vector_db = Chroma(persist_directory=self.vector_db_persist_directory, 
                                embedding_function=self.embedder)
        
    def get_retirever(self):
        if self.vector_db is None:
            return None
        else:
            return self.vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        
    def get_source_list(self):
        if self.vector_db is None:
            return None
        
        db = self.vector_db
        print(db.get().keys())
        print(len(db.get()["ids"]))
        print(db.get()["ids"])
        ids = db.get()["ids"]   
        
        sources_dict = {}
        for x in range(len(db.get()["ids"])):
            doc = db.get()["metadatas"][x]
            source = doc["source"]
            if source not in sources_dict:
                sources_dict[source] = []
            sources_dict[source].append(ids[x])
        
        sources = [{"source": source, "ids": ", ".join(ids)} for source, ids in sources_dict.items()]
        sources_df = pd.DataFrame(sources)
        return sources_df
    
    def load_documents(self, file):
        loader = PDFPlumberLoader(file)
        documents = loader.load()
        return documents
    
    
    def add_docs_to_vector_db(self, documents):
        text_splitter = SemanticChunker(self.embedder)
        documents = text_splitter.split_documents(documents)
        self.vector_db = Chroma.from_documents(documents, self.embedder, persist_directory=self.vector_db_persist_directory)
        
    def get_qa_chain(self):
        retriever = self.get_retirever()
        llm = Ollama(model=self.llm_model_name)
        return RetrievalQA.from_chain_type(llm, retriever=retriever)

    def delete_source(self, selected_ids):
        print('.........delete_source:', selected_ids)
        self.vector_db.delete(selected_ids)