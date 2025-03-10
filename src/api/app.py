from fastapi import FastAPI
from fastapi.responses import JSONResponse

from rag.rag_helper import RAGHelper

app = FastAPI(
    title="SimpleRAG API",
    description="This is a simple RAG API",
    version="0.1.0",
)

rag_helper = RAGHelper()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/query", description="Query with the model")
def query(query:str):
    result = rag_helper.query(query)
    return JSONResponse(content=result, status_code=200)