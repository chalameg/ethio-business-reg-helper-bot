# helpers/vectorstore.py

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import pickle


def create_or_load_vectorstore(chunks, persist_directory="./startup_db"):
    """
    Creates a new vectorstore or loads existing one using FAISS.
    
    Args:
        chunks: Document chunks to embed
        persist_directory (str): Directory to persist vectorstore
        
    Returns:
        FAISS: Vectorstore instance
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
    
    vectordb = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    
    # Ensure the directory exists
    os.makedirs(persist_directory, exist_ok=True)
    
    # Save the vectorstore
    save_path = os.path.join(persist_directory, "faiss_index")
    vectordb.save_local(save_path)
    
    # Save metadata about the documents
    metadata_path = os.path.join(persist_directory, "metadata.pkl")
    with open(metadata_path, 'wb') as f:
        pickle.dump({
            'document_count': len(chunks),
            'chunk_size': len(chunks[0].page_content) if chunks else 0
        }, f)
    
    print(f"💾 Vectorstore saved to {save_path}")
    
    return vectordb


def load_vectorstore(persist_directory="./startup_db"):
    """
    Loads an existing vectorstore from disk.
    
    Args:
        persist_directory (str): Directory where vectorstore is stored
        
    Returns:
        FAISS: Vectorstore instance or None if not found
    """
    import os
    
    # Check if the directory exists
    if not os.path.exists(persist_directory):
        return None
    
    # Check if there are actual vectorstore files
    faiss_index_path = os.path.join(persist_directory, "faiss_index")
    metadata_path = os.path.join(persist_directory, "metadata.pkl")
    
    if not os.path.exists(faiss_index_path) or not os.path.exists(metadata_path):
        return None
    
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Try to load the existing vectorstore
        vectorstore = FAISS.load_local(faiss_index_path, embeddings)
        
        # Verify it has documents
        if vectorstore and hasattr(vectorstore, 'index') and vectorstore.index.ntotal > 0:
            print(f"✅ Loaded FAISS vectorstore with {vectorstore.index.ntotal} vectors")
            return vectorstore
        else:
            print("❌ Vectorstore has no documents")
            return None
            
    except Exception as e:
        print(f"Error loading vectorstore: {e}")
        return None
