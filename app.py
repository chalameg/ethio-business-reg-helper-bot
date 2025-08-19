# app.py
import streamlit as st
from dotenv import load_dotenv

from helpers.chunker import chunk_documents
from helpers.loader import load_documents
from helpers.vectorstore import create_or_load_vectorstore
from helpers.retriever import create_retriever
from helpers.chain import create_rag_chain
from helpers.memory import get_memory_from_session, add_to_memory, clear_memory, get_conversation_history, get_memory_summary


# Configure Streamlit page
st.set_page_config(page_title="Ethiopian Startup & Business Registration Helper", layout="wide")

# Main Title
st.title("🇪🇹 Ethiopian Startup & Business Registration Helper 💬")

# Load environment variables (for GROQ API key, etc.)
load_dotenv()

# Session state - Initialize FIRST before using
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "docs_processed" not in st.session_state:
    st.session_state.docs_processed = False

# Initialize memory early to avoid None errors
from helpers.memory import create_conversation_memory
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = create_conversation_memory()

# Show app initialization status
if not st.session_state.docs_processed:
    st.info("🚀 **Initializing Application...** Please wait while we set up your knowledge base.")

# Auto-load existing processed documents on startup
if not st.session_state.docs_processed:
    # Show loading state at the top of the app
    st.info("🚀 **Initializing Application...** Please wait while we set up your knowledge base.")
    
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Load vector store
        status_text.text("📚 Step 1: Loading vector database...")
        progress_bar.progress(25)
        from helpers.vectorstore import load_vectorstore
        
        # Check if startup_db directory exists
        import os
        if os.path.exists("./startup_db"):
            st.info(f"📁 Found startup_db directory with {len(os.listdir('./startup_db'))} files")
        else:
            st.info("📁 No startup_db directory found")
        
        existing_vectorstore = load_vectorstore("./startup_db")
        
        if existing_vectorstore:
            # Step 2: Create retriever
            status_text.text("🔍 Step 2: Setting up document retriever...")
            progress_bar.progress(50)
            st.session_state.vector_store = existing_vectorstore
            st.session_state.retriever = create_retriever(existing_vectorstore)
            
            # Step 3: Create RAG chain
            status_text.text("🤖 Step 3: Initializing AI chat system...")
            progress_bar.progress(75)
            st.session_state.rag_chain = create_rag_chain(st.session_state.retriever)
            st.session_state.docs_processed = True
            
            # Complete
            progress_bar.progress(100)
            status_text.text("✅ Ready!")
            st.success("🎉 **Knowledge base loaded automatically!** You can now start asking questions.")
            st.balloons()  # Celebrate successful auto-load
            
            # Clear the progress indicators
            progress_bar.empty()
            status_text.empty()
        else:
            st.info("ℹ️ No existing knowledge base found. Please process documents to get started.")
            progress_bar.empty()
            status_text.empty()
    except Exception as e:
        st.info("ℹ️ No existing knowledge base found. Please process documents to get started.")
        progress_bar.empty()
        status_text.empty()

# --- Sidebar Setup ---
with st.sidebar:
    st.header("📂 Knowledge Base Management")
    
    # Show current status
    if st.session_state.docs_processed:
        st.success("✅ Knowledge Base Ready")
        st.info("You can now ask questions!")
        
        # Memory management section
        st.subheader("🧠 Conversation Memory")
        memory_summary = get_memory_summary()
        st.info(memory_summary)
        
        # Debug section
        st.subheader("🔍 Debug Info")
        if st.button("🔍 Check Vectorstore Status"):
            import os
            if os.path.exists("./startup_db"):
                files = os.listdir("./startup_db")
                st.info(f"📁 startup_db directory contains: {files}")
                
                # Check for FAISS files
                faiss_files = [f for f in files if f.startswith("faiss_index") or f.endswith(".pkl")]
                if faiss_files:
                    st.success(f"✅ Found FAISS vectorstore files: {faiss_files}")
                else:
                    st.warning("⚠️ No FAISS vectorstore files found")
                
                # Check if vectorstore has documents
                if st.session_state.vector_store and hasattr(st.session_state.vector_store, 'index'):
                    try:
                        doc_count = st.session_state.vector_store.index.ntotal
                        st.success(f"✅ Vectorstore has {doc_count} documents")
                    except Exception as e:
                        st.error(f"❌ Error checking document count: {e}")
                else:
                    st.warning("⚠️ No vectorstore loaded")
            else:
                st.error("❌ startup_db directory not found")
        
        if st.button("🗑️ Clear Memory"):
            clear_memory()
            st.success("Conversation memory cleared!")
            st.rerun()
        
        # Show recent conversation history
        conversation_history = get_conversation_history()
        if conversation_history:
            st.subheader("💬 Recent Conversation")
            for i, message in enumerate(conversation_history[-6:]):  # Show last 6 messages
                if hasattr(message, 'content'):
                    if hasattr(message, 'type') and message.type == 'human':
                        st.markdown(f"**You:** {message.content}")
                    else:
                        st.markdown(f"**AI:** {message.content}")
                    st.markdown("---")
        
        st.markdown("---")
        
        if st.button("🔄 Reprocess Documents"):
            with st.spinner("Reloading and reindexing documents..."):
                try:
                    # ✅ Load startup/business docs from ./data folder
                    docs = load_documents("./data")  
                    chunks = chunk_documents(docs)
                    vector_store = create_or_load_vectorstore(chunks)

                    # Build retriever + RAG chain
                    st.session_state.vector_store = vector_store
                    st.session_state.retriever = create_retriever(vector_store)
                    st.session_state.rag_chain = create_rag_chain(st.session_state.retriever)
                    st.session_state.docs_processed = True

                    st.success("Documents reprocessed successfully ✅")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("No knowledge base found. Process documents to get started.")
        
        if st.button("📚 Process Documents"):
            with st.spinner("Loading and indexing documents..."):
                try:
                    # ✅ Load startup/business docs from ./data folder
                    docs = load_documents("./data")  
                    chunks = chunk_documents(docs)
                    vector_store = create_or_load_vectorstore(chunks)

                    # Build retriever + RAG chain
                    st.session_state.vector_store = vector_store
                    st.session_state.retriever = create_retriever(vector_store)
                    st.session_state.rag_chain = create_rag_chain(st.session_state.retriever)
                    st.session_state.docs_processed = True

                    st.success("Documents processed successfully ✅")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# --- Main Q&A Area ---
st.header("💬 Ask About Ethiopian Startup & Business Registration")

if st.session_state.rag_chain:
    st.success("🚀 **Ready to Answer Questions!**")
    st.info("Ask me anything about Ethiopian business registration, startup ecosystem, or tax compliance.")
    
    question = st.text_input("💭 Enter your question:", placeholder="e.g., What are the requirements for registering a private limited company?")
    
    if question:
        with st.spinner("🤔 Searching through Ethiopian business documents..."):
            try:
                answer = st.session_state.rag_chain.invoke(question)
                
                # Add to conversation memory
                add_to_memory(question, answer)
                
                st.markdown("---")
                st.markdown("### 📋 **Answer:**")
                st.markdown(answer)
                
                # Add a helpful tip
                st.info("💡 **Tip:** You can ask follow-up questions or request more specific information about any topic.")
                
            except Exception as e:
                st.error(f"❌ Error processing your question: {e}")
                st.info("Please try rephrasing your question or check if the knowledge base is properly loaded.")

else:
    st.warning("⚠️ **Knowledge Base Not Ready**")
    st.info("Please process your documents first using the sidebar. Once processed, you'll be able to ask questions about Ethiopian business topics.")
    
    # Show what documents are available
    import os
    if os.path.exists("./data") and os.listdir("./data"):
        st.success(f"📁 Found {len(os.listdir('./data'))} document(s) in the data folder")
        st.info("Click '📚 Process Documents' in the sidebar to get started!")
    else:
        st.error("📁 No documents found in the data folder")
        st.info("Please add PDF documents to the ./data folder and then process them.")
