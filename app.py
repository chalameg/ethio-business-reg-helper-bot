# app.py
import streamlit as st
from dotenv import load_dotenv

from helpers.chunker import chunk_documents
from helpers.loader import load_documents
from helpers.vectorstore import create_or_load_vectorstore
from helpers.retriever import create_retriever
from helpers.chain import create_rag_chain
from helpers.memory import get_memory_from_session, add_to_memory, clear_memory, get_conversation_history, get_memory_summary


def format_llm_response(response_text):
    """
    Format LLM response text to preserve formatting in Streamlit frontend.
    Handles line breaks, bullet points, and spacing issues.
    """
    if not response_text:
        return response_text
    
    # Replace double line breaks with HTML breaks for better separation
    formatted = response_text.replace('\n\n', '<br><br>')
    
    # Replace single line breaks with HTML breaks
    formatted = formatted.replace('\n', '<br>')
    
    # Ensure bullet points are properly spaced
    # formatted = formatted.replace('• ', '<br>• ')
    
    # Return formatted text without background styling
    return formatted


# Configure Streamlit page
st.set_page_config(page_title="Ethio Startup Advisor", layout="wide")

# Main Title
st.title("Ethio Startup Advisor")

# App Description
st.markdown("""
<div style='text-align: center; padding: 20px; background-color: #1f77b4; border-radius: 10px; margin: 15px 0; color: white;'>
    <h4 style='color: white; margin-bottom: 10px;'> Get instant, accurate answers about Ethiopian business registration, licensing, and investment rules</h4>
    <p style='color: white; font-size: 16px; margin: 0;'><strong>Directly from official government proclamations and legal codes</strong></p>
</div>
""", unsafe_allow_html=True)

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

# Auto-load existing processed documents on startup
if not st.session_state.docs_processed:
    # Show loading state at the top of the app
    st.info("**Initializing Application...** Please wait while we set up your knowledge base.")
    
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Load vector store
        status_text.text("Step 1: Loading vector database...")
        progress_bar.progress(25)
        from helpers.vectorstore import load_vectorstore
        
        existing_vectorstore = load_vectorstore("./startup_db")
        
        if existing_vectorstore:
            # Step 2: Create retriever
            status_text.text("Step 2: Setting up document retriever...")
            progress_bar.progress(50)
            st.session_state.vector_store = existing_vectorstore
            st.session_state.retriever = create_retriever(existing_vectorstore)
            
            # Step 3: Create RAG chain
            status_text.text("Step 3: Initializing AI chat system...")
            progress_bar.progress(75)
            st.session_state.rag_chain = create_rag_chain(st.session_state.retriever)
            st.session_state.docs_processed = True
            
            # Complete
            progress_bar.progress(100)
            status_text.text("Ready!")
            st.success("**Knowledge base loaded automatically!** You can now start asking questions.")
            st.balloons()  # Celebrate successful auto-load
            
            # Clear the progress indicators
            progress_bar.empty()
            status_text.empty()
        else:
            st.info("ℹNo existing knowledge base found. Please process documents to get started.")
            progress_bar.empty()
            status_text.empty()
    except Exception as e:
        st.info("No existing knowledge base found. Please process documents to get started.")
        progress_bar.empty()
        status_text.empty()

# --- Sidebar Setup ---
with st.sidebar:
    st.header("Ethio Startup Advisor")
    
    # Show current status
    if st.session_state.docs_processed:
        st.success("Legal Advisor Ready")
        st.info("Ask questions about Ethiopian business law!")
        
        # Data Sources Info
        st.markdown("---")
        st.markdown("### **Legal Sources:**")
        st.info("""
        • Ethiopian Commercial Code (2021)
        • Investment Proclamation No. 1180/2020
        • Trade Registration Proclamation No. 980/2016
        • Tax Proclamations
        """)
        
        # Memory management section
        st.subheader("Conversation Memory")
        memory_summary = get_memory_summary()
        st.info(memory_summary)
        
        if st.button("Clear Memory"):
            clear_memory()
            st.success("Conversation memory cleared!")
            st.rerun()
        
        # Show recent conversation history
        conversation_history = get_conversation_history()
        if conversation_history:
            st.subheader("Recent Conversation")
            for i, message in enumerate(conversation_history[-6:]):  # Show last 6 messages
                if hasattr(message, 'content'):
                    if hasattr(message, 'type') and message.type == 'human':
                        st.markdown(f"**You:** {message.content}")
                    else:
                        st.markdown(f"**AI:** {message.content}")
                    st.markdown("---")
        
        st.markdown("---")
        
        if st.button("Reprocess Documents"):
            with st.spinner("Reloading and reindexing documents..."):
                try:
                    # Load startup/business docs from ./data folder
                    docs = load_documents("./data")  
                    chunks = chunk_documents(docs)
                    vector_store = create_or_load_vectorstore(chunks)

                    # Build retriever + RAG chain
                    st.session_state.vector_store = vector_store
                    st.session_state.retriever = create_retriever(vector_store)
                    st.session_state.rag_chain = create_rag_chain(st.session_state.retriever)
                    st.session_state.docs_processed = True

                    st.success("Documents reprocessed successfully")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("No knowledge base found. Process documents to get started.")
        
        if st.button("Process Documents"):
            with st.spinner("Loading and indexing documents..."):
                try:
                    # Load startup/business docs from ./data folder
                    docs = load_documents("./data")  
                    chunks = chunk_documents(docs)
                    vector_store = create_or_load_vectorstore(chunks)

                    # Build retriever + RAG chain
                    st.session_state.vector_store = vector_store
                    st.session_state.retriever = create_retriever(vector_store)
                    st.session_state.rag_chain = create_rag_chain(st.session_state.retriever)
                    st.session_state.docs_processed = True

                    st.success("Documents processed successfully")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# --- Main Q&A Area ---
st.header("Ask Your Startup Questions")

if st.session_state.rag_chain:
    st.success("**Ready to Advise!**")
    st.info("Ask me anything about Ethiopian startups, business registration, or entrepreneurship.")
    
    # Common Questions Section
    st.markdown("### **Common Questions You Can Ask:**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Business Registration:**
        • How do I register a private limited company?
        • What's the minimum capital requirement?
        • What documents do I need?

        **Licensing & Permits:**
        • How do I get a trade license?
        """)
    
    with col2:
        st.markdown("""
        **Foreign Investment:**
        • What are the foreign investment rules?
        • Can foreigners own 100% of a company?
        • What sectors are open to foreigners?
        
        **Tax & Compliance:**
        • What are the tax obligations for startups?
        • When do I need to register for VAT?
        """)
    
    question = st.text_input("Ask your startup question:", placeholder="e.g., What's the minimum capital for a private limited company?")
    
    if question:
        with st.spinner("Searching through official Ethiopian legal documents..."):
            try:
                answer = st.session_state.rag_chain.invoke(question)
                
                # Add to conversation memory
                add_to_memory(question, answer)
                
                st.markdown("---")
                st.markdown("### **Answer:**")
                
                # Use the formatting function for better display
                formatted_answer = format_llm_response(answer)
                st.markdown(formatted_answer, unsafe_allow_html=True)
                
                # Add a helpful tip
                st.info(" **Tip:** Ask follow-up questions about your startup journey in Ethiopia!")
                
            except Exception as e:
                st.error(f"Error processing your question: {e}")
                st.info("Please try rephrasing your question or check if the knowledge base is properly loaded.")

else:
    st.warning(" **Legal Advisor Not Ready**")
    st.info("Please load your Ethiopian legal documents first using the sidebar. Once loaded, I'll be ready to advise you on business registration and compliance.")
    
    # Show what documents are available
    import os
    if os.path.exists("./data") and os.listdir("./data"):
        st.success(f"Found {len(os.listdir('./data'))} legal document(s) in the data folder")
        st.info("Click 'Process Documents' in the sidebar to get started!")
    else:
        st.error("No legal documents found in the data folder")
        st.info("Please add Ethiopian legal documents (Commercial Code, Proclamations) to the ./data folder and then process them.")
