from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

def create_or_load_vectorstore(chunks, persist_directory="./startup_db"):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'} # Use CPU. You can change to 'cuda' if you have a GPU.
    )
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb

def load_vectorstore(persist_directory="./startup_db"):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)
