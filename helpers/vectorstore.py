from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

def create_or_load_vectorstore(chunks, persist_directory="./startup_db"):
    """
    Creates a new vectorstore or loads existing one.
    
    Args:
        chunks: Document chunks to embed
        persist_directory (str): Directory to persist vectorstore
        
    Returns:
        Chroma: Vectorstore instance
    """
    import os
    
    # First try to load existing vectorstore
    existing = load_vectorstore(persist_directory)
    if existing:
        print(f"✅ Loaded existing vectorstore from {persist_directory}")
        return existing
    
    # Create new vectorstore if none exists
    print(f"🆕 Creating new vectorstore in {persist_directory}")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'} # Use CPU. You can change to 'cuda' if you have a GPU.
    )
    
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    # Ensure the vectorstore is persisted
    vectordb.persist()
    print(f"💾 Vectorstore persisted to {persist_directory}")
    
    return vectordb

def load_vectorstore(persist_directory="./startup_db"):
    """
    Loads an existing vectorstore from disk.
    
    Args:
        persist_directory (str): Directory where vectorstore is stored
        
    Returns:
        Chroma: Vectorstore instance or None if not found
    """
    import os
    
    # Check if the directory exists and has vectorstore files
    if not os.path.exists(persist_directory):
        return None
    
    # Check if there are actual vectorstore files (not just empty directory)
    vectorstore_files = [
        "chroma.sqlite3",
        "chroma.sqlite3-shm", 
        "chroma.sqlite3-wal"
    ]
    
    has_files = any(os.path.exists(os.path.join(persist_directory, f)) for f in vectorstore_files)
    if not has_files:
        return None
    
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Try to load the existing vectorstore
        vectorstore = Chroma(
            persist_directory=persist_directory, 
            embedding_function=embeddings
        )
        
        # Verify it has documents
        if vectorstore and hasattr(vectorstore, '_collection') and vectorstore._collection.count() > 0:
            return vectorstore
        else:
            return None
            
    except Exception as e:
        print(f"Error loading vectorstore: {e}")
        return None
