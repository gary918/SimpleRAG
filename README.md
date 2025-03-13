# SimpleRAG
This is a simple RAG sample based on:
* LangChain
* Ollama
* Chroma

Which can be run by using:
* Streamlit
* React + FastAPI

## Install Ollama
### Deploy models
## Install python libraries
```pip install -r requirements.txt```

## Config the app
Edit .env file in the src directory.
```
VECTORDB_PERSIST_DIRCTORY = "../vectordb"
LLM_MODEL_NAME = "deepseek-r1:1.5b"
```
## Run Streamlit
```cd src```

```streamlit run app.py```

## Run FastAPI

```uvicorn api.app:app```

Acess the API docs page at http://localhost:8000/docs 

## Run React

```cd frontend```

```npm start```

Access the web page at http://localhost:3000 