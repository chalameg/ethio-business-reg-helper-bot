import os
from langchain_community.document_loaders import PyPDFLoader

def load_documents(data_path="data"):
    docs = []
    for file in os.listdir(data_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(data_path, file))
            docs.extend(loader.load())
    return docs
