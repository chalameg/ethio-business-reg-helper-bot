# app.py
import streamlit as st
from dotenv import load_dotenv

from helpers.chunker import chunk_documents
from helpers.loader import load_documents
from helpers.vectorstore import create_or_load_vectorstore
from helpers.retriever import create_retriever
from helpers.chain import create_rag_chain


# Configure Streamlit page
st.set_page_config(page_title="Ethiopian Startup & Business Registration Helper", layout="wide")

# Main Title
st.title("🇪🇹 Ethiopian Startup & Business Registration Helper 💬")

# Load environment variables (for GROQ API key, etc.)
load_dotenv()

# Session state
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

# --- Sidebar Setup ---
with st.sidebar:
    st.header("📂 Load Your Knowledge Base")

    if st.button("Process Documents"):
        with st.spinner("Loading and indexing documents..."):
            try:
                # ✅ Load startup/business docs from ./data folder
                docs = load_documents("./data")  
                chunks = chunk_documents(docs)
                vector_store = create_or_load_vectorstore(chunks)

                # Build retriever + RAG chain
                st.session_state.retriever = create_retriever(vector_store)
                st.session_state.rag_chain = create_rag_chain(st.session_state.retriever)

                st.success("Documents processed successfully ✅")

            except Exception as e:
                st.error(f"Error: {e}")

# --- Main Q&A Area ---
st.header("💬 Ask About Ethiopian Startup & Business Registration")

if st.session_state.rag_chain:
    st.info("✅ Ready! Ask a question about Ethiopian business law or startup registration.")
    
    question = st.text_input("Enter your question:")
    
    if question:
        with st.spinner("Thinking..."):
            answer = st.session_state.rag_chain.invoke(question)
            st.markdown(f"**Answer:** {answer}")

else:
    st.info("👈 Load your documents first from the sidebar.")
