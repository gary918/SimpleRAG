# SimpleRAG
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
## Run
```cd src```

```streamlit run app.py```
